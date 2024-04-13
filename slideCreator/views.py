import flask
import slideCreator

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')

@slideCreator.app.route('/')
def show_index():
    # Connect to database
    connection = slideCreator.model.get_db()

    response = model.generate_content("New Delhi is in the country of")

    context = { "some_text": response.text }
    return flask.render_template("index.html", **context)
