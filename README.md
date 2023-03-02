# myproject
 
### Currently they are three basic views-


**three basic functions**

- First is the init() view which basically gets the Oauth flow to start - its url- `http://127.0.0.1:8000/rest/v1/calendar/rest/v1/calendar/init/`
- Second, is the redirect() flow which access the calendar of the logged in user and renders api.html [latest 20 events]. It also saves the access tokens in the session for future use.(Currently the session expire age is set to 4 minutes for the purpose of testing and in the development). -its-url -`http://127.0.0.1:8000/rest/v1/calendar/rest/v1/calendar/redirect`/
- Third, is the myview() which basically checks if the user has a access token in the session and if it is stored, it directly access the calendar and render out the results. The access token if not there its get redirect to init() - its url - `http://127.0.0.1:8000/rest/v1/calendar/rest/v1/calendar/`
- In my view() the logic persist on refresh for 4 minutes (the session expire age which can be changed as per use)
---
### Currently the google credentials has only one test user.
---
### For to check the code you have to change the credentials
---
### And you need to download all the pacakges in requriement.txt to setup the code and run.
