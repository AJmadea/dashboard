import os
from flask import Flask

def create_app(test_config=None):
    app=Flask(__name__, instance_relative_config=True)



    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
        print(app)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

app=create_app()


print(app.config)