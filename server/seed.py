from app import app
from models import db
from models.user import User
from models.task import Task

with app.app_context():
    print("Clearing database...")

    Task.query.delete()
    User.query.delete()

    db.session.commit()

    print("Seeding users...")

    user1 = User(username="alice")
    user1.set_password("1234")

    user2 = User(username="bob")
    user2.set_password("1234")

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding tasks...")

    task1 = Task(title="Alice Task 1", description="First task", user_id=user1.id)
    task2 = Task(title="Alice Task 2", description="Second task", user_id=user1.id)
    task3 = Task(title="Bob Task 1", description="Bob task", user_id=user2.id)

    db.session.add_all([task1, task2, task3])
    db.session.commit()

    print("Seeding complete!")