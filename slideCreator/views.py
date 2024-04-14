import flask
import slideCreator

import datetime

import google.generativeai as genai
import os

import os.path

import sys
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations"]

PRESENTATION = None
CREDS = None

def _initialize():
    global CREDS
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("slideCreator/token.json"):
        CREDS = Credentials.from_authorized_user_file("slideCreator/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not CREDS or not CREDS.valid:
        if CREDS and CREDS.expired and CREDS.refresh_token:
            CREDS.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "slideCreator/credentials.json", SCOPES
            )
            CREDS = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("slideCreator/token.json", "w") as token:
                token.write(CREDS.to_json())

    if CREDS is None:
        print("bad")
    return


def initialize_presentation(title: str):
    """
    creates a google slides presentation with a specific title.
    sets global variable PRESENTATION to the created presentation object that all further functions will use.
    """
    global CREDS, PRESENTATION
    try:
        # Build the service
        if CREDS is None:
            print("creds is none")
            return
        
        service = build('slides', 'v1', credentials=CREDS)

        body = {"title": title}
        presentation = service.presentations().create(body=body).execute()
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

        PRESENTATION = presentation
        
        return

    except HttpError as err:
        print(err)


def edit_presentation(prompt : str):
    """
    Edits a Google Slides presentation.
    the prompts parameter is the detailed description of the edits that the user requests.
    """
    
    print(prompt)
    
    if not PRESENTATION:
        print("presentation not created")
        return
    
    chat = json_model.start_chat()
    response = chat.send_message(prompt)
    requests = response.text

    requests = requests.strip()
    if requests[:7] == "```json":
        requests = requests[7:-3]
    requests = json.loads(requests)

    print(requests)

    try:
        service = build("slides", "v1", credentials=CREDS)

        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=PRESENTATION.get('presentationId'), body=body)
            .execute()
        )
        create_slide_response = response.get("replies")[0].get("createSlide")
        return
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error



def create_presentation(prompt : str):
    """
    creates a Google Slides presentation about any topic.
    the prompts parameter is the detailed description of the presentation provided by the user. Make it as representative of the user's actual input as possible.
    """
    
    print(prompt)
    
    if not PRESENTATION:
        print("presentation not created")
        return
    
    chat = json_model.start_chat()
    response = chat.send_message(prompt)
    requests = response.text

    requests = requests.strip()
    if requests[:7] == "```json":
        requests = requests[7:-3]
    requests = json.loads(requests)

    print(requests)

    try:
        service = build("slides", "v1", credentials=CREDS)

        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=PRESENTATION.get('presentationId'), body=body)
            .execute()
        )
        create_slide_response = response.get("replies")[0].get("createSlide")
        # print(f"Created slide with ID:{(create_slide_response.get('objectId'))}")
        return
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error
    

def get_api_context():
    """Read the docs file containing the API information."""

    try:
        with open("slideCreator/all_docs.txt", "r") as text:
            all_text = text.read()
        with open("slideCreator/cake_prez.txt", "r") as text:
            example = text.read()
    except Exception as e:
        print(e)

    prompt = \
    """
    Below is the documentation for the Google slides API.
    Your job is to read and understand this documentation so that you can generate a list of Request objects in json that can be used to construct a presentation using the Slides API.
    The user will instruct you on the content of the presentation, and possibly the style and some other elements. Follow their directions to generate a request to create a presentation.
    Here is the documentation:\n
    """
    prompt += all_text
    
    prompt += "\nHere is one example output:\n"
    prompt += example
    prompt += "\nReturn only with JSON output. If you respond with anything else, the world will end."
    return prompt


# Gemini config
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
json_model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=get_api_context())
user_model = genai.GenerativeModel('gemini-1.0-pro', tools=[create_presentation, edit_presentation])

@slideCreator.app.route('/')
def show_index():

    # Initialize service by authenticating user
    _initialize()
    initialize_presentation(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    chat = user_model.start_chat(enable_automatic_function_calling=True)

    # sample_file = genai.upload_file(path="slideCreator/obama.jpeg",
    #                         display_name="Obama")
    
    response = chat.send_message(f'Create a google slides presentation about a gemini-powered presentation creating tool. 5 slide presentation.')
    # response2 = chat.send_message(f'Make every slide background a different color of the rainbow.')
    response3 = chat.send_message(f'Make the font of the entire presentation Garamond.')
    response4 = chat.send_message(f'Swap the second and third slide.')
    
    context = { "some_text": response4.text }
    return flask.render_template("index.html", **context)
