## MIX Fight project

### Настройки окружения:

1. Создать файл `.env` в корне проекта:
2. Данные для заполнения `./.env`
    *  ```text
       POSTGRES_PASSWORD='postgres_password'
       POSTGRES_USER='postgres_user'
       POSTGRES_DB='mix_fight'
       ```
3. Создать файл `.env` по пути `./frontend/.env`:
4. Данные для заполнения `./frontend/.env`
    *  ```text
       VITE_GOOGLE_KEY='<GOOGLE TOKEN>' -> Для работы авторизации\регистрации через гугл 
       ```
5. Создать файл `.env` по пути `./backend/.env`:
6. Данные для заполнения `./backend/.env`
    *  ```text
       SECRET_KEY='django-insecure-=r(-91pryk#+b!5sia6!=_*9h%=$mxy4hu+396sl@p5eqt(of9'
       GOOGLE_KEY='<GOOGLE TOKEN>' -> Для получения данных о пользователе(тот же что и в VITE_GOOGLE_KEY)
       EMAIL_PASSWORD='<MAIL PASSWORD>' -> Для отправки сообщений подтверждения почты
       EMAIL_SERVER='<MAIL HOST>' -> Для отправки сообщений подтверждения почты
       URL_FRONTEND='http://localhost:80/confirm_email/' -> Порт должен соответствовать тому, что указан в контейнере Vue
       SQL_PASSWORD='postgres_password'
       SQL_USER='postgres_user'
       SQL_DB='mix_fight'
       SQL_PORT='5432:5432'
       SQL_HOST='Postgres'
       SQL_ENGINE='django.db.backends.postgresql'
       ```

### Для запуска проекта в dev версии:

1. Необходимо проверить `./docker-compose.yml` чтобы в нем был раскомментирован контейнер `Nginx` и был закомментирован
   контейнер `Vue`
2. `Publisher` порт в контейнере `Nginx` должен соответствовать порту на который будет ссылаться контейнер в
   файле `./frontend/src/plugins/index.js` в строке `axios.defaults.baseURL = 'http://localhost:<PORT>/api/'`
3. Установить необходимые библиотеки для клиента:
4. В папке `./frontend/` ввести команду `yarn install` или `npm install`
5. Для развертки проекта ввести команду `make dev` -> запуск `Postgres`,`Nginx`
6. Старт клиентской части `make front` -> запуск `Vue` приложения

### Для запуска проекта в prod версии:

1. Необходимо проверить `./docker-compose.yml` чтобы в нем был закомментирован контейнер `Nginx` и был раскомментирован
   контейнер `Vue`
2. `Publisher` порт в контейнере `Vue` должен соответствовать порту на который будет ссылаться контейнер в
   файле `./frontend/src/plugins/index.js` в строке `axios.defaults.baseURL = 'http://localhost:<PORT>/api/'`
3. Для развертки проекта достаточно ввести команду `make prod`
