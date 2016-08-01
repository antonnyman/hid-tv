from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from project import app, db
from project.models import User

#from werkzeug.serving import make_ssl_devcert

#make_ssl_devcert('./ssl', host='localhost')


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)

##localhost
app.run(debug=True, ssl_context=('./ssl.crt', './ssl.key'))

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
