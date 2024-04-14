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
        "objectId": "Slide1",
        "slideLayoutReference": {
            "predefinedLayout": "TITLE_AND_BODY"
        },
        "placeholderIdMappings": [
            {
            "objectId": "Title1",
            "layoutPlaceholder": {
                "type": "TITLE",
                "index": 0
            }
            },
            {
            "objectId": "Body1",
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
        "objectId": "Title1",
        "text": "George Washington: A Life of Service"
        }
    },
    {
        "insertText": {
        "objectId": "Body1",
        "text": "Early Life and Interests"
        }
    },
    {
        "createSlide": {
        "objectId": "Slide2",
        "slideLayoutReference": {
            "predefinedLayout": "TITLE_AND_BODY"
        },
        "placeholderIdMappings": [
            {
            "objectId": "Title2",
            "layoutPlaceholder": {
                "type": "TITLE",
                "index": 0
            }
            },
            {
            "objectId": "Body2",
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
        "objectId": "Title2",
        "text": "Formative Years"
        }
    },
    {
        "insertText": {
        "objectId": "Body2",
        "text": "Born in Westmoreland County, Virginia, in 1732\n- Received a basic education, focusing on practical skills\n- Developed a strong interest in surveying and military arts"
        }
    },
    {
        "createSlide": {
        "objectId": "Slide3",
        "slideLayoutReference": {
            "predefinedLayout": "TITLE_AND_BODY"
        },
        "placeholderIdMappings": [
            {
            "objectId": "Title3",
            "layoutPlaceholder": {
                "type": "TITLE",
                "index": 0
            }
            },
            {
            "objectId": "Body3",
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
        "objectId": "Title3",
        "text": "Military Experience and Land Ownership"
        }
    },
    {
        "insertText": {
        "objectId": "Body3",
        "text": "- Served as a surveyor and gained valuable land management skills\n- Participated in the French and Indian War, rising through the ranks\n- Became a prominent landowner and farmer"
        }
    },
    {
        "createSlide": {
        "objectId": "Slide4",
        "slideLayoutReference": {
            "predefinedLayout": "TITLE_AND_BODY"
        },
        "placeholderIdMappings": [
            {
            "objectId": "Title4",
            "layoutPlaceholder": {
                "type": "TITLE",
                "index": 0
            }
            },
            {
            "objectId": "Body4",
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
        "objectId": "Title4",
        "text": "Leadership in the Revolutionary War"
        }
    },
    {
        "insertText": {
        "objectId": "Body4",
        "text": "- Appointed Commander-in-Chief of the Continental Army in 1775\n- Led the American forces to victory against the British\n- Faced numerous challenges, including lack of supplies and troop morale"
        }
    },
    {
        "createSlide": {
        "objectId": "Slide5",
        "slideLayoutReference": {
            "predefinedLayout": "TITLE_AND_BODY"
        },
        "placeholderIdMappings": [
            {
            "objectId": "Title5",
            "layoutPlaceholder": {
                "type": "TITLE",
                "index": 0
            }
            },
            {
            "objectId": "Body5",
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
        "objectId": "Title5",
        "text": "Legacy and Impact"
        }
    },
    {
        "insertText": {
        "objectId": "Body5",
        "text": "- Played a crucial role in the founding of the United States\n- Served as the first President of the United States (1789-1797)\n- Remembered as a symbol of leadership, integrity, and patriotism"
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