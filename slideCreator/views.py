import flask
import slideCreator

import datetime

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
    creates a blank slide
    """
    
    if not PRESENTATION:
        print("presentation not created")
        return

    try:
        service = build("slides", "v1", credentials=CREDS)
        
        requests = [
                    {
                    "createSlide": {
                        "objectId": "Slide1",
                        "slideLayoutReference": {
                        "predefinedLayout": "TITLE_ONLY"
                        },
                        "placeholderIdMappings": [
                        {
                            "objectId": "Slide1Title", 
                            "layoutPlaceholder": {
                            "type": "TITLE",
                            "index": 0
                            }
                        }
                        ]
                    }
                    },
                    {
                    "createImage": {
                        "objectId": "CakeImage",
                        "url": "https://www.nationsencyclopedia.com/photos/united-states-of-america-1087.jpg", 
                        "elementProperties": {
                        "pageObjectId": "Slide1",
                        "size": {
                            "height": {
                            "magnitude": 400,
                            "unit": "PT"
                            },
                            "width": {
                            "magnitude": 300,
                            "unit": "PT"
                            }
                        },
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": 100,
                            "translateY": 50, 
                            "unit": "PT"
                        }
                        }
                    }
                    },
                    {
                    "insertText": {
                        "objectId": "Slide1Title",
                        "insertionIndex": 0,
                        "text": "Happy Birthday!"
                    }
                    },
                    {
                    "updateTextStyle": {
                        "objectId": "Slide1Title",
                        "textRange": {
                        "type": "ALL"
                        },
                        "style": {
                        "fontSize": {
                            "magnitude": 72,
                            "unit": "PT"
                        },
                        "bold": "true",
                        "foregroundColor": {
                            "opaqueColor": {
                            "rgbColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0 
                            }
                            }
                        }
                        },
                        "fields": "fontSize,bold,foregroundColor"
                    }
                    }, 
                    {
                    "updatePageProperties": {
                        "objectId": "Slide1",
                        "pageProperties": {
                        "pageBackgroundFill": {
                            "solidFill": {
                            "color": {
                                "rgbColor": {
                                "red": 0.2,
                                "green": 0.2,
                                "blue": 0.5 
                                }
                            } 
                            }
                        }
                        },
                        "fields": "pageBackgroundFill.solidFill.color"
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
                        "text": "The Perfect Recipe"
                    }
                    },
                    {
                    "insertText": {
                        "objectId": "Body2",
                        "text": "- Flour\n- Sugar\n- Eggs\n- Butter\n- Vanilla\n- Sprinkles (lots!)" 
                    }
                    }, 
                    { 
                    "createParagraphBullets": {
                        "objectId": "Body2",
                        "textRange": {
                        "type": "ALL"
                        },
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
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
                        "text": "Baking with Love"
                    }
                    }, 
                    {
                    "insertText": { 
                        "objectId": "Body3",
                        "text": "- Preheat oven\n- Mix dry ingredients\n- Cream butter and sugar\n- Add eggs and vanilla\n- Combine wet and dry ingredients\n- Bake until golden brown"
                    }
                    },
                    { 
                    "createParagraphBullets": {
                        "objectId": "Body3",
                        "textRange": {
                        "type": "ALL"
                        },
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
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
                        "text": "Decorating Delights"
                    }
                    }, 
                    {
                    "insertText": {
                        "objectId": "Body4", 
                        "text": "- Frosting swirls\n- Colorful sprinkles\n- Candy decorations\n- Fresh fruit toppings\n- Creative lettering"
                    }
                    }, 
                    { 
                    "createParagraphBullets": {
                        "objectId": "Body4",
                        "textRange": {
                        "type": "ALL"
                        }, 
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE" 
                    }
                    },
                    {
                    "createSlide": {
                        "objectId": "Slide5",
                        "slideLayoutReference": {
                        "predefinedLayout": "TITLE_ONLY"
                        }, 
                        "placeholderIdMappings": [
                        {
                            "objectId": "Title5", 
                            "layoutPlaceholder": {
                            "type": "TITLE", 
                            "index": 0
                            }
                        }
                        ] 
                    }
                    },
                    {
                    "insertText": {
                        "objectId": "Title5",
                        "text": "Enjoy the Celebration!"
                    }
                    }
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
model = genai.GenerativeModel('gemini-1.5-pro-latest', tools=[create_slide])

@slideCreator.app.route('/')
def show_index():

    # Initialize service by authenticating user
    _initialize()
    create_presentation(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    chat = model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f'Can you create a blank slide?')

    context = { "some_text": response.text }
    return flask.render_template("index.html", **context)
