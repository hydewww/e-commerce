#!/usr/bin/env python
from app import create_app, db
from app.models import User, Item, Order, Order_Item, Cart, Cate
from flask_script import Manager, Shell, Server

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Item=Item, Order=Order, Order_Item=Order_Item, Cart=Cart, Cate=Cate)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
