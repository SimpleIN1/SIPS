
## Development

Команда для перезагрузки daphne сервера при изменении .py или .html файлов , используя wathcmedo

    watchmedo auto-restart --patterns="*.py;*.html" --recursive -- daphne -b 0.0.0.0 -p 8092 AlgorithmManagerProject.asgi:application

Команда для перезагрузки сelry при изменении .py, используя wathcmedo

     watchmedo auto-restart --patterns="celery_app/tasks.py;celery_app/app.py" --recursive -- celery -A celery_app.app worker --loglevel=info --concurrency=4

## Prod
Настройка .env файла. Пример:

    SECRET_KEY=******
    DEBUG=0
    
    CACHE_REDIS=redis://127.0.0.1:6379/0
    
    CELERY_BROKER_URL=redis://127.0.0.1:6379/2
    CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2
    
    CHANNEL_REDIS_URL=redis://127.0.0.1:6379/2
    
    LOGS_REDIS_URL=redis://127.0.0.1:6379/2
    
    POSTGRES_DB=algmanager_db
    POSTGRES_USER=algmanager_user
    POSTGRES_PASSWORD=algmanager_pass
    POSTGRES_HOST=172.20.0.2
    POSTGRES_PORT=5432
    
    AUTH_LDAP_SERVER_URI=ldap://
    AUTH_LDAP_BASE_DN=ou=People,dc=example,dc=com
    AUTH_LDAP_FILTERSTR=(uid=%(user)s)


Создать жесткие ссылки для сервисов

    sudo ln ./systemd_processes/alg-manager.service /etc/systemd/system/
    sudo ln ./systemd_processes/alg-manager-celery.service /etc/systemd/system

Перезагрузить systemd демон
    
    sudo systemstl daemon-reload

Запуск сервисов

    sudo systemctl start alg-manager.service
    sudo systemctl start alg-manager-celery.service

Создание символической ссылки проекта, чтобы использовать статичный путь в переменной WorkingDirectory.
"/path/to" заменить на путь к проекту на сервере

    sudo ln -sfn /path/to/AlgorithmManagerService /var/www/

## Необходимые правки
1. Настроить nginx+
2. Натсроить cors,csrf +
3. Проверить сборку докера
4. Залить приложение
5. Нарезать tif на сервере +
6. Доделать alg-manager-service (
   1. возможность просмотра выходных файлов, 
   2. добавления в базу данных файлов с сервера, 
   3. создание копий запуска алгоритма,
   4. фильтры, 
   5. websocket на вкладку со списком файлов запуска