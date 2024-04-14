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
            "objectId": "PenguinSlide1",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle1",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody1",
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
            "objectId": "PenguinTitle1",
            "text": "Introduction to Penguins"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle1",
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
            "objectId": "PenguinBody1",
            "text": "- Overview of penguins\n- General characteristics and adaptations"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody1",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
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
            "text": "- Description of various penguin species\n- Differences in size, color, habitat, and behavior"
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
            "objectId": "PenguinSlide5",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle5",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody5",
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
            "objectId": "PenguinTitle5",
            "text": "Penguin Behavior"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle5",
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
            "objectId": "PenguinBody5",
            "text": "- Social structure and communication\n- Reproduction and parenting behaviors"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody5",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide6",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle6",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody6",
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
            "objectId": "PenguinTitle6",
            "text": "Penguin Conservation"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle6",
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
            "objectId": "PenguinBody6",
            "text": "- Threats to penguin populations\n- Conservation efforts and initiatives"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody6",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide7",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle7",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody7",
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
            "objectId": "PenguinTitle7",
            "text": "Penguin Distribution"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle7",
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
            "objectId": "PenguinBody7",
            "text": "- Geographic range of penguin species\n- Distribution patterns and factors influencing distribution"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody7",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide8",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle8",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody8",
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
            "objectId": "PenguinTitle8",
            "text": "Penguin Adaptations"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle8",
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
            "objectId": "PenguinBody8",
            "text": "- Physical and behavioral adaptations\n- Specialized features for survival in cold environments"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody8",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide9",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle9",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody9",
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
            "objectId": "PenguinTitle9",
            "text": "Penguin Life Cycle"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle9",
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
            "objectId": "PenguinBody9",
            "text": "- Stages of the penguin life cycle\n- From egg laying to fledging"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody9",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide10",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle10",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody10",
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
            "objectId": "PenguinTitle10",
            "text": "Penguin Predators"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle10",
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
            "objectId": "PenguinBody10",
            "text": "- Natural predators of penguins\n- Predation risks and survival strategies"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody10",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide11",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle11",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody11",
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
            "objectId": "PenguinTitle11",
            "text": "Penguin Anatomy"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle11",
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
            "objectId": "PenguinBody11",
            "text": "- Detailed anatomy of penguins\n- Structural features and adaptations"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody11",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide12",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle12",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody12",
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
            "objectId": "PenguinTitle12",
            "text": "Penguin Communication"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle12",
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
            "objectId": "PenguinBody12",
            "text": "- Vocalizations and body language\n- Social interactions and signaling"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody12",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide13",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle13",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody13",
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
            "objectId": "PenguinTitle13",
            "text": "Penguin Threats"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle13",
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
            "objectId": "PenguinBody13",
            "text": "- Human impacts and environmental threats\n- Pollution, climate change, and habitat destruction"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody13",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide14",
            "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_BODY"
            },
            "placeholderIdMappings": [
                {
                    "objectId": "PenguinTitle14",
                    "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                    }
                },
                {
                    "objectId": "PenguinBody14",
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
            "objectId": "PenguinTitle14",
            "text": "Penguin Research"
        }
    },
    {
        "updateTextStyle": {
            "objectId": "PenguinTitle14",
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
            "objectId": "PenguinBody14",
            "text": "- Scientific studies and research projects\n- Insights into penguin biology and ecology"
        }
    },
    {
        "createParagraphBullets": {
            "objectId": "PenguinBody14",
            "textRange": {
                "type": "ALL"
            },
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
        }
    },
    {
        "createSlide": {
            "objectId": "PenguinSlide15",
            "slideLayoutReference": {
                "predefinedLayout": "BLANK"
            }
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