"""View-функции приложения goals."""

from django.http import HttpResponse

from homepage.views import page
from models.goals import find_goal_by_id
from storage import load_goals

GOALS_FILE = "data/goals.json"


def goals(request):
    """Список целей."""
    goals_list = load_goals(GOALS_FILE)

    if not goals_list:
        content = """
        <h1>Цели</h1>
        <p class="text-muted">Целей пока нет.</p>
        <a href="/" class="btn btn-outline-secondary">На главную</a>
        """
        return HttpResponse(page("Finance Planner — цели", content))

    items = ""
    for g in goals_list:
        progress = g.get_progress()
        status = "достигнута" if g.is_achieved() else "в процессе"
        badge = "bg-success" if g.is_achieved() else "bg-primary"
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/goals/{g.id}/">
                {g.name}: {g.saved:.2f} / {g.target:.2f} руб.
                ({progress:.1f}%)
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Цели</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Finance Planner — цели", content))


def goal_detail(request, goal_id):
    """Страница отдельной цели."""
    goals_list = load_goals(GOALS_FILE)
    goal = find_goal_by_id(goals_list, goal_id)

    if goal is None:
        content = """
        <h1 class="text-danger">Цель не найдена</h1>
        <a href="/goals/" class="btn btn-outline-secondary">
            ← к списку целей
        </a>
        """
        return HttpResponse(
            page("Цель не найдена", content),
            status=404,
        )

    progress = goal.get_progress()
    status = "достигнута" if goal.is_achieved() else "в процессе"
    badge = "bg-success" if goal.is_achieved() else "bg-primary"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{goal.name}</h5>
            <p class="card-text">
                <strong>Цель:</strong> {goal.target:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Накоплено:</strong> {goal.saved:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Прогресс:</strong> {progress:.1f}%
            </p>
            <div class="progress mb-3">
                <div class="progress-bar" role="progressbar"
                     style="width: {progress}%"></div>
            </div>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/goals/" class="btn btn-outline-secondary">
                ← к списку целей
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Цель: {goal.name}", content),
        status=200,
    )
