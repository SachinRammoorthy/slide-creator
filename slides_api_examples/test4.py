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
            "objectId": "PenguinSlide2",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle2",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody2",
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
            "objectId": "PenguinTitle2",
            "text": "Different Penguin Species"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle2",
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
            "objectId": "PenguinBody2",
            "text": "- Description of various penguin species\n- Differences in size, color, and habitat"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody2",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide3",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle3",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody3",
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
            "objectId": "PenguinTitle3",
            "text": "Penguin Habitats"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle3",
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
            "objectId": "PenguinBody3",
            "text": "- Overview of penguin habitats\n- From icy Antarctica to temperate regions"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody3",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide4",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle4",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody4",
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
            "objectId": "PenguinTitle4",
            "text": "Penguin Diet"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle4",
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
            "objectId": "PenguinBody4",
            "text": "- Types of food penguins consume\n- Fishing techniques and hunting strategies"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody4",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide20",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle20",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody20",
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
            "objectId": "PenguinTitle20",
            "text": "Conclusion"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle20",
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
            "objectId": "PenguinBody20",
            "text": "- Summary of key points\n- Call to action or further exploration"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody20",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    }
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