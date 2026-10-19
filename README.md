# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов и расходов, контроля месячного бюджета
и отслеживания финансовых целей.

**Веб-интерфейс реализован на Django с использованием системы шаблонов
Django Template Language (DTL).**

## 1. Назначение проекта

Finance Planner — учебное приложение для управления доходами, расходами
и месячными бюджетами. Проект развивается поэтапно:

- ПР1–ПР3 — предметная область на Python (классы, JSON-хранилище);
- ПР5 — веб-интерфейс на Django (HTML формировался в Python);
- ПР6 — переход на **систему шаблонов Django**.

## 2. Используемые технологии

- **Python 3**;
- **Django 5**;
- **Django Template Language (DTL)**;
- **HTML5**, **CSS3**, **JavaScript**;
- **Bootstrap 5** (CDN);
- **JSON** — источник данных;
- **Git**;
- **pytest**, **flake8**.

## 3. Предметная область

Три основные сущности:

- **Income** — доход (`id`, `amount`, `category`, `date`);
- **Expense** — расход (`id`, `amount`, `category`, `date`);
- **Budget** — месячный бюджет (`id`, `month`, `monthly_budget`,
  `current_expenses`).

Для предметной области реализованы собственные Python-классы в пакете `models/`.

**На текущем этапе данные хранятся в JSON-файлах. Django ORM
и база данных приложения пока не используются.**

## 4. Структура проекта
# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов и расходов, контроля месячного бюджета
и отслеживания финансовых целей.

**Веб-интерфейс реализован на Django с использованием системы шаблонов
Django Template Language (DTL).**

## 1. Назначение проекта

Finance Planner — учебное приложение для управления доходами, расходами
и месячными бюджетами. Проект развивается поэтапно:

- ПР1–ПР3 — предметная область на Python (классы, JSON-хранилище);
- ПР5 — веб-интерфейс на Django (HTML формировался в Python);
- ПР6 — переход на **систему шаблонов Django**.

## 2. Используемые технологии

- **Python 3**;
- **Django 5**;
- **Django Template Language (DTL)**;
- **HTML5**, **CSS3**, **JavaScript**;
- **Bootstrap 5** (CDN);
- **JSON** — источник данных;
- **Git**;
- **pytest**, **flake8**.

## 3. Предметная область

Три основные сущности:

- **Income** — доход (`id`, `amount`, `category`, `date`);
- **Expense** — расход (`id`, `amount`, `category`, `date`);
- **Budget** — месячный бюджет (`id`, `month`, `monthly_budget`,
  `current_expenses`).

Для предметной области реализованы собственные Python-классы в пакете `models/`.

**На текущем этапе данные хранятся в JSON-файлах. Django ORM
и база данных приложения пока не используются.**

## 4. Структура проекта

```
finance_planner/
├── manage.py
├── requirements.txt
├── README.md
├── .flake8
├── .gitignore
├── finance_planner_django/         — пакет настроек Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/                      — шаблоны уровня проекта
│   ├── base.html
│   ├── 404.html
│   └── includes/
│       └── navigation.html
├── homepage/                       — Django-приложение (главная, 404)
│   ├── templates/homepage/index.html
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.svg
│   ├── views.py
│   └── urls.py
├── incomes/                        — Django-приложение (доходы)
│   ├── templates/incomes/
│   │   ├── income_list.html
│   │   ├── income_detail.html
│   │   └── includes/income_card.html
│   ├── views.py
│   └── urls.py
├── expenses/                       — Django-приложение (расходы)
│   ├── templates/expenses/
│   │   ├── expense_list.html
│   │   ├── expense_detail.html
│   │   └── includes/expense_card.html
│   ├── views.py
│   └── urls.py
├── budgets/                        — Django-приложение (бюджеты)
│   ├── templates/budgets/
│   │   ├── budget_list.html
│   │   ├── budget_detail.html
│   │   └── includes/budget_status.html
│   ├── views.py
│   └── urls.py
├── models/                         — классы предметной области (ПР3)
│   ├── __init__.py
│   ├── incomes.py
│   ├── expenses.py
│   └── budgets.py
├── data/                           — JSON-файлы данных
│   ├── incomes.json
│   ├── expenses.json
│   └── budgets.json
├── tests/                          — тесты pytest
│   ├── test_incomes.py
│   ├── test_expenses.py
│   └── test_budgets.py
├── main.py                         — консольная версия (ПР3)
├── storage.py                      — JSON ↔ объекты
├── utils.py                        — безопасный ввод
└── conftest.py
```

## 5. Веб-интерфейс

Основные страницы:

| URL | View-функция | Что показывает |
|---|---|---|
| `/` | `homepage.views.index` | Главная с навигацией |
| `/incomes/` | `incomes.views.incomes` | Список доходов |
| `/incomes/<int:income_id>/` | `incomes.views.income_detail` | Карточка дохода |
| `/expenses/` | `expenses.views.expenses` | Список расходов |
| `/expenses/<int:expense_id>/` | `expenses.views.expense_detail` | Карточка расхода |
| `/budgets/` | `budgets.views.budgets` | Список бюджетов |
| `/budgets/<int:budget_id>/` | `budgets.views.budget_detail` | Карточка бюджета + калькулятор (`?planned=X`) |

**HTML формируется шаблонами.** Генерация HTML в Python-коде **не используется**.
Функция `page()` удалена полностью.

## 6. Django Template Language

### 6.1. Базовый шаблон

Общий шаблон: `templates/base.html`. Содержит:

- общую HTML-структуру;
- подключение Bootstrap и **собственного CSS**;
- логотип через `{% static %}`;
- навигацию через `{% include %}`;
- подвал с годом (выводится через JavaScript);
- блоки `{% block title %}` и `{% block content %}`.

Дочерние шаблоны используют наследование:

```django
{% extends "base.html" %}
```

Заголовок и содержимое переопределяются:

```django
{% block title %}…{% endblock %}
{% block content %}…{% endblock %}
```

### 6.2. Включаемые шаблоны

Повторяющиеся фрагменты вынесены в отдельные файлы:

- `includes/navigation.html` — навигация;
- `incomes/includes/income_card.html` — карточка дохода;
- `expenses/includes/expense_card.html` — карточка расхода;
- `budgets/includes/budget_status.html` — статус бюджета.

Подключение:

```django
{% include "incomes/includes/income_card.html" %}
```

### 6.3. Контекст

View-функции передают данные в шаблоны через словарь:

```python
context = {"incomes": incomes_list}
return render(request, "incomes/income_list.html", context)
```

В шаблоне данные доступны по имени:

```django
{% for income in incomes %}
```

### 6.4. Циклы и условия

```django
{% for income in incomes %}
    …
{% empty %}
    <p>Доходов пока нет.</p>
{% endfor %}
```

Условия — для статуса бюджета и обработки 404:

```django
{% if budget.is_achieved %}
    Достигнут
{% else %}
    В процессе
{% endif %}
```

### 6.5. Фильтры шаблонов

- `{{ incomes|length }}` — количество элементов;
- `{{ income.category|default:"Без категории" }}` — значение по умолчанию;
- `{{ income.amount|floatformat:2 }}` — число с 2 знаками.

Фильтры используются **только для представления**, не для бизнес-логики.

## 7. Именованные URL и пространства имён

В каждом `urls.py` объявлено:

```python
app_name = "incomes"
```

Имена маршрутов: `list`, `detail`. Ссылки в шаблонах:

```django
{% url 'incomes:list' %}
{% url 'incomes:detail' income.id %}
```

Пространства имён: `homepage`, `incomes`, `expenses`, `budgets`.

## 8. Статические файлы

Каталог: `homepage/static/homepage/`.

| Ресурс | Путь | Где используется |
|---|---|---|
| CSS | `css/style.css` | `base.html`, карточки, статус |
| JS | `js/main.js` | `base.html` (год в подвале) |
| Логотип | `img/logo.svg` | `base.html` |

Подключение через:

```django
{% load static %}
{% static 'homepage/css/style.css' %}
```

Собственный CSS оформляет карточки доходов, расходов, бюджетов
и бейджи статусов. JavaScript выводит текущий год в подвал.

## 9. Хранение данных

На текущем этапе данные хранятся в JSON-файлах:

- `data/incomes.json`;
- `data/expenses.json`;
- `data/budgets.json`.

Загрузка — через `storage.py`. Классы предметной области — в `models/`.

**Django ORM и база данных пока не используются** — это задача следующих ПР.

## 10. Основные модули

- **`storage.py`** — загрузка данных из JSON;
- **`models/`** — классы `Income`, `Expense`, `Budget`;
- **`main.py`** — консольная версия приложения (сохранена с ПР3);
- **`utils.py`** — вспомогательные функции ввода;
- **`incomes/views.py`, `expenses/views.py`, `budgets/views.py`,
  `homepage/views.py`** — view-функции на `render()`.

## 11. Тестирование

Тесты в каталоге `tests/`:

- `test_incomes.py`;
- `test_expenses.py`;
- `test_budgets.py`.

Запуск:

```bash
pytest -v
```

## 12. Проверка качества кода

```bash
flake8 . --extend-exclude=venv
```

## 13. Запуск проекта

```bash
python manage.py runserver
```

Веб-интерфейс: `http://127.0.0.1:8000/`.

## 14. Git

Каждый этап фиксируется отдельным коммитом с префиксом практической работы:

```bash
git add .
git commit -m "PR6: …"
```

## 15. Текущее состояние проекта

Реализовано:

- классы предметной области `Income`, `Expense`, `Budget` (ПР3);
- консольный интерфейс;
- JSON-хранилище;
- Django-проект и четыре Django-приложения;
- веб-представления для основных сущностей;
- **Django Template Language**;
- наследование шаблонов;
- базовый шаблон `base.html`;
- блоки `block`;
- включаемые шаблоны `include`;
- передача данных через контекст;
- циклы и условия;
- фильтры шаблонов;
- именованные URL и пространства имён;
- статические файлы (CSS, JS, логотип);
- собственное оформление интерфейса;
- тесты предметной области.

**Не реализовано (на следующих ПР):**

- Django ORM и модели Django;
- формы Django;
- работа с базой данных;
- операции создания/редактирования/удаления через веб-формы;
- аутентификация пользователей.

## 16. Дальнейшее развитие

- переход от JSON к базе данных и Django ORM;
- формы Django для создания и редактирования;
- валидация пользовательского ввода;
- API.