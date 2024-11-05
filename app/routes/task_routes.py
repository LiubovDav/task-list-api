from flask import Blueprint, request, Response, make_response, abort
from app.models.task import Task
from ..db import db

bp = Blueprint("task_bp", __name__, url_prefix="/tasks" )

@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

    except KeyError as e:
        response = {
            "details": "Invalid data"
        }
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

   
    # try:
    #      description = request_body["description"]
    # except:
    #     response = {
    #         "details": "Invalid data"
    #     }
    #     return response, 400


    # try:
    #     completed_at = request_body["completed_at"]
    # except:
    #     completed_at = None


    # new_task = Task(title=title, description=description, completed_at=completed_at)


    

@bp.get("")
def get_all_task():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    completed_at_param = request.args.get("completed_at")
    if completed_at_param:
        query = query.where(Task.completed_at.ilike(f"%{completed_at_param}%"))

    sort_param = request.args.get("sort")
    if sort_param:
        if sort_param == "asc":
            query = query.order_by(Task.title.asc())
        elif sort_param == "desc":
            query = query.order_by(Task.title.desc())

    query = query.order_by(Task.id)
    task = db.session.scalars(query)

    tasks_response = []
    for task in task:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at != None
            }
        )
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return task.to_dict()

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"details": "Invalid data"}

        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    }

    return response, 200

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }

    return response, 200






