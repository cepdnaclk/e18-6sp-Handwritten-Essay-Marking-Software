import os #pip install azure-cognitiveservices-vision-computervision
import io
import json
import time
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests #pip install requests
from PIL import Image,ImageDraw,ImageFont

credentials = json.load(open('credentials.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']

cv_client = ComputerVisionClient(ENDPOINT,CognitiveServicesCredentials(API_KEY))
local_file = './Sample.jpg' 

response = cv_client.read_in_stream(open(local_file,'rb'),language='en',raw=True)
operationLocation = response.headers['Operation-Location']
operation_id = operationLocation.split('/')[-1]
time.sleep(5)
result = cv_client.get_read_result(operation_id)

print(result.status)

if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print(line.text)
