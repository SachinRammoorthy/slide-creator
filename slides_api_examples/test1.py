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
                        "objectId": "PenguinSlide",
                        "slideLayoutReference": {
                        "predefinedLayout": "TITLE_AND_BODY"
                        },
                        "placeholderIdMappings": [
                        {
                            "objectId": "PenguinTitle",
                            "layoutPlaceholder": {
                            "type": "TITLE",
                            "index": 0
                            }
                        },
                        {
                            "objectId": "PenguinBody",
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
                        "objectId": "PenguinTitle",
                        "text": "The Wondrous World of Penguins"
                    }
                    },
                    {
                    "updateTextStyle": {
                        "objectId": "PenguinTitle",
                        "textRange": {
                        "type": "ALL"
                        },
                        "style": {
                        "fontSize": {
                            "magnitude": 48,
                            "unit": "PT"
                        },
                        "bold": True
                        },
                        "fields": "fontSize,bold"
                    }
                    },
                    {
                    "insertText": {
                        "objectId": "PenguinBody",
                        "text": "- Flightless birds adapted for swimming\n- Found mostly in the Southern Hemisphere\n- Excellent divers and swimmers\n- Have dense feathers for insulation\n- Live in large colonies"
                    }
                    },
                    {
                        "createParagraphBullets": {
                            "objectId": "PenguinBody",
                            "textRange": {
                            "type": "ALL"
                            },
                            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
                        }
                    },
                    {
                    "createShape": {
                        "objectId": "PenguinShape",
                        "shapeType": "ELLIPSE",
                        "elementProperties": {
                        "pageObjectId": "PenguinSlide",
                        "size": {
                            "height": {
                            "magnitude": 300,
                            "unit": "PT"
                            },
                            "width": {
                            "magnitude": 200,
                            "unit": "PT"
                            }
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": 400, 
                            "translateY": 150,
                            "unit": "PT"
                        }
                        }
                    }
                    },
                    {
                    "updateShapeProperties": {
                        "objectId": "PenguinShape",
                        "shapeProperties": {
                        "shapeBackgroundFill": {
                            "solidFill": {
                            "color": {
                                "rgbColor": {
                                "red": 0.0,
                                "green": 0.0,
                                "blue": 1.0
                                }
                            }
                            }
                        }
                        },
                        "fields": "shapeBackgroundFill.solidFill.color"
                    }
                    },
                    {
                    "updatePageProperties": {
                        "objectId": "PenguinSlide",
                        "pageProperties": {
                        "pageBackgroundFill": {
                            "solidFill": {
                            "color": {
                                "rgbColor": {
                                "red": 0.0,
                                "green": 0.5,
                                "blue": 0.0 
                                }
                            }
                            }
                        }
                        },
                        "fields": "pageBackgroundFill.solidFill.color"
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