from django.http import HttpResponse  # used to give response to browser(text based)
from django.shortcuts import render
from django.http import JsonResponse
import json
from rasa.core.agent import Agent
import requests
import io
import base64
import textwrap
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import json

#rasa run --enable-api
model_path = './RasaBot/models'
agent = Agent.load(model_path)


def heropage(request):
    #return render(request,"index.html")
    return render(request,"Hero.html")

def chatpage(request):
    return render(request,"Chat.html")

def adminpage(request):
    return render(request,"admin.html")

def add(request):
    return render(request,"add.html")

def updateAnswer(request):
    return render(request,"updateAnswer.html")

def delete(request):
    return render(request,"delete.html")

def updateKeyword(request):
    return render(request,"updateKeyword.html")


def rasachat(request, inputValue):
    api_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user", "message": inputValue}

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # raise exception for non-200 responses
        response_data = response.json()
        bot_message = response_data[0]["text"]
    except requests.exceptions.RequestException as e:
        # handle HTTP or network errors
        bot_message = f"Error: {str(e)}"
    except (ValueError, KeyError, IndexError):
        # handle invalid JSON or missing data errors
        bot_message = "Sorry, there was an error processing your request."
    return JsonResponse({"msg": bot_message})


def buttonmsg(request,buttonName):
    #for analytics
    with open('static/javascript/Analysis1.json','r') as f:
        ana = json.load(f)
    ana[buttonName]+=1
    with open('static/javascript/Analysis1.json', 'w') as f:
        json.dump(ana, f)

    with open('static/javascript/keyword.json','r') as f:
        data = json.load(f)
    mylist=[]
    for i in data[buttonName]:
        mylist.append(i)
    mylist.append(buttonName)
    mylist_json = json.dumps(mylist)
    return JsonResponse({'mylist':mylist_json})

def majorKeywordRetrival(request):
    with open('static/javascript/keyword.json','r') as f:
        data = json.load(f)
    MajorKeyword=[]
    for i in data:
        MajorKeyword.append(i)
    MajorKeyword_json = json.dumps(MajorKeyword)
    return JsonResponse({'MajorKeyword':MajorKeyword_json})
    

     
def subbuttonmsg(request,corekey,content):
    #fro analytics
    with open('static/javascript/Analysis2.json','r') as f:
        ana = json.load(f)
    ana[corekey][content]+=1
    with open('static/javascript/Analysis2.json', 'w') as f:
        json.dump(ana, f)

    with open('static/javascript/keyword.json','r') as f:
        data = json.load(f) 
    text=data[corekey][content]
    subbuttonresponse = format_text(text)    
    ans=json.dumps(subbuttonresponse)
    return JsonResponse({'subbuttonresponse':ans})


def keywordMsg(request,selectedValue):
    i = 1
    with open('static/javascript/keyword.json','r') as f:
        data = json.load(f) 
    KeywordResponseList=[]
    for key, value in data[selectedValue].items():
        
        a= str(i)+ ")" + key + " : "+value + "\n"
        KeywordResponseList.append(a)
        i += 1
    KeywordResponseList_json = json.dumps(KeywordResponseList)
    return JsonResponse({'KeywordResponseList':KeywordResponseList_json})

def addElement(request,subKeyVal,inputField,textField):
    with open('static/javascript/keyword.json','r')as f:
        data=json.load(f)
    with open('static/javascript/Analysis2.json','r')as f:
        ana=json.load(f)

    if subKeyVal in data and inputField in data[subKeyVal]:
        a="Error: Subkeyword already exists."
        return JsonResponse({"success": False, "message": "Subkeyword already exists."})

    for i in data:
        if(subKeyVal==i):
            data[subKeyVal][inputField]=textField
            ana[subKeyVal][inputField]=0
            a="Added successfully"

    with open('static/javascript/Analysis2.json','w')as f:
        json.dump(ana,f)
    with open('static/javascript/keyword.json', 'w') as f:
        json.dump(data, f)
    
    return JsonResponse({"success": True, "message": "Subkeyword added successfully."})


def deleteElement(request,subKeyVal,inputField):
    
    with open('static/javascript/keyword.json','r')as f:
        data=json.load(f)
    with open('static/javascript/Analysis2.json','r')as f:
        ana=json.load(f)

    del data[subKeyVal][inputField]
    del ana[subKeyVal][inputField]

    with open('static/javascript/Analysis2.json','w')as f:
        json.dump(ana,f)
    with open('static/javascript/keyword.json', 'w') as f:
        json.dump(data, f)
    
    return JsonResponse({"message": "keyword deleted successfully."})


def keyupdate(request, subKeyVal, inputField, updatedKey):
    with open('static/javascript/keyword.json','r')as f:
        data=json.load(f)
    with open('static/javascript/Analysis2.json','r')as f:
        ana=json.load(f)

    ana[subKeyVal][updatedKey]=ana[subKeyVal][inputField]
    del ana[subKeyVal][inputField]
    data[subKeyVal][updatedKey]=data[subKeyVal][inputField]
    del data[subKeyVal][inputField]

    with open('static/javascript/keyword.json', 'w') as f:
        json.dump(data, f)
    with open('static/javascript/Analysis2.json', 'w') as f:
        json.dump(ana, f)
    return JsonResponse({"message": "keyword updated successfully."})

def ansupdate(request,subKeyVal, inputField, updatedAnswer):
    with open('static/javascript/keyword.json','r')as f:
        data=json.load(f)

    data[subKeyVal][inputField]=updatedAnswer

    with open('static/javascript/keyword.json', 'w') as f:
        json.dump(data, f)
    return JsonResponse({"message": "Answer updated successfully."})


#---------------Formating---------------

import string
import nltk
import spacy

nlp = spacy.load("en_core_web_sm")


def is_bullet_point(text):
    bullet_tokens = ['*', '-']
    for sent in nltk.sent_tokenize(text):
        for token in nltk.word_tokenize(sent):
            if token.startswith(tuple(bullet_tokens)):
                return True
    return False


def format_text(text):
    # Add bullet points to the text
    lines = text.split('\n')
    bulleted_lines = []
    for line in lines:
        if line.strip() != '':
            if ':' in line:
                # Add a bullet point before each item in the list on a new line,
                # with the initial letter of each item capitalized
                line_parts = line.split(':')
                prefix = line_parts[0].strip().capitalize()
                items = line_parts[1].strip().split(',')
                bulleted_lines.append(prefix + ':')
                for item in items:
                    bulleted_lines.append('\t- ' + item.strip().capitalize())
            else:
                # Remove the bullet point from the beginning of the line
                if line.count(',') >= 2:
                    words = line.split(',')
                    bulleted_line = ''
                    for i in range(len(words)):
                        word = words[i].strip()
                        if word != '':
                            if i == 0:
                                if line.count(',,') >= 1:
                                    word_parts = word.split(',,')
                                    first_word = word_parts[0].strip().capitalize()
                                    second_word = word_parts[1].strip().capitalize()
                                    bulleted_lines.append(first_word.capitalize() + ':')
                                    bulleted_lines.append('\t- ' + second_word)
                                    break
                                else:
                                    bulleted_line += '\t- ' + word.capitalize()
                            else:
                                if bulleted_line != '':
                                    bulleted_lines.append(bulleted_line.strip() + ',')
                                    bulleted_line = ''
                                bulleted_line += '\t- ' + word.capitalize()
                    if bulleted_line != '':
                        bulleted_lines.append(bulleted_line.strip() + ',')
                else:
                    bulleted_lines.append(line.strip().capitalize())

    # Join the lines to form the final text
    bulleted_text = '\n'.join(bulleted_lines)

    # Return the final formatted text
    return bulleted_text



#----------------Analytics------------------
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import os
import time
matplotlib.use('Agg')




# def MajorKeywordAnalysis(request):
#     with open('static/javascript/Analysis1.json','r') as f:
#         ana = json.load(f)
#     button_labels = list(ana.keys())
#     click_counts = list(ana.values())

#     plt.bar(button_labels, click_counts)
#     # plt.xlabel('Button Labels')
#     plt.ylabel('Frequently Clicked')
#     img_bytes = io.BytesIO()
#     plt.title('Major Keyword Analysis')
#     file_name = 'scatter_{}.png'.format(int(time.time()))
#     plt.savefig(file_name, format='png')
#     with open(file_name, 'rb') as f:
#         image_data = f.read()

#     # Pass the image data to the template context as base64-encoded bytes
#     image_data = base64.b64encode(image_data).decode('utf-8')
#     context = {'image_data': image_data}
#     return render(request, 'adminAnalytics.html', context)


import io
import base64
from django.http import HttpResponse
import matplotlib.pyplot as plt

def MajorKeywordAnalysis(request):
    with open('static/javascript/Analysis1.json','r') as f:
        ana = json.load(f)
    button_labels = list(ana.keys())
    click_counts = list(ana.values())

    plt.bar(button_labels, click_counts)
    # plt.xlabel('Button Labels')
    plt.ylabel('Frequently Clicked')
    plt.title('Major Keyword Analysis')

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()  # Close the current figure

    # Get the image data from the bytes buffer
    image_data = buffer.getvalue()
    buffer.close()

    # Convert the image data to base64-encoded bytes
    image_data = base64.b64encode(image_data).decode('utf-8')

    # Pass the image data to the template context
    context = {'image_data': image_data}
    return render(request, 'adminAnalytics.html', context)




def SubKeywordAnalysis(request, major):
    with open('static/javascript/Analysis2.json','r') as f:
        ana = json.load(f)
    button_labels = list(ana[major].keys())
    click_counts = list(ana[major].values())

    # Wrap long labels into multiple lines
    wrapped_labels = [textwrap.fill(label, 10) for label in button_labels]

    plt.bar(wrapped_labels, click_counts)
    # plt.xlabel('Button Labels')
    plt.ylabel('Frequently Clicked')
    plt.title(major + " Analysis")

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()  # Close the current figure

    # Get the image data from the bytes buffer
    image_data = buffer.getvalue()
    buffer.close()

    # Convert the image data to base64-encoded bytes
    image_data = base64.b64encode(image_data).decode('utf-8')

    # Pass the image data to the template context
    context = {'image_data': image_data}
    return render(request, major + ".html", context)
