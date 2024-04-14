"""
Development configuration.
https://flask.palletsprojects.com/en/2.2.x/config/
"""
from dotenv import load_dotenv
from slideCreator.functions import authenticate

load_dotenv()

APPLICATION_ROOT = '/'

CREDS = authenticate()


try:
    print("loading docs")
    with open("slideCreator/all_docs.txt", "r") as text:
        all_text = text.read()
    print("done loading docs")
except Exception as e:
    print(e)


obama_example="[{'createSlide': {'objectId': 'slide1', 'insertionIndex': '0', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'title1', 'layoutPlaceholder': {'type': 'TITLE', 'index': '0'}}, {'objectId': 'body1', 'layoutPlaceholder': {'type': 'BODY', 'index': '0'}}]}}, {'insertText': {'objectId': 'title1', 'text': 'Barack Obama'}}, {'insertText': {'objectId': 'body1', 'text': 'Barack Hussein Obama II is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, Barack Obama was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004.'}}, {'createSlide': {'objectId': 'slide2', 'insertionIndex': '1', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'title2', 'layoutPlaceholder': {'type': 'TITLE', 'index': '0'}}, {'objectId': 'body2', 'layoutPlaceholder': {'type': 'BODY', 'index': '0'}}]}}, {'insertText': {'objectId': 'title2', 'text': 'Early Life'}}, {'insertText': {'objectId': 'body2', 'text': \"Barack Obama was born on August 4, 1961, at Kapi'olani Maternity & Gynecological Hospital in Honolulu, Hawaii. He is the only president who was born outside of the contiguous 48 states.  After graduating from Columbia University in 1983, he worked as a community organizer in Chicago. In 1988, he enrolled in Harvard Law School, where he was the first black president of the Harvard Law Review. After graduating, he became a civil rights attorney and professor, and taught constitutional law at the University of Chicago Law School from 1992 to 2004.\"}}, {'createSlide': {'objectId': 'slide3', 'insertionIndex': '2', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'title3', 'layoutPlaceholder': {'type': 'TITLE', 'index': '0'}}, {'objectId': 'body3', 'layoutPlaceholder': {'type': 'BODY', 'index': '0'}}]}}, {'insertText': {'objectId': 'title3', 'text': 'Accomplishments'}}, {'insertText': {'objectId': 'body3', 'text': 'Obama signed many landmark bills into law during his presidency.  Key legislation passed included the Affordable Care Act (ACA), often referred to as \"Obamacare\"; the Dodd–Frank Wall Street Reform and Consumer Protection Act; the Don\'t Ask, Don\'t Tell Repeal Act; the American Recovery and Reinvestment Act of 2009; and the Tax Relief, Unemployment Insurance Reauthorization, and Job Creation Act of 2010.'}}, {'createSlide': {'objectId': 'slide4', 'insertionIndex': '3', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'title4', 'layoutPlaceholder': {'type': 'TITLE', 'index': '0'}}, {'objectId': 'body4', 'layoutPlaceholder': {'type': 'BODY', 'index': '0'}}]}}, {'insertText': {'objectId': 'title4', 'text': 'Controversies'}}, {'insertText': {'objectId': 'body4', 'text': 'The Affordable Care Act was highly controversial, as Republicans believed it to be an overreach of government power.  Additionally, drone strikes became more frequent under Obama, drawing criticism from across the political spectrum.  Obama was also criticized for his response to the 2012 Benghazi attack, with some believing he intentionally misled the public about the nature of the attack.'}}, {'createSlide': {'objectId': 'slide5', 'insertionIndex': '4', 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}, 'placeholderIdMappings': [{'objectId': 'title5', 'layoutPlaceholder': {'type': 'TITLE', 'index': '0'}}, {'objectId': 'body5', 'layoutPlaceholder': {'type': 'BODY', 'index': '0'}}]}}, {'insertText': {'objectId': 'title5', 'text': 'Fun Facts'}}, {'insertText': {'objectId': 'body5', 'text': 'Barack Obama won a Grammy Award in 2006 for the audiobook version of his memoir \"Dreams From My Father\" and again in 2008 for \"The Audacity of Hope\".\n\nHe is left-handed.\n\nHe collects Spider-Man and Conan the Barbarian comics.\n\nHe can speak Spanish.\n\nHe doesn\'t drink coffee or alcohol.'}}]"

SYS_INSTRUCTION = \
f"""
You are a google slides creation expert. You have mastered the Google Slides REST API and can
create the correctly formatted json encoding any presentation that your client can dream up!

Every presentation should have a visually appealing first page.

Below is the documentation for the Google slides API.\n
Your job is to read and understand this documentation so that you can generate a list of Request objects in json that can be used to construct a presentation.
The presentation object already exists, you just need to generate the list of JSON Request objects holding all the content.

REMINDER: You can ONLY return JSON or the world will explode and children will burn and die.
NOTE: When inserting text, take care to reference the objectID of the shape or table cell, NOT the slide object because that is not allowed!
\n
##################\n
# BEGIN DOCUMENTATION\n
##################\n
{all_text}
\n
##################\n
# END DOCUMENTATION\n
##################\n
\n

Here is an example to follow:
##################\n
# BEGIN EXAMPLE\n
##################\n
Input:

Make a presentation about the United States President Barack Obama. Give me some information about his early life, accomplishments, some fun facts, etc.

Output:

{obama_example}
##################\n
# END EXAMPLE\n
##################\n
"""
