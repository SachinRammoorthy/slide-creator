import flask
import json
import datetime
import slideCreator
import time

import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse, HarmBlockThreshold, HarmCategory
import os

import os.path

from slideCreator.config import CREDS, SYS_INSTRUCTION
from slideCreator.model import call_generative_curl_request

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


PRESENTATION_ID = None

settings_override={
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE
}

def create_presentation(title: str):
    """creates a google slides presentation with a specific title"""
    global PRESENTATION_ID
    try:
        # Build the service
        service = build('slides', 'v1', credentials=CREDS)

        body = {"title": title}
        presentation = service.presentations().create(body=body).execute()
        PRESENTATION_ID = presentation.get('presentationId')
        print(
            f"Created presentation with ID:{(presentation.get('presentationId'))}"
        )
        request = {
            'requests': [
                {
                    'deleteObject': {
                        'objectId': presentation['slides'][0]['objectId']
                    }
                }
            ]
        }
        # Execute the request to delete the slide
        response = service.presentations().batchUpdate(
            presentationId=presentation.get('presentationId'),
            body=request
        ).execute()

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
    NOTE: When inserting text, take care to reference the objectID of the shape or table cell, NOT the slide object because that is not allowed!
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

def _clean_gemini_json_response(resp: GenerateContentResponse):
    """Remove the extra characters before and after the response. Return only JSON"""
    string = resp.text
    print("RAW string", string)
    string = string.strip()
    if string[:7] == "```json":
        string = string[7:-3]
    request_json = json.loads(string)
    return request_json

def _apply_slide_changes(resp: GenerateContentResponse):
    """Apply the changes to the slide deck."""
    global PRESENTATION_ID
    json = _clean_gemini_json_response(resp)
    print("\n\n",json,"\n\n")
    try:
        service = build("slides", "v1", credentials=CREDS)

        # Execute the request.
        body = {"requests": json}
        response = (
            service.presentations()
            .batchUpdate(presentationId=PRESENTATION_ID, body=body)
            .execute()
        )
        create_slide_response = response.get("replies")[0].get("createSlide")
        return

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error


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

    # msg = get_api_context()

    obama_img = genai.upload_file("slideCreator/static/images/image_alex.jpg")
    print("Obama image: ", obama_img.uri)

    user_req = "\nUSER: I need a presentation about Johnny Sins -- the person in this image. Tell me about his life, accomplishments, controversies, and some fun facts.\n"

    print("sent message")
    #response = call_generative_curl_request(os.environ["GOOGLE_API_KEY"], SYS_INSTRUCTION, msg, user_req)
    #print(response.json())
    response = chat.send_message([user_req, obama_img], safety_settings=settings_override)
    _apply_slide_changes(response)
    # public_obama_img = "https://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg"
    # response = chat.send_message(f"Generate a title page for the presentation. Use this link to get the public photo of Obama on the title page: {public_obama_img}. Put the image in the middle of the page.")
    # _apply_slide_changes(response)

    end_time = time.time()

    context = { "some_text": response.text,
               "elapsed_time": (end_time - start_time) }
    return flask.render_template("index.html", **context)
