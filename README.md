Инструкция по запуску проекта
1.Клонируйте репозиторий:
git clone https://github.com/spiculor/TestTask.git
cd TestTask

2.Убедитесь, что у вас установлен Docker и Docker Compose.
Создайте и запустите контейнеры с помощью Docker Compose:
"docker-compose up --build"
Дождитесь запуска всех сервисов. После успешного запуска, API будет доступен по адресу http://localhost:8000.

3.Документация API:
Вы можете получить доступ к документации Swagger по адресу http://localhost:8000/docs.

4.Тестирование API:
Используйте маршруты /auth/register и /auth/login для регистрации и аутентификации пользователя.
После входа в систему используйте полученные токены для выполнения операций с задачами (создание, получение, обновление, удаление) через маршруты /tasks.