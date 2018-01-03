#!/usr/bin/env python
from app import create_app, db
from app.models import User, Item, Order, Order_Item, Cart, Cate
from flask_script import Manager, Shell, Server

app = create_app()
manager = Manager(app)
server = Server(host='0.0.0.0', port=8899)


def make_shell_context():
    return dict(app=app, db=db, User=User, Item=Item, Order=Order, Order_Item=Order_Item, Cart=Cart, Cate=Cate)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('runserver', server)

if __name__ == '__main__':
    manager.run()
