import flask
import slideCreator


@slideCreator.app.route('/')
def show_index():
    # Connect to database
    connection = slideCreator.model.get_db()

    context = { "num_integrations": 1024 }
    return flask.render_template("index.html", **context)
