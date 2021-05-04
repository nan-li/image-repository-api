# image-challenge
Commands I ran:

$ virtualenv env
$ source env/bin/activate  

$ pip3 install flask  
$ pip3 install cloudinary  
$ pip3 install psycopg2-binary flask flask-sqlalchemy  

# Learning Process
- Took this assignment as an opportunity to learn something new and try something different.
- First time working with JWT
- My impulse was to create a Flask app with a basic frontend using Jinja templates where login and image uploading are simplified. Then I thought about how to create an API that doesn't require a frontend where everything can be done via Postman for example.
- Realized I didn't know how to take care of authentication without user forms in the browser.
- Did research and learned about HTTP Basic Auth and its security flaws. Then I read about JSON Web Tokens or JWTs and how it can be used to protect my routes.