# Services

## Settings environs

### Accounting service

---

Move to "backend/AccountingService/AccountProject" dir and create environ files:
    
    .docker.account.env
    .docker.account.postgres.env
    .docker.brocker.env

Example conf for ".docker.account.env":

    DEBUG=0
    SECRET_KEY=django-insecure-key
    JWT_SECRET_KEY=jwt-secret-key-key
    
    ACCESS_TOKEN_LIFETIME=5
    
    ALLOWED_HOSTS=*
    INTERNAL_IPS=127.0.0.1,0.0.0.0,localhost
    CSRF_TRUSTED_ORIGINS=https://0.0.0.0:8443,https://127.0.0.1:8443,http://127.0.0.1:8090
    CORS_ORIGIN_WHITELIST=https://0.0.0.0,https://127.0.0.1
    
    EMAIL_HOST=mail.ru
    EMAIL_PORT=587
    EMAIL_USE_TLS=1
    EMAIL_HOST_USER=test@mail.ru
    EMAIL_HOST_PASSWORD=host_password
    
    WEBSITE_NAME=SIPS
    SCHEMA=https
    DOMAIN=127.0.0.1
    PORT=8090
    SUPPORT_EMAIL=test@mail.ru
    
    CACHE_REDIS=redis://redis:6379/0
    
    FRONTEND_404_URL=https://frontend-host/404
    FRONTEND_RESET_PASSWORD_VERIFICATION_URL=https://frontend-host/reset-password/
    FRONTEND_REGISTER_EMAIL_VERIFICATION_URL=https://frontend-host/verify-email/
    FRONTEND_REGISTER_VERIFICATION_URL=https://frontend-host/verify-user/
    
    MIGRATIONS=1

Example conf for ".docker.account.postgres.env":
    
    POSTGRES_PASSWORD=postgres_pass
    POSTGRES_DB=postgres_db
    POSTGRES_USER=postgres_user
    POSTGRES_PORT=5432
    POSTGRES_HOST=postgres-auth

Example conf for ".docker.account.postgres.env":

    CELERY_BROKER_URL=redis://redis:6379/1
    CELERY_RESULT_BACKEND=redis://redis:6379/1

Example url to swagger documentation for authentication service:
    
    http://127.0.0.1:5000/api/vaccount/docs/swagger/?format=openapi

Run auth service:

    docker-compose -f docker-compose.dev.yml up -d server-account redis postgres-auth celery-worker
    or
    docker-compose -f docker-compose.dev.hub.yml up -d server-account redis postgres-auth celery-worker

Run commands into docker-container (not required):

    docker-compose -f docker-compose.dev.yml exec server-account ../venv/bin/python manage.py makemigrations
    docker-compose -f docker-compose.dev.yml exec server-account ../venv/bin/python manage.py migrate

Run command collect static

    docker-compose -f docker-compose.prod.yml exec server-account ../venv/bin/python manage.py collectstatic

### Auth service

---
