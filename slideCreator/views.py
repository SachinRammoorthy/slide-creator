import flask
import slideCreator

import datetime
import time

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

from google.generativeai.types import HarmCategory, HarmBlockThreshold

import pathlib
import tempfile

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations"]

PRESENTATION = None
CREDS = None
JSON_CHAT = None
USER_CHAT = None


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


def _get_audio():
    audio = genai.upload_file("slideCreator/MLK_Speech.mp3")
    return audio


def _disable_saftey():
    to_return = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    return to_return


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

        service = build("slides", "v1", credentials=CREDS)

        body = {"title": title}
        presentation = service.presentations().create(body=body).execute()
        print(f"Created presentation with ID:{(presentation.get('presentationId'))}")

        request = {
            "requests": [
                {"deleteObject": {"objectId": presentation["slides"][0]["objectId"]}}
            ]
        }

        # Execute the request to delete the slide
        response = (
            service.presentations()
            .batchUpdate(
                presentationId=presentation.get("presentationId"), body=request
            )
            .execute()
        )

        PRESENTATION = presentation

        return

    except HttpError as err:
        print(err)


def edit_presentation(prompt: str):
    """
    Edits a Google Slides presentation.
    the prompts parameter is the description of the edits that the user requests.
    this includes inserting images, changing colors, adding text or certain elements, etc. making any changes to a presentation.
    """

    # problem might be that this output is not just editing but replacing the entire thing.

    global JSON_CHAT, PRESENTATION

    print("editing")
    print(prompt)

    if not PRESENTATION:
        print("presentation not created")
        return

    # chat = json_model.start_chat()
    response = JSON_CHAT.send_message(prompt)
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
            .batchUpdate(presentationId=PRESENTATION.get("presentationId"), body=body)
            .execute()
        )
        create_slide_response = response.get("replies")[0].get("createSlide")
        return

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error


def create_presentation(prompt: str):
    """
    creates a Google Slides presentation about any topic.
    the prompts parameter is the description of the presentation provided by the user.
    """

    global JSON_CHAT, PRESENTATION

    print("creating")
    print(prompt)

    if not PRESENTATION:
        print("presentation not created")
        return

    # chat = json_model.start_chat()

    response = JSON_CHAT.send_message(prompt)
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
            .batchUpdate(presentationId=PRESENTATION.get("presentationId"), body=body)
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
        # with open("slideCreator/cake_prez.txt", "r") as text:
        #     example = text.read()
    except Exception as e:
        print(e)

    prompt = """
    Below is the documentation for the Google slides API.
    Your job is to read and understand this documentation so that you can generate a list of Request objects in json that can be used to construct a presentation using the Slides API.
    The user will instruct you on the content of the presentation, and possibly the style and some other elements. Follow their directions to generate a request to create or edit the presentation.
    If only an edit (such as inserting an image, text, style, etc), do not re-create the presentation -- only create requests that will update the existing slides.
    Here is the documentation:\n
    """
    prompt += all_text

    prompt += "\nHere is one example output for a request to create a presentation about a gemini-powered presentation tool:\n"
    prompt += "[{'createSlide': {'objectId': 'Slide1', 'slideLayoutReference': {'predefinedLayout': 'TITLE_ONLY'}, 'placeholderIdMappings': [{'objectId': 'Slide1Title', 'layoutPlaceholder': {'type': 'TITLE', 'index': 0}}]}}, {'insertText': {'objectId': 'Slide1Title', 'insertionIndex': 0, 'text': 'Introducing the Gemini Presentation Tool'}}, {'updateTextStyle': {'objectId': 'Slide1Title', 'textRange': {'type': 'ALL'}, 'style': {'fontSize': {'magnitude': 72, 'unit': 'PT'}, 'bold': True}, 'fields': 'fontSize,bold'}}, {'createSlide': {'objectId': 'Slide2', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'Title2', 'layoutPlaceholder': {'type': 'TITLE', 'index': 0}}, {'objectId': 'Body2', 'layoutPlaceholder': {'type': 'BODY', 'index': 0}}]}}, {'insertText': {'objectId': 'Title2', 'text': 'Powered by Advanced AI'}}, {'insertText': {'objectId': 'Body2', 'text': 'This innovative tool leverages the power of Gemini, a large language model, to create stunning presentations with ease.'}}, {'createSlide': {'objectId': 'Slide3', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'Title3', 'layoutPlaceholder': {'type': 'TITLE', 'index': 0}}, {'objectId': 'Body3', 'layoutPlaceholder': {'type': 'BODY', 'index': 0}}]}}, {'insertText': {'objectId': 'Title3', 'text': 'Effortless Content Creation'}}, {'insertText': {'objectId': 'Body3', 'text': 'Simply provide your topic and key points, and Gemini will generate compelling content, including text, images, and even videos.'}}, {'createSlide': {'objectId': 'Slide4', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'Title4', 'layoutPlaceholder': {'type': 'TITLE', 'index': 0}}, {'objectId': 'Body4', 'layoutPlaceholder': {'type': 'BODY', 'index': 0}}]}}, {'insertText': {'objectId': 'Title4', 'text': 'Customization and Style'}}, {'insertText': {'objectId': 'Body4', 'text': 'Tailor your presentation with various themes, layouts, and formatting options to match your brand and style.'}}, {'createSlide': {'objectId': 'Slide5', 'slideLayoutReference': {'predefinedLayout': 'TITLE_ONLY'}, 'placeholderIdMappings': [{'objectId': 'Title5', 'layoutPlaceholder': {'type': 'TITLE', 'index': 0}}]}}, {'insertText': {'objectId': 'Title5', 'text': 'Create impactful presentations with Gemini!'}}]\n"
    prompt += "\nHere is one example output for a request to edit the presentation by inserting an image on slide 2:\n"
    prompt += "\n[{'createImage': {'objectId': 'AI_Image', 'url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStEdQs2Dcjx3LazH-YKPoObGErNNzmxNs_2OpNCMHrAGbRSwqMN7-21tm7p_8&s', 'elementProperties': {'pageObjectId': 'Slide2', 'size': {'height': {'magnitude': 200, 'unit': 'PT'}, 'width': {'magnitude': 200, 'unit': 'PT'}}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 100, 'translateY': 100, 'unit': 'PT'}}}}]"

    # prompt += example
    prompt += "\nReturn only with JSON output. If you respond with anything else, the world will end."
    return prompt


# Gemini config
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
json_model = genai.GenerativeModel(
    "gemini-1.5-pro-latest", system_instruction=get_api_context()
)
user_model = genai.GenerativeModel(
    "gemini-1.5-pro-latest", tools=[create_presentation, edit_presentation]
)


@slideCreator.app.route("/")
def show_index():
    return flask.render_template("index.html")


@slideCreator.app.route("/generate/", methods=["POST"])
def generate():
    global JSON_CHAT, USER_CHAT

    response = {"status": "success", "message": None}
    try:
        files = flask.request.files
    except:
        response["status"] = "error"
        response["message"] = "No files uploaded"
        print(response)
        return flask.jsonify(response)

    try:
        form_data = json.loads(flask.request.form["data"])
    except:
        response["status"] = "error"
        response["message"] = "No form data"
        print(response)
        return flask.jsonify(response)

    response["message"] = "Creating slides..."

    print(form_data)
    # Initialize service by authenticating user
    _initialize()
    initialize_presentation(form_data["title"])
    USER_CHAT = user_model.start_chat(enable_automatic_function_calling=True)

    file_arr = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        dirpath = pathlib.Path(temp_dir)
        for file in files:
            filepath = dirpath / file
            files[file].save(filepath)
            file_arr.append(genai.upload_file(path=str(filepath), display_name=file))

    JSON_CHAT = json_model.start_chat()

    if file_arr:
        response["message"] = USER_CHAT.send_message(
            [form_data["topics"][0]["data"], *file_arr],
            safety_settings=_disable_saftey(),
        )
    else:
        response["message"] = USER_CHAT.send_message(
            form_data["topics"][0]["data"],
            safety_settings=_disable_saftey(),
        )
    
    # response["message"] = USER_CHAT.send_message("make slide 2 blue")

    return {}
