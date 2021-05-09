# Image Repository API 🖥️
This backend-focused project stores images hosted by Cloudinary and uses JSON Web Tokens for authorization.


Commands I ran:

$ virtualenv env  
$ source env/bin/activate
$ source secrets.sh 

$ pip3 install flask  
$ pip3 install cloudinary  
$ pip3 install psycopg2-binary flask flask-sqlalchemy  
$ pip3 install flask-jwt-extended  

## Learning Process
- I began by creating a Flask app with the intention to implement a basic frontend using Jinja templates and vanilla JS/jQuery so that login and image uploading are simplified, but this is something I am already very comfortable doing.
- Instead, I wondered about how to create an API that doesn't require a frontend where all requests can be done via Postman, for example. I realized I had no idea how to work without user forms in the browser.
- After doing research, I read about HTTP Basic Auth and JSON Web Tokens (JWT), concepts unfamiliar to me, and this assignment grew into an opportunity to learn something new. 
- After testing my routes using Postman, I became intrigued to try everything from the command line and learned how to use `curl` to do so.

## Routes Overview
* [/users/register](#register)
* [/users/login](#login)
* [/users/<YOUR_USERNAME>/upload](#upload)

## Routes Details

### <a name="register"/>`/users/register`

Making a request:

```
curl -d '{"username":"<YOUR_USERNAME>", "password":"<YOUR_PASSWORD>"}' -H 'Content-Type: application/json' http://0.0.0.0:5000/users/register
```

Successful response:

```json
{
  "message": "Account successfully created.", 
  "status": "success", 
  "user_id": "YOUR_USER_ID", 
  "username": "YOUR_USERNAME"
}
```

### <a name="login"/>`/users/login`

Making a request:

```
curl -d '{"username":"<YOUR_USERNAME>", "password":"<YOUR_PASSWORD>"}' -H 'Content-Type: application/json' http://0.0.0.0:5000/users/login
```

Successful response:

```json
{
  "token": "<YOUR_TOKEN_HERE_AND_BE_SURE_TO_SAVE_IT>", 
  "user_id": 1
} 
```

### <a name="upload"/>`/users/<YOUR_USERNAME>/upload`
Making a request:

```
curl -F "image=@<PATH/TO/IMAGE.PNG>" -H "Authorization: Bearer <YOUR_TOKEN>" http://0.0.0.0:5000/users/<YOUR_USERNAME>/upload
```

By default, the default permission on uploaded photos is set to PRIVATE. Set the permission of photo on upload to PUBLIC by adding '-F permission=PUBLIC'.

```
curl -F "image=@<PATH/TO/IMAGE.PNG>" -F permission=PUBLIC -H "Authorization: Bearer <YOUR_TOKEN>"  http://0.0.0.0:5000/users/<YOUR_USERNAME>/upload
```

Successful response:

```
{
  "image_url": "<HTTP_URL_FOR_IMAGE>", 
  "message": "Image successfully uploaded.", 
  "permission": "<PRIVATE_OR_PUBLIC>", 
  "status": "success"
}
```


## Running Tests
$ createdb testdb
$ python3 tests.py

## How to Run the API
- source secrets.sh


