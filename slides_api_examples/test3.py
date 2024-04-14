import datetime
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
    if os.path.exists("token.json"):
        CREDS = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not CREDS or not CREDS.valid:
        if CREDS and CREDS.expired and CREDS.refresh_token:
            CREDS.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            CREDS = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(CREDS.to_json())
    
    if CREDS is None:
        print("bad")
    return


def create_presentation(title: str = f"Presentation {datetime.datetime.now()}"):
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
    requests = [
        {
            "createSlide": {
                "objectId": "CatSlide1",
                "slideLayoutReference": {
                    "predefinedLayout": "TITLE_AND_TWO_COLUMNS"
                },
                "placeholderIdMappings": [
                    {
                        "objectId": "CatTitle1",
                        "layoutPlaceholder": {
                            "type": "TITLE",
                            "index": 0
                        }
                    },
                    {
                        "objectId": "CatColumn1_1",
                        "layoutPlaceholder": {
                            "type": "BODY",
                            "index": 0
                        }
                    },
                    {
                        "objectId": "CatColumn1_2",
                        "layoutPlaceholder": {
                            "type": "BODY",
                            "index": 1
                        }
                    }
                ]
            }
        },
        {
            "insertText": {
                "objectId": "CatTitle1",
                "text": "Fascinating Felines"
            }
        },
        {
            "updateTextStyle": {
                "objectId": "CatTitle1",
                "textRange": {
                    "type": "ALL"
                },
                "style": {
                    "fontSize": {
                        "magnitude": 42,
                        "unit": "PT"
                    },
                    "bold": True
                },
                "fields": "fontSize,bold"
            }
        },
        {
            "insertText": {
                "objectId": "CatColumn1_1",
                "text": "- Cats are independent animals\n- Known for their agility and grace\n- Domesticated cats are descended from wild ancestors"
            }
        },
        {
            "insertText": {
                "objectId": "CatColumn1_2",
                "text": "- Cats have excellent night vision\n- Communication through meows, purrs, and body language\n- Variety of breeds with distinct characteristics"
            }
        },
        {
            "createParagraphBullets": {
                "objectId": "CatColumn1_1",
                "textRange": {
                    "type": "ALL"
                },
                "bulletPreset": "BULLET_ARROW_DIAMOND_DISC"
            }
        },
        {
            "createParagraphBullets": {
                "objectId": "CatColumn1_2",
                "textRange": {
                    "type": "ALL"
                },
                "bulletPreset": "BULLET_ARROW_DIAMOND_DISC"
            }
        },
        {
            "createSlide": {
                "objectId": "CatSlide2",
                "slideLayoutReference": {
                    "predefinedLayout": "TITLE_AND_BODY"
                },
                "placeholderIdMappings": [
                    {
                        "objectId": "CatTitle2",
                        "layoutPlaceholder": {
                            "type": "TITLE",
                            "index": 0
                        }
                    },
                    {
                        "objectId": "CatBody2",
                        "layoutPlaceholder": {
                            "type": "BODY",
                            "index": 0
                        }
                    }
                ]
            }
        },
        {
            "insertText": {
                "objectId": "CatTitle2",
                "text": "Cat Breeds"
            }
        },
        {
            "insertText": {
                "objectId": "CatBody2",
                "text": "There are numerous cat breeds, each with its own unique characteristics and personalities."
            }
        },
    ]




    # If you wish to populate the slide with elements,
    # add element create requests here, using the page_id.
    service = build('slides', 'v1', credentials=CREDS)

    # Execute the request.
    try:
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

if __name__ == "__main__":
    _initialize()
    create_presentation()
    create_slide()