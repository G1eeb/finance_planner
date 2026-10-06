# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов, расходов и контроля месячного бюджета.

На ПР5 проект получил **веб-интерфейс на Django**. Консольная версия сохранена
и продолжает работать параллельно.

## Предметная область

Основные сущности:

- **Income** — доход (поступление денежных средств);
- **Expense** — расход (списание денежных средств);
- **Budget** — месячный бюджет.

## Используемый фреймворк

- **Django 5.2** — веб-фреймворк;
- **Bootstrap 5.3** — CSS-фреймворк для вёрстки (подключён через CDN).

## Классы предметной области (из ПР3)

### `Income` — доход

Атрибуты: `id`, `amount`, `category`, `date`.

Методы: `validate_amount()`, `from_dict()`, `to_dict()`, `__str__()`.

### `Expense` — расход

Атрибуты: `id`, `amount`, `category`, `date`.

Методы: `validate_amount()`, `from_dict()`, `to_dict()`, `__str__()`.

### `Budget` — месячный бюджет

Атрибуты: `id`, `month`, `monthly_budget`, `current_expenses`.

Методы: `get_remaining()`, `get_remaining_after()`, `can_afford()`,
`validate_budget()`, `from_dict()`, `to_dict()`, `__str__()`.

Классы размещены в пакете `models/` и используются **и веб-версией,
и консольной**.

## Страницы веб-интерфейса

| URL | View-функция | Назначение |
|---|---|---|
| `/` | `homepage.views.index` | Главная страница с навигацией |
| `/incomes/` | `incomes.views.incomes` | Список доходов |
| `/incomes/<int:income_id>/` | `incomes.views.income_detail` | Карточка дохода |
| `/expenses/` | `expenses.views.expenses` | Список расходов |
| `/expenses/<int:expense_id>/` | `expenses.views.expense_detail` | Карточка расхода |
| `/budgets/` | `budgets.views.budgets` | Список бюджетов |
| `/budgets/<int:budget_id>/` | `budgets.views.budget_detail` | Карточка бюджета + калькулятор |
| `/admin/` | `django.contrib.admin` | Админ-панель Django |

**Обработка ошибок:**
- при несуществующем ID — страница с сообщением, код 404;
- для несуществующих URL — кастомная страница 404
  (`homepage.views.page_not_found`).

**Разовый калькулятор бюджета** доступен на странице бюджета
через GET-параметр: `/budgets/1/?planned=15000`.

## Как устроена навигация

Все страницы используют общий каркас — функция `page()`
в `homepage/views.py`. Она собирает HTML-документ:
- кодировка UTF-8, viewport;
- заголовок вкладки;
- подключение Bootstrap 5.3 через CDN;
- верхняя навигация (главная, доходы, расходы, бюджеты).

Каждая view-функция формирует только **содержимое** страницы
и передаёт его в `page()`.

## Данные

Данные хранятся в JSON-файлах:
- `data/incomes.json` — доходы;
- `data/expenses.json` — расходы;
- `data/budgets.json` — бюджеты.

При загрузке JSON → объекты `Income`, `Expense`, `Budget`
(через `from_dict`). При сохранении объекты → JSON (через `to_dict`).

**Загрузка и сохранение выполняются функциями модуля `storage.py`**:
- `load_incomes()` / `save_incomes()`;
- `load_expenses()` / `save_expenses()`;
- `load_budgets()` / `save_budgets()`.

**На ПР5 Django ORM и база данных не используются** — источник данных
остаётся JSON. Перенос сущностей в Django ORM — на следующих работах.

## Структура проекта

    finance_planner/
    ├── manage.py                       — точка входа Django
    ├── finance_planner_django/         — пакет настроек Django
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py                     — корневая маршрутизация + handler404
    │   ├── asgi.py
    │   └── wsgi.py
    ├── homepage/                       — Django-приложение
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py                   — пусто (ORM позже)
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py                    — page(), index(), page_not_found()
    ├── incomes/                        — Django-приложение (доходы)
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py                   — пусто
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py                    — incomes(), income_detail()
    ├── expenses/                       — Django-приложение (расходы)
    │   ├── ... (аналогично)
    │   ├── urls.py
    │   └── views.py                    — expenses(), expense_detail()
    ├── budgets/                        — Django-приложение (бюджеты)
    │   ├── ... (аналогично)
    │   ├── urls.py
    │   └── views.py                    — budgets(), budget_detail()
    ├── models/                         — пакет классов предметной области
    │   ├── __init__.py
    │   ├── incomes.py                  — класс Income + функции
    │   ├── expenses.py                 — класс Expense + функции
    │   └── budgets.py                  — класс Budget + функции
    ├── data/                           — JSON-файлы данных
    │   ├── .gitkeep
    │   ├── incomes.json
    │   ├── expenses.json
    │   └── budgets.json
    ├── tests/                          — автоматизированные тесты pytest
    │   ├── test_incomes.py
    │   ├── test_expenses.py
    │   └── test_budgets.py
    ├── main.py                         — консольная версия
    ├── storage.py                      — JSON ↔ объекты
    ├── utils.py                        — безопасный ввод
    ├── conftest.py
    ├── requirements.txt                — Django, pytest, flake8
    ├── .flake8
    ├── .gitignore
    └── README.md

## Запуск

### Веб-версия (Django)

    python manage.py migrate        # первый раз — служебные таблицы
    python manage.py runserver

Открыть в браузере: `http://127.0.0.1:8000/`

### Консольная версия

    python main.py

## Тестирование

    pytest -v

Автоматизированные тесты продолжают проходить — функциональность
консольной версии сохранена.

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
- Django-проект и четыре Django-приложения
  (`homepage`, `incomes`, `expenses`, `budgets`);
- двухуровневая маршрутизация URL;
- view-функции для всех страниц;
- общий HTML-каркас страницы через функцию `page()`;
- страницы: главная, списки и карточки доходов, расходов, бюджетов;
- отображение данных предметной области из JSON;
- навигация между страницами;
- оформление Bootstrap 5.3;
- кастомная страница 404;
- разовый калькулятор бюджета через GET-параметры.

**Планируется (следующие ПР):**
- перенос сущностей `Income`, `Expense`, `Budget` в Django ORM;
- подключение базы данных;
- переход на Django-шаблоны (`templates/`, `render()`, `base.html`);
- формы создания и редактирования (POST-запросы);
- аутентификация пользователей.