# Services

## Settings environs

---

Move to "backend/AuthenticationService/AccountProject" dir and create environ files:
    
    .docker.auth.env
    .docker.auth.postgres.env
    .docker.brocker.env

Example conf for ".docker.auth.env":

    DEBUG=1
    SECRET_KEY=django-insecure-i29mexw0loav@^2l@kh7)v^4dr$6m+hy=qfd!==+s52$m%ek7c
    
    EMAIL_HOST=smtp.mail.ru
    EMAIL_PORT=2525
    EMAIL_USE_TLS=1
    EMAIL_HOST_USER=testemail.emal@mail.ru
    EMAIL_HOST_PASSWORD=ZfTnzUitFRhP6JmjzSqG
    
    WEBSITE_NAME=SIPS
    SCHEMA=http
    DOMAIN=0.0.0.0
    PORT=5000
    SUPPORT_EMAIL=test@example.ru
    
    EMAIL_SEND=1
    
    CACHE_REDIS=redis://redis:6379/0
    
    URL_FRONTEND_404=http://0.0.0.0:5000/404
    URL_FRONTEND_RESET_PASSWORD=http://0.0.0.0:5000/reset_password
    
    MIGRATIONS=1

Example conf for ".docker.auth.postgres.env":
    
    POSTGRES_PASSWORD=postgres_pass
    POSTGRES_DB=postgres_db
    POSTGRES_USER=postgres_user
    POSTGRES_PORT=5432
    POSTGRES_HOST=postgres-auth

Example conf for ".docker.auth.postgres.env":

    CELERY_BROKER_URL=redis://redis:6379/1
    CELERY_RESULT_BACKEND=redis://redis:6379/1

## Authentication service

---
Example url to swagger documentation for authentication service:
    
    http://127.0.0.1:5000/api/account/swagger/

Run auth service:

    docker-compose -f docker-compose.dev.yml up -d server-auth redis postgres-auth celery-worker
    or
    docker-compose -f docker-compose.dev.hub.yml up -d server-auth redis postgres-auth celery-worker

Run commands into docker-container (not required):

    docker-compose -f docker-compose.dev.yml exec server-auth ../venv/bin/python manage.py makemigrations
    docker-compose -f docker-compose.dev.yml exec server-auth ../venv/bin/python manage.py migrate

