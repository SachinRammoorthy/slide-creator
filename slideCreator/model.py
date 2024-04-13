"""Model API – Database setup."""

import flask
import slideCreator

def get_db():
    pass

@slideCreator.app.teardown_appcontext
def close_db(error):
    pass
