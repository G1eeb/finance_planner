# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов и расходов, контроля месячного бюджета
и отслеживания финансовых целей.

**Веб-интерфейс:** Django + Django Template Language (DTL).
**Доступ к данным:** Django ORM.
**Админ-панель:** Django Admin с настроенными `ModelAdmin` и inline-формами.

## 1. Назначение проекта

Finance Planner — учебное приложение для управления доходами, расходами
и месячными бюджетами. Проект развивается поэтапно:

- ПР1–ПР3 — предметная область на Python (классы, JSON-хранилище);
- ПР5 — веб-интерфейс на Django (HTML в Python);
- ПР6 — переход на **систему шаблонов Django**;
- ПР7 — **слой реляционной базы данных SQLite** (ручные SQL-запросы);
- ПР9 — переход на **Django ORM** (модели, миграции, перенос данных);
- ПР10 — **настройка Django Admin**, Q-объекты для составных условий,
  **анализ SQL-запросов** через Django Debug Toolbar.

## 2. Используемые технологии

- **Python 3.12**;
- **Django 5.2**;
- **Django ORM** — работа с базой данных через модели;
- **Django Template Language (DTL)**;
- **Django Admin** — административная панель;
- **Django Debug Toolbar** — анализ SQL-запросов (только при `DEBUG=True`);
- **HTML5**, **CSS3**, **JavaScript**;
- **Bootstrap 5** (CDN);
- **SQLite 3** — база данных Django (`db.sqlite3`);
- **Git**, **pytest**, **flake8**.

## 3. Предметная область

Четыре сущности и соответствующие им Django-модели:

| Модель | Приложение | Назначение |
|---|---|---|
| **Category** | `categories` | справочник категорий (уникальные названия) |
| **Income** | `incomes` | доходы |
| **Expense** | `expenses` | расходы |
| **Budget** | `budgets` | месячные бюджеты |

## 4. Модели Django

### 4.1. Модель `Category` (`categories/models.py`)

| Поле | Тип Django | Параметры |
|---|---|---|
| `id` | `BigAutoField` | автоматический PK |
| `name` | `CharField` | `max_length=100`, `unique=True` |

`__str__` возвращает название категории.
`Meta.ordering = ["name"]` — сортировка по алфавиту по умолчанию.

### 4.2. Модель `Income` (`incomes/models.py`)

| Поле | Тип Django | Параметры |
|---|---|---|
| `id` | `BigAutoField` | автоматический PK |
| `amount` | `DecimalField` | `max_digits=12`, `decimal_places=2` |
| `category` | `ForeignKey(Category)` | `on_delete=PROTECT`, `related_name="incomes"` |
| `date` | `DateField` | дата |

`related_name="incomes"` позволяет получать доходы категории через
`category.incomes.all()`.

### 4.3. Модель `Expense` (`expenses/models.py`)

Аналогично `Income`, но `related_name="expenses"`.

### 4.4. Модель `Budget` (`budgets/models.py`)

| Поле | Тип Django | Параметры |
|---|---|---|
| `id` | `BigAutoField` | автоматический PK |
| `month` | `CharField` | `max_length=7`, `unique=True` |
| `monthly_budget` | `DecimalField` | `max_digits=12`, `decimal_places=2` |
| `current_expenses` | `DecimalField` | `max_digits=12`, `decimal_places=2`, `default=0` |

Вычисляемые свойства (`@property`):

- **`remaining`** — остаток бюджета (`monthly_budget - current_expenses`);
- **`is_overspent`** — признак превышения;
- **`can_afford(amount)`** — метод: возможна ли планируемая трата.

## 5. Связи между моделями

- **`Income.category → Category`** — связь «многие к одному»,
  `on_delete=PROTECT`: нельзя удалить категорию, если на неё
  ссылаются доходы.
- **`Expense.category → Category`** — аналогично.
- **`Budget`** — независимая модель, без FK.

## 6. Миграции

Структура базы управляется миграциями Django:

```bash
python manage.py makemigrations   # создать миграции из моделей
python manage.py migrate          # применить к db.sqlite3
```

Файлы миграций (`*/migrations/0001_initial.py`) хранятся в Git.
Применённые миграции видны в `python manage.py showmigrations` (отметка `[X]`).

## 7. Django ORM

Все views получают данные через ORM. Используемые приёмы:

- **`objects.all()`**, **`objects.get()`**, **`get_object_or_404()`** — получение записей;
- **`filter()`**, **`exclude()`** — фильтрация по условиям;
- **`filter(field__icontains=...)`** — поиск по подстроке;
- **`filter(field__gte=...)`**, **`filter(field__lte=...)`**, **`filter(field__range=(a, b))`** — диапазоны;
- **`filter(field__isnull=True)`** — обратная связь + проверка на NULL;
- **`Q(...) | Q(...)`** — составные условия через OR;
- **`order_by()`** — сортировка (один или несколько полей);
- **`select_related("category")`** — JOIN для FK (без N+1);
- **`annotate(F(...))`** — вычисляемые поля;
- **`values().annotate(Sum(...), Count(...))`** — группировка;
- **`aggregate(total=Sum(...), cnt=Count(...))`** — итоги по всей выборке;
- **`Paginator`** — постраничный вывод.

### 7.1. Q-объекты для составных условий

В `incomes/views.py` и `expenses/views.py` реализован **расширенный поиск**
через `Q`:

```python
from django.db.models import Q

qs = qs.filter(
    Q(category__name__icontains=search_q)
    | Q(amount__gte=Q_AMOUNT_THRESHOLD)
)
```

Это позволяет искать записи, где **категория содержит подстроку**
**ИЛИ** сумма больше порога (50 000). В SQL это транслируется в `WHERE ... OR ...`.

## 8. Django Admin

Административная панель доступна по адресу `/admin/`. Для входа
используется суперпользователь (`python manage.py createsuperuser`).

### 8.1. Зарегистрированные модели

В админке доступны все четыре модели:

- **`Category`** — `categories/admin.py`;
- **`Income`** — `incomes/admin.py`;
- **`Expense`** — `expenses/admin.py`;
- **`Budget`** — `budgets/admin.py`.

### 8.2. Настройки `ModelAdmin`

Для каждой модели настроены:

| Модель | `list_display` | `list_filter` | `search_fields` | Особенности |
|---|---|---|---|---|
| `Category` | `id`, `name` | — | `name` | Inline для `Income` и `Expense` |
| `Income` | `id`, `amount`, `category`, `date` | `category`, `date` | `category__name` | `date_hierarchy`, `list_select_related` |
| `Expense` | `id`, `amount`, `category`, `date` | `category`, `date` | `category__name` | `date_hierarchy`, `list_select_related` |
| `Budget` | `id`, `month`, `monthly_budget`, `current_expenses`, `remaining_display`, `is_overspent_display` | `month` | `month` | Вычисляемые столбцы через `@admin.display` |

### 8.3. Inline в карточке категории

В `CategoryAdmin` добавлены два `TabularInline`:

- **`IncomeInline`** — доходы категории (`amount`, `date`);
- **`ExpenseInline`** — расходы категории (`amount`, `date`).

Inline'ы работают в режиме **только для чтения** (`readonly_fields`,
`can_delete=False`, `extra=0`). Редактирование — через ссылку «Изменить»,
которая открывает полную форму записи. Это соответствует принципу
методички: административная панель не заменяет бизнес-логику.

### 8.4. Локализация

Все модели снабжены `verbose_name` и `verbose_name_plural` в `Meta`.
В `settings.py` установлено `LANGUAGE_CODE = "ru-ru"`. Названия
приложений в админке — на русском.

## 9. Производительность и анализ SQL-запросов

Для анализа SQL-запросов установлен **Django Debug Toolbar**
(`django-debug-toolbar>=8.0`). Подключение:

- **`INSTALLED_APPS`** — `debug_toolbar`;
- **`MIDDLEWARE`** — `DebugToolbarMiddleware` (первой строкой);
- **`INTERNAL_IPS = ["127.0.0.1", "localhost"]`** в `settings.py`;
- **`urls.py`** — маршрут `__debug__/` под `if settings.DEBUG:`;
- **`requirements.txt`** — `django-debug-toolbar>=8.0`.

### 9.1. Результаты анализа

| Страница | Запросов к БД | JOIN с категориями | N+1 |
|---|---|---|---|
| `/` | 0 | — | нет |
| `/incomes/` | 4 | есть (`select_related`) | нет |
| `/incomes/1/` | 1 | есть | нет |
| `/incomes/?q=зар` | 4 | есть | нет |
| `/incomes/filter/` (без дат) | 0 | — | нет |
| `/incomes/statistics/` | 2 | есть (`values` + `F`) | нет |
| `/expenses/` | 4 | есть | нет |
| `/expenses/1/` | 1 | есть | нет |
| `/budgets/` | 1 | — (FK нет) | нет |
| `/budgets/1/` | 1 | — | нет |
| `/budgets/1/?planned=5000` | 3 | — | нет |
| `/incomes/999/` (404) | 1 | — | нет |

**Вывод: N+1 не обнаружен.** Везде, где выполняется обращение
к связанной модели `Category`, применяется `select_related("category")` —
это подтверждается наличием `INNER JOIN categories_category` в SQL
и количеством запросов (1 вместо 1 + N).

### 9.2. Использованные оптимизации

- **`select_related("category")`** в списках и карточках доходов/расходов —
  один запрос с `INNER JOIN` вместо N+1.
- **`values(category_name=F("category__name")).annotate(...)`** в статистике —
  один запрос с `JOIN` и `GROUP BY`.
- **`aggregate(total=Sum(...), cnt=Count(...))`** — один запрос для итогов
  вместо перебора всех записей в Python.
- **`Paginator`** — отдельный `COUNT(*)` только когда нужен номер страницы.
- **`list_select_related = ("category",)`** в `IncomeAdmin` и `ExpenseAdmin` —
  оптимизация админского списка (1 запрос на страницу вместо N+1).

## 10. Страницы проекта

| URL | Что показывает |
|---|---|
| `/` | Главная с навигацией |
| `/incomes/` | Список доходов + фильтры, сортировка, пагинация, расширенный поиск (Q) |
| `/incomes/<int:id>/` | Карточка дохода |
| `/incomes/filter/` | Поиск по датам |
| `/incomes/statistics/` | Статистика по категориям |
| `/expenses/` | Список расходов + фильтры, сортировка, пагинация, расширенный поиск (Q) |
| `/expenses/<int:id>/` | Карточка расхода |
| `/expenses/filter/` | Поиск по датам |
| `/expenses/statistics/` | Статистика по категориям |
| `/budgets/` | Список бюджетов |
| `/budgets/<int:id>/` | Бюджет + калькулятор `?planned=X` |
| `/admin/` | Административная панель Django |

**Фильтры в списках** (`?q=`, `?search_q=`, `?category=`, `?exclude_category=`,
`?amount_min=`, `?amount_max=`) и **сортировка** (`?sort=`) — через GET-параметры.
**Пагинация** — 5 записей на страницу, параметры сохраняются при переходе.

## 11. Веб-интерфейс (Django Template Language)

- **базовый шаблон** `templates/base.html` с блоками `{% block title %}`
  и `{% block content %}`;
- **наследование** через `{% extends "base.html" %}`;
- **включаемые шаблоны** через `{% include %}` — навигация, карточки;
- **контекст** — данные через `render(request, tpl, context)`;
- **циклы** `{% for %}` и `{% empty %}`, **условия** `{% if %}`;
- **именованные URL** через `{% url %}` с `app_name`
  (`homepage`, `incomes`, `expenses`, `budgets`);
- **фильтры** — `length`, `default`, `floatformat`, `date`, `stringformat`.

## 12. Статические файлы

Каталог `homepage/static/homepage/`:

- `css/style.css` — собственные стили;
- `js/main.js` — вывод текущего года в подвал;
- `img/logo.svg` — логотип.

Подключение через `{% load static %}` + `{% static %}`.

## 13. Консольная версия (сохранена)

- `main.py` — консольное приложение (ПР3);
- `storage.py` — JSON ↔ объекты;
- `models/` — Python-классы `Income`, `Expense`, `Budget` (не Django-модели);
- `utils.py` — безопасный ввод;
- `tests/` — тесты pytest.

**Консольная версия и тесты работают с JSON** — это предыдущая реализация
предметной области. Django ORM в ней не используется.

## 14. Структура проекта

```
finance_planner/
├── manage.py
├── db.sqlite3                          ← база данных Django (в .gitignore)
├── requirements.txt
├── README.md
├── .flake8
├── .gitignore
├── finance_planner_django/
│   ├── settings.py                     ← INSTALLED_APPS, MIDDLEWARE, INTERNAL_IPS
│   └── urls.py                         ← admin, include, __debug__
├── templates/
│   ├── base.html
│   ├── 404.html
│   └── includes/navigation.html
├── homepage/
│   ├── static/homepage/                ← css, js, img
│   ├── templates/homepage/index.html
│   ├── views.py
│   └── urls.py
├── categories/
│   ├── admin.py                        ← CategoryAdmin + Inline
│   ├── migrations/0001_initial.py
│   └── models.py
├── incomes/
│   ├── admin.py                        ← IncomeAdmin
│   ├── migrations/0001_initial.py
│   ├── models.py
│   ├── templates/incomes/
│   └── views.py                        ← ORM + Q-объекты
├── expenses/
│   ├── admin.py                        ← ExpenseAdmin
│   ├── migrations/0001_initial.py
│   ├── models.py
│   ├── templates/expenses/
│   └── views.py                        ← ORM + Q-объекты
├── budgets/
│   ├── admin.py                        ← BudgetAdmin
│   ├── migrations/0001_initial.py
│   ├── models.py
│   ├── templates/budgets/
│   └── views.py
├── models/                             ← Python-классы ПР3 (JSON-реализация)
│   ├── incomes.py
│   ├── expenses.py
│   └── budgets.py
├── data/                               ← JSON + старая SQLite (ПР7)
│   ├── incomes.json
│   ├── expenses.json
│   ├── budgets.json
│   └── finance_planner.sqlite          ← источник для импорта, в .gitignore
├── sql/                                ← ПР7 (сохранено как предыдущая реализация)
│   ├── schema.sql
│   └── queries.sql
├── db/
│   ├── database.py                     ← ПР7
│   ├── import_json.py                  ← ПР7
│   ├── inspect_source_db.py            ← ПР9
│   └── import_sqlite_to_orm.py         ← ПР9
├── tests/
└── main.py                             ← консольная версия (ПР3)
```

## 15. Запуск проекта

### Первая установка

```bash
pip install -r requirements.txt

# 1. Применить миграции Django (создаст таблицы моделей в db.sqlite3)
python manage.py migrate

# 2. Создать суперпользователя для входа в админку
python manage.py createsuperuser

# 3. (Опционально) перенести данные из базы ПР7
python db/import_sqlite_to_orm.py
```

### Веб-версия

```bash
python manage.py runserver
```

- Приложение: `http://127.0.0.1:8000/`
- Админка: `http://127.0.0.1:8000/admin/`

### Консольная версия

```bash
python main.py
```

## 16. Тестирование и проверка

```bash
python manage.py check             # проверка конфигурации
python manage.py showmigrations    # состояние миграций
pytest -v                          # 30 тестов предметной области
flake8 . --extend-exclude=venv     # проверка стиля
```

## 17. Текущее состояние проекта

Реализовано:

- Python-классы предметной области `Income`, `Expense`, `Budget` (ПР3);
- консольный интерфейс, JSON-хранилище, тесты;
- Django-проект с приложениями `homepage`, `categories`, `incomes`,
  `expenses`, `budgets`;
- система шаблонов Django (ПР6);
- база данных SQLite через ручные SQL-запросы (ПР7, сохранена как
  предыдущая реализация);
- **Django ORM** (ПР9):
  - модели `Category`, `Income`, `Expense`, `Budget` с полями и связями;
  - миграции;
  - перенос данных из базы ПР7;
  - все views используют ORM;
- **фильтрация**, **сортировка**, **пагинация**, **агрегаты**
  (`Sum`, `Count`), **поиск по строке** (`icontains`),
  **исключение** (`exclude`), **обратная связь** (`isnull`);
- **Django Admin** (ПР10):
  - регистрация всех четырёх моделей;
  - настройка `list_display`, `list_filter`, `search_fields`, `ordering`,
    `date_hierarchy`, `list_select_related`;
  - Inline для доходов и расходов в карточке категории;
  - вычисляемые столбцы в `BudgetAdmin`;
  - локализация на русском;
- **Q-объекты** для расширенного поиска (OR) в доходах и расходах;
- **Django Debug Toolbar** установлен, SQL-запросы проанализированы,
  N+1 не обнаружен, результаты зафиксированы в README;
- навигация со всеми разделами.

**Не реализовано (на следующих ПР):**

- формы Django (создание/редактирование через собственные веб-формы);
- аутентификация пользователей (кроме стандартной для админки);
- API.

## 18. Дальнейшее развитие

- формы Django для создания и редактирования записей из публичной части;
- регистрация и вход пользователей;
- REST API (Django REST Framework);
- тесты для views и шаблонов;
- CI/CD.