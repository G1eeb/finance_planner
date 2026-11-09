# Finance Planner — сервис финансового планирования

Приложение для учёта личных доходов и расходов, контроля месячного бюджета
и отслеживания финансовых целей.

**Веб-интерфейс:** Django + Django Template Language (DTL).
**Доступ к данным:** Django ORM (с ПР9). Ранее использовались
JSON (ПР1–ПР3) и SQLite через `sqlite3` (ПР7) — сохранены как
предыдущие реализации.

## 1. Назначение проекта

Finance Planner — учебное приложение для управления доходами, расходами
и месячными бюджетами. Проект развивается поэтапно:

- ПР1–ПР3 — предметная область на Python (классы, JSON-хранилище);
- ПР5 — веб-интерфейс на Django (HTML в Python);
- ПР6 — переход на **систему шаблонов Django**;
- ПР7 — **слой реляционной базы данных SQLite** (ручные SQL-запросы);
- ПР9 — переход на **Django ORM** (модели, миграции, перенос данных).

## 2. Используемые технологии

- **Python 3**;
- **Django 5**;
- **Django ORM** — работа с базой данных через модели;
- **Django Template Language (DTL)**;
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

Метод `__str__` возвращает название категории.
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