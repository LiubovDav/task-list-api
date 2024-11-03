from flask import Blueprint, request, Response, make_response, abort
from app.models.task import Task
from ..db import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks" )

@task_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"]

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed_at": new_task.completed_at
    }
    return response, 201





