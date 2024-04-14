import flask
import datetime
import slideCreator
import time

import google.generativeai as genai
import os

import os.path

from slideCreator.config import CREDS, SYS_INSTRUCTION
from slideCreator.model import call_generative_curl_request

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


PRESENTATION_ID = None

def create_presentation(title: str):
    """creates a google slides presentation with a specific title"""

    try:
        # Build the service
        service = build('slides', 'v1', credentials=CREDS)

        body = {"title": title}
        presentation = service.presentations().create(body=body).execute()
        print(
            f"Created presentation with ID:{(presentation.get('presentationId'))}"
        )
        return presentation
    except HttpError as err:
        print(err)


def get_api_context():
    """Read the docs file containing the API information."""

    try:
        print("loading docs")
        with open("slideCreator/all_docs.txt", "r") as text:
            all_text = text.read()
        print("done loading docs")
    except Exception as e:
        print(e)

    prompt = \
    """
    Below is the documentation for the Google slides API.\n
    Your job is to read and understand this documentation so that you can generate a list of Request objects in json that can be used to construct a presentation.
    The presentation object already exists, you just need to generate the list of JSON Request objects holding all the content.

    REMINDER: You can ONLY return JSON or the world will explode and children will burn and die.
    \n
    ##################\n
    # BEGIN DOCUMENTATION\n
    ##################\n
    """
    prompt += all_text
    prompt += \
    """
    \n
    ##################\n
    # END DOCUMENTATION\n
    ##################\n
    \n
    """
    return prompt



# Gemini config
genai.configure(api_key=os.environ["GOOGLE_API_KEY"], transport='rest')
model = genai.GenerativeModel('gemini-1.5-pro-latest',
                              system_instruction=SYS_INSTRUCTION)

@slideCreator.app.route('/')
def show_index():
    start_time = time.time()

    # response = model.generate_content("New Delhi is in the country of")
    chat = model.start_chat(enable_automatic_function_calling=True)

    title = f"Eli Slide Deck {datetime.datetime.now()}"

    create_presentation(title)

    msg = get_api_context()

    obama_img = genai.upload_file("slideCreator/static/images/obama.jpg")
    print("Obama image: ", obama_img.uri)

    user_req = "\nUSER: I need a presentation all the president in the attached photo. His early life, accomplishments, controversies, and any other fun facts you think would be appropriate.\n"

    print("sent message")
    #response = call_generative_curl_request(os.environ["GOOGLE_API_KEY"], SYS_INSTRUCTION, msg, user_req)
    #print(response.json())
    response = chat.send_message([msg+user_req, obama_img])
    print("msg one done.")
    response = chat.send_message(f"Generate a title page for the presentation. Insert the obama image into this title page. The URL is {obama_img.uri}")

    end_time = time.time()

    context = { "some_text": response.text,
               "elapsed_time": (end_time - start_time) }
    return flask.render_template("index.html", **context)
