from django.shortcuts import render
import json
from django.http import HttpResponse
import requests
from imports.traversal import trains
from firebase import firebase
from imports.nltk_splitter import ParseTheInput
fireBase = firebase.FirebaseApplication('https://sail-857f9.firebaseio.com/', None)
result = fireBase.get('', None)

'''
def threeStepsAdd(request):
    requestedJson = request.GET['json']
    x = json.loads(requestedJson)
    url = 'http://localhost:8080/'
    creds = '?user_name=trial&password=karikanda4&format=json'
    r = requests.post(url + creds, data={"api_key": "BLAH", "password": "blah", "user_name": x['package']})
    creds = '?password=BLAH&format=json&user_name=' + x['package']

    r = requests.post(url + creds, data={"table_name": x['activity']})

    creds = creds + '&json={"table_name":"'+x['activity']+'"}'
    r.request = requests.post(url+creds,data=)
    return HttpResponse(x)
'''


def trainThisApp(request):
    x = request.GET['json']
    x = json.loads(x)
    t = trains(result)
    t.TrainOne(x['package'])
    return HttpResponse(x)


def predictThisLevel(request):
    x = request.GET['json']
    x = json.loads(x)
    package = x['package']
    current_view = x['view']
    url = 'http://localhost:8080/predict/'
    creds = '?password=blah&format=json&user_name=' + str(
        package) + '&json={"table_name":"' + current_view + '","message":"' + x['message'] + '"}'
    r = requests.get(url + creds)
    print r
    print x['message']
    s = ParseTheInput(x['message'])
    j = json.loads(r.text)
    j = json.loads(j)
    j['split_string'] = s.find_partition()
    return HttpResponse(json.dumps(j))
