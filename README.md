# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов и расходов, контроля месячного бюджета
и отслеживания финансовых целей.

На ПР5 проект получил **веб-интерфейс на Django**. Консольная версия ПР3
сохранена и продолжает работать параллельно.

## Предметная область

Основные сущности:

- **Transaction** — операция (доход или расход);
- **Goal** — финансовая цель.

Бюджет — разовый калькулятор, реализован набором функций.

## Используемый фреймворк

- **Django 5.2** — веб-фреймворк;
- **Bootstrap 5.3** — CSS-фреймворк для вёрстки (подключён через CDN).

## Классы предметной области (из ПР3)

### `Transaction` — операция

Атрибуты: `id`, `type`, `amount`, `category`, `date`.

Методы: `is_income()`, `is_expense()`, `from_dict()`, `to_dict()`,
`__str__()`.

### `Goal` — финансовая цель

Атрибуты: `id`, `name`, `target`, `saved`.

Методы: `add_to_goal()`, `get_progress()`, `is_achieved()`,
`from_dict()`, `to_dict()`, `__str__()`.

Классы размещены в пакете `models/` и используются **и веб-версией, и консольной**.

## Страницы веб-интерфейса

| URL | View-функция | Назначение |
|---|---|---|
| `/` | `homepage.views.index` | Главная страница с навигацией |
| `/transactions/` | `transactions.views.transactions` | Список операций |
| `/transactions/<int:transaction_id>/` | `transactions.views.transaction_detail` | Карточка операции |
| `/goals/` | `goals.views.goals` | Список целей |
| `/goals/<int:goal_id>/` | `goals.views.goal_detail` | Карточка цели |
| `/budget/` | `homepage.views.budget_check` | Разовый калькулятор бюджета |
| `/admin/` | `django.contrib.admin` | Админ-панель Django |

**Обработка ошибок:**
- при несуществующем ID операции/цели — страница с сообщением, код 404;
- для несуществующих URL — кастомная страница 404 (`homepage.views.page_not_found`).

## Как устроена навигация

Все страницы используют общий каркас — функция `page()` в `homepage/views.py`.
Она собирает HTML-документ:
- кодировка UTF-8, viewport;
- заголовок вкладки;
- подключение Bootstrap 5.3 через CDN;
- верхняя навигация (главная, операции, цели, бюджет).

Каждая view-функция формирует только **содержимое** страницы и передаёт его
в `page()`.

## Данные

Данные хранятся в JSON-файлах:
- `data/transactions.json` — операции;
- `data/goals.json` — цели.

При загрузке JSON → объекты `Transaction` и `Goal` (через `from_dict`).
При сохранении объекты → JSON (через `to_dict`).

**Загрузка и сохранение выполняются функциями ПР3** — модуль `storage.py`.
Веб-слой использует:
- `load_transactions()`, `load_goals()`;
- `find_transaction_by_id()`, `find_goal_by_id()`;
- `calculate_budget()`, `check_budget()`.

**На ПР5 Django ORM и база данных не используются** — источник данных остаётся JSON.
Перенос сущностей в Django ORM — на следующих практических работах.

## Структура проекта

    finance_planner/
    ├── manage.py                       — точка входа Django
    ├── finance_planner_django/         — пакет настроек Django
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py                     — корневая маршрутизация + handler404
    │   ├── asgi.py
    │   └── wsgi.py
    ├── homepage/                       — Django-приложение (главная, бюджет, 404)
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py                   — пусто (ORM позже)
    │   ├── tests.py
    │   ├── urls.py                     — маршруты приложения
    │   └── views.py                    — page(), index(), budget_check(), page_not_found()
    ├── transactions/                   — Django-приложение (операции)
    │   ├── ... (аналогично)
    │   ├── urls.py
    │   └── views.py                    — transactions(), transaction_detail()
    ├── goals/                          — Django-приложение (цели)
    │   ├── ... (аналогично)
    │   ├── urls.py
    │   └── views.py                    — goals(), goal_detail()
    ├── models/                         — пакет классов предметной области (ПР3)
    │   ├── __init__.py
    │   ├── transactions.py
    │   └── goals.py
    ├── data/                           — JSON-файлы данных
    │   ├── transactions.json
    │   └── goals.json
    ├── tests/                          — тесты pytest (ПР3)
    │   ├── test_budget.py
    │   ├── test_transactions.py
    │   └── test_goals.py
    ├── main.py                         — консольная версия (ПР3)
    ├── budget.py                       — функции расчёта бюджета
    ├── storage.py                      — JSON ↔ объекты
    ├── utils.py                        — безопасный ввод
    ├── conftest.py
    ├── requirements.txt                — Django, pytest, flake8
    ├── .flake8
    ├── .gitignore
    └── README.md

## Назначение модулей

- **`main.py`** — консольная версия приложения (сохранена с ПР3);
- **`finance_planner_django/`** — настройки Django-проекта;
- **`homepage/`** — главная страница, страница бюджета, обработчик 404;
- **`transactions/`** — страницы операций;
- **`goals/`** — страницы целей;
- **`models/`** — классы предметной области (ПР3);
- **`storage.py`** — загрузка/сохранение JSON;
- **`budget.py`** — расчёт бюджета (ПР1);
- **`utils.py`** — безопасный ввод;
- **`tests/`** — автоматизированные тесты.

## Запуск

### Веб-версия (Django)

    python manage.py migrate        # первый раз — служебные таблицы
    python manage.py runserver

Открыть в браузере: `http://127.0.0.1:8000/`

### Консольная версия

    python main.py

## Тестирование

    pytest -v

Автоматизированные тесты ПР3 продолжают проходить — функциональность
консольной версии не изменилась.

## Проверка качества кода

    flake8 .

## Зависимости

Состав `requirements.txt`:

- `Django==5.2.*` — веб-фреймворк;
- `pytest>=8.0` — тесты;
- `flake8>=7.0` — проверка качества кода.

Установка:

    pip install -r requirements.txt

## Текущее состояние

**Реализовано на ПР5:**
- Django-проект и три Django-приложения (`homepage`, `transactions`, `goals`);
- двухуровневая маршрутизация URL;
- view-функции для всех страниц;
- общий HTML-каркас страницы через функцию `page()`;
- страницы: главная, операции (список + карточка), цели (список + карточка);
- отображение данных предметной области из JSON;
- навигация между страницами;
- оформление Bootstrap 5.3;
- кастомная страница 404;
- разовый калькулятор бюджета через GET-параметры.

**Планируется (следующие ПР):**
- перенос сущностей `Transaction` и `Goal` в Django ORM;
- подключение базы данных;
- переход на Django-шаблоны (`templates/`, `render()`, `base.html`);
- формы создания и редактирования операций и целей (POST-запросы);
- аутентификация пользователей.