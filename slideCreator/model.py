import requests
from requests import Response


def call_generative_curl_request(api_key, sys_instr: str, context: str, user_request: str) -> Response:
    """Return a curl request as a string that contains all the valid information for the system."""

    model = "gemini-1.5-pro-latest"
    model_uri = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json",
            }

    data = {
        # "system_instruction": {
        #     "parts": [{"text": sys_instr}]
        # },
        "contents": [
            {   
                "parts":[
                {"text": context},
                {"text": user_request}
                ]
            },
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
        }
    }

    # command = "curl -X POST -H {headers} -d {data} {uri}"
    # return command.format(
    #     uri=model_uri,
    #     headers=headers,
    #     data=data
    # )
    print("making call")
    resp = requests.post(model_uri, json=data, headers=headers)
    print("call made")
    if resp.status_code >= 400:
        raise Exception(resp.__dict__)
    return resp


if __name__=="__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    print("hello ", os.environ["GOOGLE_API_KEY"])
    resp = call_generative_curl_request(api_key=os.environ["GOOGLE_API_KEY"],
                                        sys_instr="You are a cat. The json response you return should have a message attribute that contains your response in the style of a cat.",
                                        context="You have a deep voice, a normal 'meow' for you is actually a longer 'meeeooowwww'. The Json that you output should have one attribute called 'message'",
                                        user_request="What is the weather like today?")
    data = resp.json()
    print(data['candidates'][0]['content']['parts'][0]['text'])
