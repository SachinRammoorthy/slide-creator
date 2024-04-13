import flask
import slideCreator

import google.generativeai as genai
import os

import os.path

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


def create_presentation(title: str):
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

        PRESENTATION = presentation        
        return

    except HttpError as err:
        print(err)


def create_slide():
    """
    creates a blank slide on the presentation object PRESENTATION previously created.
    """
    
    if not PRESENTATION:
        print("presentation not created")
        return

    try:
        service = build("slides", "v1", credentials=CREDS)
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        requests = [
            {
                "createSlide": {
                    "objectId": "ABCDFE",
                    "insertionIndex": "1",
                    "slideLayoutReference": {
                        "predefinedLayout": "TITLE_AND_TWO_COLUMNS"
                    },
                }
            },
        ]

        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.

        # Execute the request.
        body = {"requests": requests}
        response = (
            service.presentations()
            .batchUpdate(presentationId=PRESENTATION.get('presentationId'), body=body)
            .execute()
        )
        create_slide_response = response.get("replies")[0].get("createSlide")
        print(f"Created slide with ID:{(create_slide_response.get('objectId'))}")
        return
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error

# Gemini config
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest', tools=[create_presentation, create_slide])

@slideCreator.app.route('/')
def show_index():

    # Initialize service by authenticating user
    _initialize()

    # response = model.generate_content("New Delhi is in the country of")
    chat = model.start_chat(enable_automatic_function_calling=True)

    response = chat.send_message('Can you create a google slides presentation called Random Pres?')
    response2 = chat.send_message('Can you create a blank slide on the same presentation?')

    context = { "some_text": response2.text }
    return flask.render_template("index.html", **context)
