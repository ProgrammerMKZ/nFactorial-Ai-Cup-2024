from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .forms import ImageForm
import os

current_dir = os.getcwd()

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def diagnostics(request):
    return render(request, 'main/register-light.html')

def LLM(request):
    return render(request, 'main/main-page.html')

def Pneumonia(request):
    return render(request, 'main/main-page2.html')

def MRI(request):
    return render(request, 'main/main-page1.html')

def symptoms(request):
    if request.method == "POST": # если прилетел пост запрос
        text_input = request.POST.get("text-input") # из формы получаем значение инпута с названием text-input
        payload = {"inputs": text_input, 
                   "wait_for_model": True}
        
        API_URL = "https://api-inference.huggingface.co/models/ajtamayoh/Symptoms_to_Diagnosis_SonatafyAI_BERT_v1"
        headers = {"Authorization": "Bearer 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"}
        response = requests.post(API_URL, headers=headers, json=payload)
        
        result = response.json()
        if type(result) == dict:
                for i in result.keys():
                    if i == 'error':
                        return render(request, 'main/symptoms.html', {'error_msg':'Cannot process this request'})
        
        result_arr = []
        for i in result[0]:
            if float(i['score']) > 0.01:
                result_arr.append(i['label'] + ' ' + str(round(i['score']*100, 1)) + "%")
        return render(request, 'main/symptoms.html', {'result_arr':result_arr})
            
    return render(request, 'main/symptoms.html')

def cancer(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            API_URL = "https://api-inference.huggingface.co/models/dima806/brain_tumor_detection"
            headers = {"Authorization": "Bearer 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"}
            print(current_dir+img_obj.image.url)
            with open(current_dir+img_obj.image.url, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            result = response.json()
            if type(result) == dict:
                for i in result.keys():
                    if i == 'error':
                        return render(request, 'main/cancer.html', {'form': form, 'img_obj': img_obj, 
                                                               'error_msg':'Cannot process this image'})
            result_arr = []
            for i in result:
                result_arr.append(i['label'] + ' ' + str(round(i['score']*100, 1)) + "%")
                

            return render(request, 'main/cancer.html', {'form': form, 'img_obj': img_obj, 'result_arr':result_arr})

    form = ImageForm()
    return render(request, 'main/cancer.html', {'form':form})

def pneumonia(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            API_URL = "https://api-inference.huggingface.co/models/nickmuchi/vit-finetuned-chest-xray-pneumonia"
            headers = {"Authorization": "Bearer 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"}

            print(current_dir+img_obj.image.url)
            with open(current_dir+img_obj.image.url, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            result = response.json()
            print(result)
            if type(result) == dict:
                for i in result.keys():
                    if i == 'error':
                        return render(request, 'main/pneumonia.html', {'form': form, 'img_obj': img_obj, 
                                                               'error_msg':'Cannot process this image'})
                
                
            result_arr = []
            for i in result:
                  result_arr.append(i['label'] + ' ' + str(round(i['score']*100, 1)) + "%")
                

            return render(request, 'main/pneumonia.html', {'form': form, 'img_obj': img_obj, 'result_arr':result_arr})

    form = ImageForm()
    return render(request, 'main/pneumonia.html', {'form':form})

