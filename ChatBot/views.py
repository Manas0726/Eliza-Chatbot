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
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

#rasa run --enable-api
model_path = './RasaBot/models'
agent = Agent.load(model_path)


def heropage(request):
    #return render(request,"index.html")
    return render(request,"index.html")

@csrf_protect
def feedback(request):
    if request.method=='POST':
        uname=request.POST.get('name')
        uemail=request.POST.get('email')
        umessage=request.POST.get('message')
        if uname and uemail and umessage:
            subject = ('hey this is feedback to you from '+uname)
            message = (umessage)
            sender_email = (uemail)
            recipient_email = 'elizagpn@gmail.com'

            send_mail(
            subject,
            'Sender email: {}\n\n{}'.format(sender_email, message),
            sender_email,
            [recipient_email],
            fail_silently=False
            ) 
            messages.success(request,'Thanks For Your FeedBack.')
            return redirect('home')
        else:
            messages.success(request,'Please Fill in all Fields')
            return redirect('home')
    return render (request,'home')      

# def send_email1(request):
#     if request.method == 'POST':
#         subject = ('hey this is feedback to you')
#         message = request.POST.get('message', '')
#         sender_email = request.POST.get('email', '')
#         recipient_email = 'eliza2023.cm@gmail.com'
        
#         send_mail(
#             subject,
#             'Sender email: {}\n\n{}'.format(sender_email, message),
#             sender_email,
#             [recipient_email],
#             fail_silently=False,
#         )
#         #return HttpResponseRedirect('/success/')
        
#     return render(request, 'email_form.html')

@csrf_protect
def Signuppage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        pass2=request.POST.get('cpass')
        if uname and email and pass1 and pass2:
            try:    
                if pass1!=pass2:
                    #return HttpResponse("Your Pasword and Confirm Passsword Are not same")
                    messages.success(request,'Your password and Confirm Password Are not Same')
                else:
                    if User.objects.filter(username=uname).first():
                        messages.success(request,'Username is Already Taken')
                        return redirect('signup') 
                    if User.objects.filter(email=email).first():
                        messages.success(request,'Email is Already Used')
                        return redirect('signup')
                    else:     
                        my_user=User.objects.create_user(uname,email)
                        my_user.set_password(pass1)
                        my_user.save()
                        auth_token=str(uuid.uuid4())
                        profile_obj=Profile.objects.create(user=my_user,auth_token=auth_token)
                        profile_obj.save()
                        messages.success(request,'verification link send to your email')
                        send_mail_signup(email,auth_token)
                        
                                    
            except Exception as e:
                print(e)
                return redirect('signup')
        else:
            messages.error(request, 'Please fill in all fields')         
    return render (request,'signup.html')  
      
@csrf_protect
def Loginpage(request):
    try:
        if request.method=='POST':
            username1= request.POST.get('username')
            password1= request.POST.get('pass')
            user_obj=User.objects.filter(username=username1).first()
            if user_obj is None:
                 #return HttpResponse('NO user Found Please Sign-In First to continue')
                 messages.success(request,'No User Found Please Sign-In First to Continue')
                 return redirect('signup')
       
            Profile_obj=Profile.objects.filter(user=user_obj).first()
       
            if not Profile_obj.is_verified:
                 #return HttpResponse('Profile Is Not verified Plz verified Your Profile')
                 messages.success(request,'Account is not verified Please Verified Your Account') 
                 return redirect('signup')
       
            user=authenticate(request,username=username1,password=password1) 
            if user is not None:
                 login(request,user)
                 return  render(request,'Chat.html') 
            else:
                messages.success(request,'Wrong Password')
                return redirect('login') 
    except Exception as e:
        print(e)
        return redirect('login')          
     
    return render (request,'login.html')
@csrf_protect
def super_login(request):
    try:
         if request.method=='POST':
            username2= request.POST.get('username')
            password2= request.POST.get('pass')
            user = authenticate(request, username=username2, password=password2)
         if user is not None and user.is_superuser:
            login(request, user)
            return  render(request,'admin.html') 
         else:
            messages.success(request, 'Invalid Admin username or password')
            return redirect('superlogin')  
            #return render (request,'superlogin.html')   
    except Exception as e:
        print(e)
        return render(request,'superlogin.html') 
    
def Logoutpage(request):
    logout(request)
    return redirect('home')

@csrf_protect
def Tokenpage(request):
    return render(request,'token.html')
@csrf_protect
def verify(request , auth_token):
    try:
        profile_obj= Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                 messages.success(request,'Yout Account Has Been Already verified')
                # return HttpResponse('Your Account has been already verified.')
                 return redirect('/login')
            profile_obj.is_verified= True
            profile_obj.save()
            messages.success(request, 'Your Account has been verified.')
            return redirect('/login')
        else:
            return redirect('')
    except Exception as e:
        print(e) 
        return redirect('')   
            

def send_mail_signup(email,token):
    subject='Your Account Needs to be verified'
    message=f'paste the link to Verify Your Account http://13.126.203.189:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject , message, email_form , recipient_list)
             

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

def jsonList(request):
    with open('static/javascript/keyword.json') as f:
        data = json.load(f)
    context = {'data': data}
    return render(request, 'jsonList.html', context)




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
