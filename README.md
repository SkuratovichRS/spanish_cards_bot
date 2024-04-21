# Бот для изучения английского языка
## Описание
Проект представляет собой телеграм-бот, который помогает пользователям изучать английские слова. Бот предоставляет пользователю карточки с русскими словами и требует перевода на английский язык. Бот включает в себя основные слова для всех пользователей и список слов для конкретного пользователя. Реализованы функции добавления и удаления слов из этого списка.

## Основные и дополнительные компоненты проекта
Проект включает в себя следующие компоненты:

### 1. Бот
Этот компонент является основным интерфейсом для взаимодействия пользователя с проектом. Он обрабатывает входящие сообщения и команды от пользователей, предоставляет им слова для изучения, отслеживает и сохраняет изменения в базе данных.

### 2. База данных
База данных включает в себя таблицы для хранения набора слов и пользователей и отслеживает прогресс пользователя.

### 3. Дополнительные компоненты
Реализованы следующие функции: добавление слов в общий для всех пользователей список, автоматический перевод добавленного пользователем слова, генерация вариантов ответа для добавленных пользователем слов.  

## Инструкции по установке
1. Клонируйте репозиторий на свой локальный компьютер.
2. Установите необходимые зависимости, выполнив команду `pip install -r requirements.txt`.
3. Создайте и настройте базу данных, используя схему в файле `EnglishBotDB_schema.jpg`.
4. Занесите в файл `settings.ini` токен своего бота и данные для подключения к БД.
5. Выполните команду `python fill_db.py` для заполнения БД начальными данными.
6. Запустите бота, выполнив команду `python main.py`.

## Начало работы
1. Нажмите команду `/start`.
2. Используйте предложенные команды и кнопки для изучения английских слов.


