# 3 задание QA guru
Инструкция по запуску postgres в докере находится в файле app/Docker Postgres Manual.md

Для работы с БД используется SQLModel, также используется Alembic для миграций.  
Инструкция по началу работы с SQLModel совместно с Alembic и БД, находящейся в докер контейнере:
- запустите БД в контейнере по инструкции выше
- установите необходимые пакеты в окружение (ниже пример для pipenv)
```
pipenv install sqlalchemy sqlmodel alembic
```
- для начала настроим БД. Создайте в пакете app пакет models. Здесь будет 2 файла: database.py - настройки и предустановки для работы с БД и models.py - сами модели и базовые методы для работы с моделями.
В файле database.py сделайте следующее:  
Создайте движок, используя строку подключения к БД в докере
```python
engine = create_engine(SQLMODEL_DATABASE_URL, pool_size=int(os.getenv('DATABASE_POOL_SIZE', 10)))
```
create_engine мы используем из SQLModel, SQLMODEL_DATABASE_URL - строка подключения к БД в контейнере, тажке устанавливается максимальное число одновременных подключений, по умолчанию 10.
Создайте класс сессии с едиными параметрами, используя фабрику sessionmaker из SQLAlchemy
```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)
```
Здесь отключен автосброс в БД, автокоммит и добавлена привязка к движку и классу SQLModel.Session
Определите функцию сессии для использования её в эндпоинтах с помощью fastapi.Depends
```python
def get_db():
    with SessionLocal() as session:
        yield session
```
Таким образом сессия будет автоматически закрываться в каждом эндпоинте без необходимости открытия её каждый раз с помощью контекстного менеджера.  
В файле models.py сделайте следующее:  
Создайте базовые классы, в моём случае, это авторы и их книги. Автор имеет поля id, first_name, second_name. Книга имеет поля id, title, price, author_id.  
Создайте базовый класс, имеющий поле id, используемый автором и книгой для упрощения кода.  
```python
class DefaultBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, index=True)
```
Создайте базовые модели (не таблицы) с набором обязательных полей для автора и книги. Эти модели можно передавать в форму при запросе на создание автора или книги.  
```python
class AuthorBase(SQLModel):
    first_name: str = Field(max_length=100, nullable=False)
    last_name: str = Field(max_length=100, nullable=False)

class BookBase(SQLModel):
    title: str = Field(max_length=100, nullable=False)
    price: float = Field(nullable=False, gt=0)
    author_id: int = Field(foreign_key='authors.id', nullable=False)
```
Наконец создайте модели БД для автора и книги
```python
class Author(DefaultBase, AuthorBase, table=True):
    __tablename__ = 'authors'

    books: List['Book'] = Relationship(
        back_populates='author',
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan',
        }
    )

class Book(DefaultBase, BookBase, table=True):
    __tablename__ = 'books'

    author: 'Author' = Relationship(
        back_populates='books'
    )
```
- теперь настроим миграции, используя Alembic:  
Миграции следует располагать в корневой папке приложения. Выполните следующую команду:
```
alembic init migrations
```
Эта команда создаст необходимую структуру миграций следующего вида:
```
yourproject/
    alembic.ini
    migrations/
        env.py
        README
        script.py.mako
        versions/
            __init__.py
```
Следует настроить 3 файла: alembic.ini - файл конфигурации Alembic, он должен располагаться в той же папке, откуда вызываются команды миграции, env.py - скрипт, вызываемый при каждой миграции, script.py.mako - файл шаблона генерации миграций.  
В alembic.ini сделайте следующее:  
Укажите script_location = migrations - имя папки с миграциями
В env.py сделайте следующее:
Добавьте необходимые импорты, чтобы alembic корректно распознал модели
```python
from sqlmodel import SQLModel
from app.models.models import *
```
Загрузите переменные из файла окружения
```python
load_dotenv(".env")
```
Добавьте переменную со строкой подключения к БД в докере, как указано в начале
```python
SQLALCHEMY_DATABASE_URL = os.getenv("DOCKER_DATABASE_URL")
```
и используйте её в конфигурации alembic
```python
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)
```
Добавьте метаданные из SQLModel для поддержки автогенерации миграций
```python
target_metadata = SQLModel.metadata
```
В script.py.mako сделайте следующее:  
Импортируйте sqlmodel (можно сразу после импорта sqlalchemy) для корректной автогенерации полей
```python
import sqlmodel
```
- создайте начальную миграцию
```
alembic revision --autogenerate -m "Initial"
```
Примените миграцию - это перенесёт созданные в проекте таблицы в БД в докере
```
alembic upgrade head
```
Проверьте, созданы ли таблицы, подключившись к контейнеру с БД
```
docker exec -it <container_name> psql -U <user_name> -d <db_name>
```
Далее проверьте список таблиц в базе
```
\dt
```
Команда должна вывести список, в котором будут таблицы authors и books. Это значит, что миграция прошла корректно.