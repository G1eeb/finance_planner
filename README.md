# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов и расходов, контроля месячного бюджета
и отслеживания финансовых целей.

**Веб-интерфейс:** Django + Django Template Language (DTL).
**Хранение данных:** SQLite (с ПР7). JSON сохранён как предыдущая реализация.

## 1. Назначение проекта

Finance Planner — учебное приложение для управления доходами, расходами
и месячными бюджетами. Проект развивается поэтапно:

- ПР1–ПР3 — предметная область на Python (классы, JSON-хранилище);
- ПР5 — веб-интерфейс на Django (HTML в Python);
- ПР6 — переход на **систему шаблонов Django**;
- ПР7 — **слой реляционной базы данных SQLite**.

## 2. Используемые технологии

- **Python 3**;
- **Django 5**;
- **Django Template Language (DTL)**;
- **HTML5**, **CSS3**, **JavaScript**;
- **Bootstrap 5** (CDN);
- **SQLite 3** — база данных (файл `data/finance_planner.sqlite`);
- **json** — предыдущая реализация хранилища;
- **Git**, **pytest**, **flake8**.

## 3. Предметная область

Четыре таблицы базы данных:

| Таблица | Назначение |
|---|---|
| **categories** | справочник категорий (уникальные названия) |
| **incomes** | доходы |
| **expenses** | расходы |
| **budgets** | месячные бюджеты |

## 4. Структура базы данных

### 4.1. Таблица `categories`

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | PK — идентификатор |
| `name` | TEXT | название категории, UNIQUE, NOT NULL |

### 4.2. Таблица `incomes` — доходы

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | PK — идентификатор |
| `amount` | REAL | сумма, NOT NULL |
| `category_id` | INTEGER | FK → `categories.id`, NOT NULL |
| `date` | TEXT | дата в формате ISO (YYYY-MM-DD), NOT NULL |

### 4.3. Таблица `expenses` — расходы

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | PK — идентификатор |
| `amount` | REAL | сумма, NOT NULL |
| `category_id` | INTEGER | FK → `categories.id`, NOT NULL |
| `date` | TEXT | дата в формате ISO (YYYY-MM-DD), NOT NULL |

### 4.4. Таблица `budgets` — бюджеты

| Поле | Тип | Назначение |
|---|---|---|
| `id` | INTEGER | PK — идентификатор |
| `month` | TEXT | месяц в формате YYYY-MM, UNIQUE, NOT NULL |
| `monthly_budget` | REAL | сумма бюджета, NOT NULL |
| `current_expenses` | REAL | потрачено, NOT NULL, DEFAULT 0 |

### 4.5. Ключи

- **Первичные ключи (`PRIMARY KEY`)** — `id` в каждой таблице.
- **Внешние ключи (`FOREIGN KEY`)**:
  - `incomes.category_id → categories.id`;
  - `expenses.category_id → categories.id`.

При каждом подключении включается проверка внешних ключей
(`PRAGMA foreign_keys = ON`) — это гарантирует целостность данных.

## 5. Файлы базы данных

```
finance_planner/
├── data/
│   └── finance_planner.sqlite      ← файл БД (генерируется, в .gitignore)
├── sql/
│   ├── schema.sql                  ← CREATE TABLE
│   └── queries.sql                 ← 16 SQL-запросов проекта
└── db/
    ├── __init__.py
    ├── database.py                 ← get_connection() + PRAGMA foreign_keys = ON
    └── import_json.py              ← перенос JSON → SQLite
```

**`sql/schema.sql`** — команды создания таблиц `categories`, `incomes`,
`expenses`, `budgets` с полями, типами и ограничениями (`PRIMARY KEY`,
`FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT`).

**`sql/queries.sql`** — 16 SQL-запросов с комментариями, покрывающих:

- выборку списков (`SELECT`);
- фильтрацию (`WHERE`);
- соединение таблиц (`JOIN`);
- агрегатные функции (`COUNT`, `SUM`, `AVG`);
- группировку (`GROUP BY`);
- фильтрацию групп (`HAVING`);
- параметризованные запросы (`?`).

**`db/import_json.py`** — скрипт переноса данных из JSON в SQLite:

- собирает уникальные категории из `incomes` и `expenses`;
- вставляет категории в `categories`, строит маппинг `имя → id`;
- вставляет доходы, расходы и бюджеты через `executemany`;
- транзакция: `commit()` при успехе, `rollback()` при ошибке.

**`db/database.py`** — `get_connection()` с `PRAGMA foreign_keys = ON`.

## 6. Получение данных из SQLite в Django

Все view-функции используют **`sqlite3` из стандартной библиотеки** —
**Django ORM не используется**.

Основной порядок:

```python
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row       # доступ по именам полей
rows = conn.execute(sql, params).fetchall()
conn.close()
```

- **`row_factory = sqlite3.Row`** — доступ к полям по именам (`row["name"]`),
  а не по индексам (`row[0]`);
- **параметризованные запросы** (`?`) — значения передаются отдельно
  от SQL-текста, **без f-строк и конкатенации**.

**Пример из `incomes/views.py`:**

```python
income = conn.execute("""
    SELECT i.id, i.amount, i.date,
           c.name AS category_name
    FROM incomes i
    JOIN categories c ON i.category_id = c.id
    WHERE i.id = ?
""", (income_id,)).fetchone()
```

## 7. Страницы, использующие данные из SQLite

| URL | Что показывает | Ключевые SQL-приёмы |
|---|---|---|
| `/incomes/` | Список доходов | `JOIN` |
| `/incomes/<int:id>/` | Карточка дохода | `JOIN` + `WHERE` + параметр |
| `/incomes/filter/` | Поиск доходов по датам | `BETWEEN` + 2 параметра |
| `/incomes/statistics/` | Статистика доходов по категориям | `GROUP BY` + `SUM` + `COUNT` |
| `/expenses/` | Список расходов | `JOIN` |
| `/expenses/<int:id>/` | Карточка расхода | `JOIN` + `WHERE` + параметр |
| `/expenses/filter/` | Поиск расходов по датам | `BETWEEN` + 2 параметра |
| `/expenses/statistics/` | Статистика расходов по категориям | `GROUP BY` + `SUM` + `COUNT` |
| `/budgets/` | Список бюджетов | вычисляемые поля `remaining`, `is_overspent` |
| `/budgets/<int:id>/` | Бюджет + калькулятор `?planned=X` | вычисляемые поля + GET-параметр |

## 8. Веб-интерфейс (Django Template Language)

Используется **система шаблонов Django**:

- **базовый шаблон** `templates/base.html` с блоками `{% block title %}`
  и `{% block content %}`;
- **наследование** через `{% extends "base.html" %}`;
- **включаемые шаблоны** через `{% include %}` — навигация, карточки;
- **контекст** — данные передаются через `render(request, tpl, context)`;
- **циклы** `{% for %}` и `{% empty %}`, **условия** `{% if %}`;
- **именованные URL** через `{% url %}` с пространствами имён
  (`homepage`, `incomes`, `expenses`, `budgets`);
- **фильтры** — `length`, `default`, `floatformat`.

Функция `page()` из ПР5 удалена — все представления используют `render()`.

## 9. Статические файлы

Каталог `homepage/static/homepage/`:

- `css/style.css` — собственные стили (карточки, бейджи, подвал);
- `js/main.js` — вывод текущего года в подвал;
- `img/logo.svg` — логотип.

Подключение через `{% load static %}` + `{% static %}`.

## 10. Консольная версия (сохранена)

- `main.py` — консольное приложение (ПР3);
- `storage.py` — JSON ↔ объекты;
- `models/` — классы `Income`, `Expense`, `Budget`;
- `utils.py` — безопасный ввод;
- `tests/` — 30 тестов pytest.

**Консольная версия и тесты работают с JSON** — это **предыдущая реализация**
предметной области, сохранена по методичке. Django ORM **не используется** —
это задача следующих ПР.

## 11. Запуск

### Первая установка

```bash
pip install -r requirements.txt

# 1. Создать пустую БД
python -c "import sqlite3; sqlite3.connect('data/finance_planner.sqlite').close()"

# 2. Применить схему
python -c "import sqlite3; conn=sqlite3.connect('data/finance_planner.sqlite'); conn.executescript(open('sql/schema.sql', encoding='utf-8').read()); conn.commit(); conn.close()"

# 3. Импортировать данные из JSON
python -m db.import_json
```

### Веб-версия

```bash
python manage.py runserver
```

Открыть `http://127.0.0.1:8000/`.

### Консольная версия

```bash
python main.py
```

## 12. Тестирование и проверка

```bash
pytest -v
flake8 . --extend-exclude=venv
python manage.py check
```

## 13. Текущее состояние проекта

Реализовано:

- классы предметной области `Income`, `Expense`, `Budget` (ПР3);
- консольный интерфейс, JSON-хранилище, тесты;
- Django-проект, четыре приложения (`homepage`, `incomes`, `expenses`,
  `budgets`);
- **система шаблонов Django** (ПР6);
- **база данных SQLite**: таблицы `categories`, `incomes`, `expenses`,
  `budgets` с PK и FK;
- **SQL-запросы** (`SELECT`, `WHERE`, `JOIN`, агрегаты, `GROUP BY`,
  `HAVING`, параметризованные);
- **поиск** доходов и расходов по диапазону дат;
- **статистика** доходов и расходов по категориям;
- получение данных из SQLite в Django-views;
- навигация со всеми разделами.

**Не реализовано (на следующих ПР):**

- Django ORM и модели Django;
- формы Django;
- аутентификация пользователей;
- операции создания/редактирования через веб-формы.

## 14. Дальнейшее развитие

- переход на Django ORM и модели Django;
- формы создания и редактирования записей;
- аутентификация;
- API.