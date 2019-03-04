import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from config import Config

import pandas as pd

import os.path

from app.webapp import requires_roles


def create_app():
    server = Flask(__name__)
    server.config.from_object(Config)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app):
    from app.dashapp1.layout import create_layout as create_layout1
    from app.dashapp1.callbacks import register_callbacks1 as register_callbacks1_1
    from app.dashapp1.callbacks import register_callbacks2 as register_callbacks2_1
    from app.dashapp1.callbacks import register_callbacks3 as register_callbacks3_1
    from app.dashapp1.callbacks import register_callbacks4 as register_callbacks4_1

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    dashapp1 = dash.Dash(__name__,
                        server = app,
                        url_base_pathname='/dashboard1/',
                        external_stylesheets=external_stylesheets)
    dashapp1.title = 'Standard DashViz'

    my_path = os.path.abspath(os.path.dirname(__file__))
    path1 = os.path.join(my_path, "datasets/test2")
    dset = pd.read_csv(path1)

    dashapp1.layout = create_layout1(dset)

    register_callbacks1_1(dashapp1, dset)
    register_callbacks2_1(dashapp1, dset)
    register_callbacks3_1(dashapp1, dset)
    register_callbacks4_1(dashapp1, dset)

    _protect_dashviews(dashapp1)

# Code which creates Dash Apps protected by authorization.

# Function creating role-based authorization.
# Not used with DashApp1 which is accessible to everyone 
def _protect_dashviews(dashapp, roles=()):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])
            if roles:
                dashapp.server.view_functions[view_func] = requires_roles(roles)(dashapp.server.view_functions[view_func])

def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
