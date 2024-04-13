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

def create_presentation(title: str):
    """creates a google slides presentation with a specific title"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("slideCreator/token.json"):
        creds = Credentials.from_authorized_user_file("slideCreator/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "slideCreator/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("slideCreator/token.json", "w") as token:
                token.write(creds.to_json())

    try:
        # Build the service
        service = build('slides', 'v1', credentials=creds)

        body = {"title": title}
        presentation = service.presentations().create(body=body).execute()
        print(
            f"Created presentation with ID:{(presentation.get('presentationId'))}"
        )
        return presentation
    except HttpError as err:
        print(err)



# Gemini config
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest', tools=[create_presentation])

@slideCreator.app.route('/')
def show_index():
    # Connect to database
    connection = slideCreator.model.get_db()

    # response = model.generate_content("New Delhi is in the country of")
    chat = model.start_chat(enable_automatic_function_calling=True)

    response = chat.send_message('Can you create a google slides presentation called Sachchits Magical Adventure?')

    context = { "some_text": response.text }
    return flask.render_template("index.html", **context)


