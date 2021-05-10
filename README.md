# Image Repository API 
This backend-focused project stores images hosted in Cloudinary and uses JSON Web Tokens for authorization.
<br/><br/>
You can make requests to the deployed server: http://54.80.94.139/

## Content
* [Learning Process](#learn)
* [Tech Stack](#stack)
* [Routes Overview](#overview)
* [Routes Details](#details)
* [Run This Project Locally](#run)
* [Running Tests](#tests)

## <a name="learn"/>Learning Process
- I began by creating a Flask app and implementing a basic frontend using Jinja templates and vanilla JS/jQuery so that login and image uploading are simplified, but this is something I am already very comfortable doing.
- Instead, I wondered about how to create an API that doesn't require a frontend where all requests can be done via Postman, for example. I realized I had no idea how to work without user forms in the browser.
- After doing research, I read about HTTP Basic Auth and JSON Web Tokens (JWT), concepts unfamiliar to me, and this assignment grew into an opportunity to learn something new. 
- After testing my routes using Postman, I became intrigued to try everything from the command line and learned how to use `cURL` to do so.

## <a name="stack"/>Tech Stack
- Python
- Flask
- PostgreSQL
- SQLAlchemy ORM
- JSON Web Tokens
- Cloudinary API

## <a name="overview"/>Routes Overview
* [/users/register](#register)
* [/users/login](#login)
* [/users/{YOUR_USERNAME}/upload](#upload)
* [/users/{USERNAME}/images](#get_user_images)


## <a name="details"/>Routes Details
Instructions below on how to make requests to the listed routes from the command line using `curl`.<br/>
### <a name="register"/>`/users/register`

**Making a request:**

```sh
$ curl \
-d '{"username":"{YOUR_USERNAME}", "password":"{YOUR_PASSWORD}"}' \
-H 'Content-Type: application/json' \
http://54.80.94.139/users/register
```

**Example:**
```sh
curl \
-d '{"username":"user1", "password":"test1"}' \
-H 'Content-Type: application/json' \
http://54.80.94.139/users/register
```

**Successful response:**

```json
{
  "message": "Account successfully created.", 
  "status": "success", 
  "user_id": "YOUR_USER_ID", 
  "username": "YOUR_USERNAME"
}
```

### <a name="login"/>`/users/login`

**Making a request:**

```sh
curl \
-d '{"username":"{YOUR_USERNAME}", "password":"{YOUR_PASSWORD}"}' \
-H 'Content-Type: application/json' \
http://54.80.94.139/users/login
```

**Successful response:**

```json
{
  "token": "{YOUR_TOKEN_HERE_AND_BE_SURE_TO_SAVE_IT}", 
  "user_id": "{YOUR_USER_ID}"
} 
```

The token returned from this route long and can be tedious to include in subsequent requests.


### <a name="upload"/>`/users/{YOUR_USERNAME}upload`

**Making a request:**

```sh
curl \
-F "image=@{PATH/TO/IMAGE.PNG}" \
-H "Authorization: Bearer {YOUR_TOKEN}" \
http://54.80.94.139/users/{YOUR_USERNAME}/upload
```

**Example (uploading bear.png in the present directory):**

```sh
curl \
-F "image=@./bear.png" \
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMDYwODY0NCwianRpIjoiOTQ4ZTAzZjgtMGRlNC00ODhhLWE0MzYtZmQ5NGJhNjY5ZWU4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNjIwNjA4NjQ0LCJleHAiOjE2MjA2MDk1NDR9.0lPlJGHwNk6MrEPpCvE5WZIGEmikJM0-l2PgxuqjDB8" \
http://54.80.94.139/users/user1/upload
```

By default, the permission on uploaded photos is set to **PRIVATE**. Set the permission of photo on upload to **PUBLIC** by adding `'-F permission=PUBLIC'`.

```sh
curl \
-F "image=@{PATH/TO/IMAGE.PNG}" \
-F permission=PUBLIC -H "Authorization: Bearer {YOUR_TOKEN}"  \
http://54.80.94.139/users/{YOUR_USERNAME}/upload
```

**Successful response:**

```json
{
  "image_url": "{HTTP_URL_FOR_IMAGE}", 
  "message": "Image successfully uploaded.", 
  "permission": "{PRIVATE_OR_PUBLIC}", 
  "status": "success"
}
```

### <a name="get_user_images"/>`/users/{USERNAME}/images`
Get all images if you are requesting own images. Get public images of another user.

**Making a request:**

```sh
curl \
-H "Authorization: Bearer {YOUR_TOKEN}" \
http://54.80.94.139/users/{USERNAME}/images
```

**Example:**
```sh
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMDYwODY0NCwianRpIjoiOTQ4ZTAzZjgtMGRlNC00ODhhLWE0MzYtZmQ5NGJhNjY5ZWU4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNjIwNjA4NjQ0LCJleHAiOjE2MjA2MDk1NDR9.0lPlJGHwNk6MrEPpCvE5WZIGEmikJM0-l2PgxuqjDB8" \
http://54.80.94.139/users/user1/images
```
**Successful response:**

```json
{
  "images": [
    {
      "id": 1, 
      "image_url": "url/for/user1image1", 
      "permission": "PRIVATE"
    }, 
    {
      "id": 2, 
      "image_url": "url/for/user1image2_private", 
      "permission": "PUBLIC"
    }, 
    {
      "id": 4, 
      "image_url": "url/for/img", 
      "permission": "PUBLIC"
    }
  ], 
  "status": "success", 
  "total": 3
}
```

## <a name="run"/>Run This Project Locally
- Clone this repository

```sh
$ git clone https://github.com/nan-li/image-repository-api.git
```

- Create and activate a virtual environment in the directory

```sh
$ virtualenv env  
$ source env/bin/activate
```

- Install dependencies

```sh
$ pip3 install -r requirements.txt
```

- Sign up for a Cloudinary account
- Create `secrets.sh` in the directory with the following:

```sh
export CLOUDINARY_CLOUD_NAME="YOUR_CLOUD_NAME"
export CLOUDINARY_API_KEY="YOUR_API_KEY"
export CLOUDINARY_API_SECRET="YOUR_API_SECRET"
export JWT_SECRET_KEY="YOUR_JWT_KEY"
```

- Load these variables into the shell
```sh
$ source secrets.sh
```

- Create and seed the database
```sh
$ python3 seed.py
```

- Run the server
```sh
$ python3 server.py
```

Now you can make requests to your own server at: http://0.0.0.0:5000/


## <a name="tests"/>Running Tests
```sh
$ createdb testdb
$ python3 tests.py
```
