# EnterScale-Assessment
Backend Engineer Assessment for Enter Scale developed with django and Django Rest-framework

Technologies used:
1. Python
2. Django
3. Django Rest-Framework
4. SQLite
5. Celery
6. Redis
7. Docker



## Brief Explanation:
A dummy Admin have been created with the following details:

    email: admin@email.com
    password: admin@email.com




## Environment Variables
The following are the needed environment variables that should be added to an .env file:
PAYSTACK_SECRET_KEY
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD


## Development
1. Install docker
2. Run `docker compose build`
3. Run `docker compose up`
4. To stop the server, run `docker compose down`


## API Documentation

The auth token can be passed through the Authorization field in the request headers, in this format:
- Bearer XXXXXX

There are 3 Swagger Pages for the API documentation
1. Core Operations (Auth and Admin endpoints): http://127.0.0.1:8000/docs/core/
    - All endpoints here, except the auth endpoints, are protected
2. Vendor Operations: http://127.0.0.1:8000/docs/vendor/
    - All vendor endpoints are protected

3. Customer Operations: http://127.0.0.1:8000/docs/customer/
    - All endpoints here are open


## System Design Flow
Below are two Images that depict the system design flow

### Vendor account creation and product creation flow
![Vendor Flow](<Vendor Flow.png>)

### Customer order flow

![Customer order flow](<Order flow.png>)