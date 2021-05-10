# Image Repository API 🖥
This backend-focused project stores images hosted in Cloudinary and uses JSON Web Tokens for authorization.

## Learning Process
- I began by creating a Flask app with the intention to implement a basic frontend using Jinja templates and vanilla JS/jQuery so that login and image uploading are simplified, but this is something I am already very comfortable doing.
- Instead, I wondered about how to create an API that doesn't require a frontend where all requests can be done via Postman, for example. I realized I had no idea how to work without user forms in the browser.
- After doing research, I read about HTTP Basic Auth and JSON Web Tokens (JWT), concepts unfamiliar to me, and this assignment grew into an opportunity to learn something new. 
- After testing my routes using Postman, I became intrigued to try everything from the command line and learned how to use `curl` to do so.

## Tech Stack
- Python
- Flask
- PostgreSQL
- SQLAlchemy ORM
- JSON Web Tokens
- Cloudinary API

## Routes Overview
* [/users/register](#register)
* [/users/login](#login)
* [/users/<YOUR_USERNAME>/upload](#upload)
* [/users/<USERNAME>/images](#get_user_images)


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
  "user_id": <YOUR_USER_ID>
} 
```

### <a name="upload"/>`/users/<YOUR_USERNAME>/upload`
Making a request:

```
curl -F "image=@<PATH/TO/IMAGE.PNG>" -H "Authorization: Bearer <YOUR_TOKEN>" http://0.0.0.0:5000/users/<YOUR_USERNAME>/upload
```

By default, the default permission on uploaded photos is set to PRIVATE. Set the permission of photo on upload to PUBLIC by adding `'-F permission=PUBLIC'`.

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

### <a name="get_user_images"/>`/users/<USERNAME>/images`
Get all images if you are requesting own images. Get public images of another user.

Making a request:

```
curl -H "Authorization: Bearer <YOUR_TOKEN>" http://0.0.0.0:5000/users/<USERNAME>/images
```

Successful response:

```
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
      "image_url": "http://res.cloudinary.com/dfzb7jmnb/image/upload/v1620607893/f1eojamkyrjfygzwvqp7.png", 
      "permission": "PUBLIC"
    }
  ], 
  "status": "success", 
  "total": 3
}
```

## Run This Project
- Clone this repository

```
$ git clone https://github.com/nan-li/image-repository-api.git
```

- Create and activate a virtual environment in the directory

```
$ virtualenv env  
$ source env/bin/activate
```

- Install dependencies

```
$ pip3 install -r requirements.txt
```

- Sign up for a Cloudinary account
- Create `secrets.sh` in the directory with the following:

```
export CLOUDINARY_CLOUD_NAME="YOUR_CLOUD_NAME"
export CLOUDINARY_API_KEY="YOUR_API_KEY"
export CLOUDINARY_API_SECRET="YOUR_API_SECRET"
export JWT_SECRET_KEY="YOUR_JWT_KEY"
```

- Load these variables into the shell
```
$ source secrets.sh
```

- Create and seed the database
```
$ python3 seed.py
```

- Run the server
```
$ python3 server.py
```

## Running Tests
```
$ createdb testdb
$ python3 tests.py
```
