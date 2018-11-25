from django.http import JsonResponse,HttpResponse
from django.core import serializers
import json
def response_succeess(data):
    #响应成功；message:说明
    #           data:数据
    message="成功"
    content={
        "success":"true",
        "message":message,
        "data":data
    }
    # print("content",content)
    # print(type(content))
    return JsonResponse(content)

def response_failed(message):
    content={
        "success":"false",
        "message":message,
    }
    return JsonResponse(content)