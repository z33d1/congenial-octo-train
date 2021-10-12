from flask_script import Manager
from app import create_app
from app.setup_db import setup_orders_db, drop_orders_db

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=1003, debug=True)
    
@manager.command
def setup_db():
    setup_orders_db()

@manager.command
def drop_db():
    drop_orders_db()

@manager.command
def test():
    print("Tests here")

if __name__ == '__main__':
    manager.run()