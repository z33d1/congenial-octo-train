from flask_script import Manager
from app import create_app
from app.setup_db import setup_users_db, clear_users_db

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host="0.0.0.0", port=8085, debug=True)


@manager.command
def test():
    print("Tests here")


@manager.command
def setup_db():
    setup_users_db()


@manager.command
def drop_db():
    clear_users_db()


if __name__ == '__main__':
    manager.run()