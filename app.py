import os
import tempfile

from flask import Flask
from home import home
from search import search
from calculate import calculate
from logging.config import dictConfig


# logging configuration dict
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(message)s",
            },
            "app": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "filters":{
            "app":{
                "name": "app"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default"
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "app.log",
                "formatter": "app",
                "filters": ["app"]
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["file", "wsgi"]
        }
    }
)



def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(home.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(calculate.bp)

    return app

app = create_app()

