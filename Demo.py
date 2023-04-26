import requests

# url = 'http://localhost:5005/model/parse'
# data = {
#     'text': 'Hello, how are you?'
# }

# response = requests.post(url, json=data)
# print(response.json())

# def rasachat(inputValue):
#     api_url = "http://localhost:5005/webhooks/rest/webhook"
#     payload = {"sender": "user", "message": inputValue}

#     try:
#         response = requests.post(api_url, json=payload)
#         response.raise_for_status()  # raise exception for non-200 responses
#         response_data = response.json()
#         bot_message = response_data[0]["text"]
#     except requests.exceptions.RequestException as e:
#         # handle HTTP or network errors
#         bot_message = f"Error: {str(e)}"
#     except (ValueError, KeyError, IndexError):
#         # handle invalid JSON or missing data errors
#         bot_message = "Sorry, there was an error processing your request."

#     return ({"msg":bot_message})

# print(rasachat("Are you a human?"))
import json
import matplotlib as plt
def MajorKeywordAnalysis():
    with open('static/javascript/Analysis1.json','r')as f:
        ana=json.load(f)
    button_labels = list(ana.keys())
    click_counts = list(ana.values())
    plt.pie(click_counts, labels=button_labels)
    plt.title('Major Keyword Analysis')
    plt.show()
MajorKeywordAnalysis()