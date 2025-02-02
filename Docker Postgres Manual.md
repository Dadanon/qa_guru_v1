# Инструкция по установке postgres в docker контейнере и подключению к БД

1. Скачайте Docker с официального сайта (https://docs.docker.com/get-started/get-docker/) и установите. После установки проверьте работоспособность Docker, набрав в консоли ```docker version```
2. Создайте файл docker-compose.yml в корневой папке проекта и напишите в нем следующее:
```yaml
services:
  postgres:
    image: postgres:17-alpine
    env_file:
      - .env
    environment:
      POSTGRES_USER: $(DOCKER_DATABASE_USER)
      POSTGRES_PASSWORD: $(DOCKER_DATABASE_PASSWORD)
      POSTGRES_DB: $(DOCKER_DATABASE_DB_NAME)
    ports:
      - '5434:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```
- мы запускаем в docker-compose один контейнер - postgres
- выбираем последнюю версию и явно её указываем: postgres:17-alpine. При запуске файла docker-compose необходимый образ postgres скачается автоматически
- также явно указываем файл окружения, в котором будут храниться переменные, используемые в docker-compose: .env
- в окружении (environment) мы указываем имя пользователя, с помощью которого мы будем коннектиться к БД, пароль этого пользователя и название БД
- настройка порта необходима, если у нас установлен локальный postgres, который работает по умолчанию на 5432 порту. В этом случае мы пишем, что будем обращаться к БД, которая крутится в контейнере на 5432 (стандартном) порту, делая запрос на другой порт (в данном случае, 5434)
- напоследок мы указываем раздел для хранения данных БД для того, чтобы при перезапуске контейнера данные сохранялись

3. Запустите файл, набрав в консоли
```bash
docker-compose up -d 
```
4. Проверьте работу контейнера командой ```docker ps```. Строка списка запущенных контейнеров, описывающая работающий postgres, должна выглядеть примерно так:
```
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS          PORTS                    NAMES
6f16bc935a69   postgres:17-alpine   "docker-entrypoint.s…"   14 minutes ago   Up 14 minutes   0.0.0.0:5434->5432/tcp   qa_guru_v1-postgres-1
```