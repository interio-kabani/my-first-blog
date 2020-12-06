from django.shortcuts import render

# Create your views here.
import cv2 
import time
from mysite1 import settings
from django.views.generic import TemplateView
import sys
import matplotlib.pyplot as plt
from PIL import Image
from django.http import HttpResponse
import os
import io




class PredView(TemplateView):
    def __init__(self):
        self.params = {"Are you ready?"}
        self.params = {"none"}

    def get(self,request):
        return render(request, 'pred/index.html', {'app': self.params, 'app2': self.params})
        return render(request, 'pred/index.html', {'app2': self.params})
    def post(self, request):
        app = detect_face()
        app2 = detect_min()
        #image = point_plot()
        return render(request, 'pred/index.html', {'app': app, 'app2': app2})
        #return render(request, 'pred/index.html', {'app2': app2})


#def index(request):
    #app = detect_face()
    #return render(request, 'pred/index.html', {'app': app})
#requestをとっているのはurlsでimportされてリクエストされるから。つまりリクエストされたら発動するってことだと思う   
#requestとはユーザから受け取ったデータのすべて
#djangotemplateにへんすうをひょうじするには{{}}が必要

# カスケードファイルを指定して、検出器を作成
#cascade_file = settings.CASCADE_FILE_PATH
cascade_file = "haarcascade_frontalface_alt2.xml"
# (1)カスケード分類器のファイルを読み込むわよ
cascade = cv2.CascadeClassifier(cascade_file)

# (2)カメラを読み込んでグレイスケールに変換
#face1 = cv2.imread("WIN_20200531_13_35_23_Pro.jpg")
#cap = cv2.VideoCapture(0)
result_point = []
time_past = [1,2,3,4,5,6]
def detect_face():
    result_point.clear()
    cap = cv2.VideoCapture(0)
    start = time.time()
    point = 0
    #result_point = []
    time_past = [1,2,3,4,5,6]
    #assert os.path.isfile(cascade), 'haarcascade_frontalface_default.xml がない'
    for i in range(6):
        #毎回カメラ使うから熱くなるかも
        #採点部分をhtmlにさせればリアルタイムぽくなるかも
        ret, frame = cap.read(0)
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_list = cascade.detectMultiScale(img_gray,scaleFactor = 1.2, minNeighbors = 5)
        if len(face_list) == 1:
            point = point + 1
        time.sleep(1)
        total = time.time() - start
        result = point / total * 100
        result_point.append(result)
    
    return result_point
def point_plot():
    image = plt.figure()
    plt.plot(time_past, result_point)
    plt.title("point")
    plt.ylabel("your point")
    plt.xlabel("time")

    save_dir = '/static/media/'

    plt.savefig(os.path.join(save_dir, 'image.png'))

    #image.savefig("image")
    response = HttpResponse(content_type="image/png")
    #image.save(response, "PNG")
    return response

def detect_min():
    point_min = result_point.index(min(result_point))
    
        #print(result_point)
      
    #plt.plot(time_past, result_point)
    #plt.title("point")
    #plt.ylabel("your point")
    #plt.xlabel("time")
    #plt.show()
    #return result_point
    return point_min