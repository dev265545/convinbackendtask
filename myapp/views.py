from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from django.contrib.sessions.backends.cache import SessionStore
from datetime import datetime, time, timedelta
from google.auth.exceptions import UserAccessTokenError
from google.auth.transport.requests import Request

class MyView(APIView):
    def get(self, request):
        access_token = request.session.get('google_auth_access_token')
        refresh_token = request.session.get('google_auth_refresh_token')
        if not access_token or not refresh_token:
            return HttpResponseRedirect(reverse('google-calendar-init'))

        credentials = Credentials.from_authorized_user_info(info={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_uri': settings.GOOGLE_OAUTH2_TOKEN_URI,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        })

        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # Use the credentials to access the user's calendar data
        # ...
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary',
                timeMin=datetime.utcnow().isoformat() + 'Z',  # 'Z' indicates UTC time
                maxResults=20,
                singleEvents=True,
                orderBy='startTime').execute()
        events = events_result.get('items', [])

        return render(request, 'api.html', {'events': events})
class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=settings.GOOGLE_OAUTH2_SCOPES,
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect')),
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )
        request.session['google_auth_state'] = state
        return HttpResponseRedirect(authorization_url)
class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        state = request.session.get('google_auth_state', None)
        if not state:
            return HttpResponseRedirect(reverse('google-calendar-init'))

        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=settings.GOOGLE_OAUTH2_SCOPES,
            state=state,
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect')),
        )

        try:
            flow.fetch_token(authorization_response=request.build_absolute_uri())
        except UserAccessTokenError as e:
            if e.args[0]['error'] == 'invalid_grant':
                # Invalidate the session and redirect the user to the initial authentication flow
                del request.session['google_auth_state']
                return HttpResponseRedirect(reverse('google-calendar-init'))
            else:
                # Handle other TokenError exceptions as needed
                raise e

        credentials = flow.credentials
        
        # Store the access token and refresh token in the session
        request.session['google_auth_access_token'] = credentials.token
        request.session['google_auth_refresh_token'] = credentials.refresh_token

        # Use the credentials to access the user's calendar data
        # For example:
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary',
                timeMin=datetime.utcnow().isoformat() + 'Z',  # 'Z' indicates UTC time
                maxResults=20,
                singleEvents=True,
                orderBy='startTime').execute()
        events = events_result.get('items', [])

        return render(request, 'api.html', {'events': events})
