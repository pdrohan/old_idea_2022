from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager
from flask_login import user_unauthorized
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, logout_user, current_user
from flask_user import roles_required, UserManager, PasswordManager, EmailManager
from flask_mail import Mail, Message

db = SQLAlchemy()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    mail = Mail(app)
    #APPLICATION SETTINGS
    app.config['SECRET_KEY'] = 'petersworldpetersworldpetersworldpeterworld'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #FLASK USER SETTINGS
    app.config['CSRF_ENABLED'] = True
    app.config['USER_LOGIN_URL'] = '/login/'
    app.config['USER_APP_NAME'] = 'SNAPSHOT'
    app.config['USER_COPYRIGHT_YEAR'] = '2021'
    app.config['USER_CORPORATION_NAME'] = 'SNAPSHOT'
    app.config['USER_ENABLE_CHANGE_PASSWORD'] = True
    app.config['USER_ENABLE_CHANGE_USERNAME'] = False
    app.config['USER_ENABLE_CONFIRM_EMAIL'] = True
    app.config['USER_ENABLE_FORGOT_PASSWORD'] = True
    app.config['USER_ENABLE_REGISTRATION'] = True
    app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True
    #FLASK-MAIL SETTINGS
    app.config['USER_EMAIL_SENDER_EMAIL'] = "snapshotsystem@gmail.com"
    app.config['MAIL_SERVER'] = 'smpt.gmail.com'
    app.config['MAIL_USERNAME'] = 'snapshotsystem@gmail.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'snapshotsystem@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Zxcasdqwe448#'
    app.config['MAIL_PORT'] = '587'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['USER_ENABLE_USERNAME'] = False
    app.config['USER_ENABLE_EMAIL'] = True
    db.init_app(app)

    #import the views we created from the views file
    from .views import views
    from .auth import auth

    @app.before_first_request
    def create_tables():
        db.create_all()

    from .models import User, Note, Notetype, Role, Player, Coach, Metric, Game, Rating, Team, Adminn

    user_manager = UserManager(app, db, User)
    # password_manager = PasswordManager(app)
    # email_manager = EmailManager(app)

    #figure out admin

    admin = Admin(app)
    # class AdminControl(ModelView):
    #     column_display_pk = True
    #     def is_accessible(self):
    #         if current_user.is_admin == True:
    #             return current_user.is_authenticated
    #     def not_authenticated(self):
    #         return abort()

    #register the blueprintgs
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)
#This is telling flask how we load a user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Adminn, db.session))
    admin.add_view(ModelView(Player, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Note, db.session))


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')
