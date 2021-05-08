# image-challenge
Commands I ran:

$ virtualenv env  
$ source env/bin/activate  

$ pip3 install flask  
$ pip3 install cloudinary  
$ pip3 install psycopg2-binary flask flask-sqlalchemy  
$ pip3 install flask-jwt-extended  

# Learning Process
- This assignment became an opportunity to learn something new and try something different.
- First time working with JWT
- My impulse was to create a Flask app with a basic frontend using Jinja templates and vanilla JS/jQuery where login and image uploading are simplified, but this is something I am already very comfortable doing. Instead, I thought about how to create an API that doesn't require a frontend where everything can be done via Postman, for example.
- Realized I didn't know how to take care of authentication without user forms in the browser.
- Did research and learned about HTTP Basic Auth and its security flaws. Then I read about JSON Web Tokens or JWTs and how it can be used to protect my routes.

How to Run:
- source secrets.sh


| Route | Description |
| --- | --- |
| `/users/register` | Register a new account by supplying your desired username and password <br/><br/>curl -d '{"username":"YOUR_USERNAME", "password":"YOUR_PASSWORD"}' -H 'Content-Type: application/json' http://0.0.0.0:5000/users/register |
| `/users/login` | TBD |



