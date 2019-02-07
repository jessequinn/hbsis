import coverage
import os
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from project import app, db

app.config.from_object(os.environ['APP_MODE'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def cov():
    '''
    Coverage test run.

    :return:
    '''
    cov = coverage.coverage(branch=True, include='project/*', omit='*/__init__.py')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


@manager.command
def test():
    '''
    Testing without coverage.

    :return:
    '''

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
