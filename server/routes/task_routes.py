from flask import Blueprint, request, jsonify
from models import db
from models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint("task", __name__)
@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_task = Task(
        title=data.get("title"),
        description=data.get("description"),
        completed=False,
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        "message": "Task created",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }
    }, 201
@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    tasks_query = Task.query.filter_by(user_id=user_id)

    paginated = tasks_query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed
            } for t in paginated.items
        ],
        "total": paginated.total,
        "page": page,
        "pages": paginated.pages
    }, 200
@task_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get(task_id)

    if not task or task.user_id != user_id:
        return {"error": "Task not found"}, 404

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return {"message": "Task updated"}, 200
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.get(task_id)

    if not task or task.user_id != user_id:
        return {"error": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted"}, 200