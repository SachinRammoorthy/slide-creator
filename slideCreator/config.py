"""
Development configuration.
https://flask.palletsprojects.com/en/2.2.x/config/
"""
from dotenv import load_dotenv
from slideCreator.functions import authenticate

load_dotenv()

APPLICATION_ROOT = '/'

CREDS = authenticate()


SYS_INSTRUCTION = \
"""
You are a google slides creation expert. You have mastered the Google Slides REST API and can
create the correctly formatted json encoding any presentation that your client can dream up!
"""