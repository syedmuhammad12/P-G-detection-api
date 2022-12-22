from fileinput import filename
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import skimage
import wget
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import random
import urllib
import string
import base64
from tensorflow.keras.models import load_model
from django.conf import settings
import serial
import time
import base64
import cv2
import numpy as np
from fyp_project.defect_algos.cap_seated_lg import cap_seated_lg
from quality_assurance_system.models import *
from .defect_algos.cap_seated_lg import cap_seated_lg
from .defect_algos.cap_seated_md import cap_seated_md
from .defect_algos.cap_sealed_lg import cap_sealed_lg
from .defect_algos.cap_sealed_md import cap_sealed_md
from .defect_algos.cap_cocked_lg import cap_cocked_lg
from .defect_algos.cap_cocked_md import cap_cocked_md
from .defect_algos.product_on_bottle_lg import product_on_bottle_lg
from .defect_algos.product_on_bottle_md import product_on_bottle_md
from django.http import HttpResponse
from django.views.generic import View
from .utils import generateEtamuReport 
import mimetypes
import os
import pandas as pd
from django.core.mail import EmailMessage
# from django.conf import settings

from django.http import FileResponse, Http404

def pdf_view(path):
    return FileResponse(open(path, 'rb'), content_type='application/pdf')


def generateEtamuReportView(request):

    generateEtamuReport()

    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'report.pdf'
    # Define the full file path
    filepath = BASE_DIR + '/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

    # return HttpResponse(pdf, content_type='application/pdf')


def emailEtamuReportView(request):

    # start_date = request.GET.get('start_date')
    # end_date = request.GET.get('end_date')

    generateEtamuReport()

    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'report.pdf'
    # Define the full file path
    filepath = BASE_DIR + '/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')

    subject = "E-Tamu Report"
    message = "PDF Attached Below"
    emails = ["aliabbaspanjwani7@gmail.com", request.GET.get('email')]
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    # mail.attach('Report.pdf', pdf_view(filepath), 'application/pdf')
    mail.attach_file(filepath)
    
    try:
        mail.send(fail_silently = False)
        # return HttpResponse("Mail Sent")
        messages.success(request, 'Report emailed successfully.')
    except:
        # return HttpResponse("Mail Not Sent")
        messages.success(request, 'An error occured while emailing the report.')

    return redirect('home')


def rotate_motor(request):

    ser = serial.Serial( port="COM7", 
             baudrate=9600, 
             bytesize=8, 
             timeout=1,
             stopbits=serial.STOPBITS_ONE )

    time.sleep(3)

    ser.write("P|0400".encode('Ascii'))

    ser.close() 

    return JsonResponse({"rotate_45" : "done"}, status=200)

def align_camera(request):
    
    bottle_size = request.POST.get('bottle_size')

    ser = serial.Serial( port="COM6", 
            baudrate=9600, 
            bytesize=8, 
            timeout=1,
            stopbits=serial.STOPBITS_ONE )

    time.sleep(3)



    if bottle_size == "md" and request.session.get('cam_pos', None) is None:
        ser.write("C|-3740".encode('Ascii'))
    elif bottle_size == "lg" and request.session.get('cam_pos', None) is None:
        ser.write("C|-4080".encode('Ascii'))
    elif bottle_size == "md" and request.session.get('cam_pos', None) == "lg":
        ser.write("C|340".encode('Ascii'))
    elif bottle_size == "lg" and request.session.get('cam_pos', None) == "md":
        ser.write("C|-340".encode('Ascii'))


    request.session["cam_pos"] = bottle_size


    ser.close()

    return JsonResponse({"camer_align" : "done"}, status=200)

def redirect_to_home(request):
    return redirect('home')

@login_required(login_url='login')
def team(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/team.html", {'showURL': urlObject})

@login_required(login_url='login')
def faqs(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/faqs.html", {'showURL': urlObject})

@login_required(login_url='login')
def about(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/about.html", {'showURL': urlObject})

@login_required(login_url='login')
def index(request):
    urlObject = request.get_host() + request.path
    count_of_total_bottles = Bottle.objects.count()
    count_of_acceptable_bottles = Bottle.objects.filter(result="Acceptable").count()
    count_of_unacceptable_bottles = Bottle.objects.filter(result="Unacceptable").count()

    last_6_months_numbers = [(datetime.today().month - i - 1) % 12 + 1 for i in range(6)]
    last_6_months_data = {}
    # last_6_months_numbers.reverse()
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    current_month = datetime.today().month
    current_year = datetime.today().year
    print("************* dates *****************")
    for i in range(-1,5):
        start_date = datetime(current_year,current_month,1)+relativedelta(months=-(i+1))
        end_date = datetime(current_year,current_month,1)+relativedelta(months=-i) 
        # end_date = str(end_date)
        # end_date = end_date.split(" ")[0]
        # end_date = end_date.split("-")
        # end_date = end_date[0]+"-"+end_date[1]+"-"
        last_6_months_data[month_names[last_6_months_numbers[i+1]-1]] = {"acceptable":Bottle.objects.filter(result="Acceptable", created_at__date__range=(start_date, end_date)).count(), "unacceptable":Bottle.objects.filter(result="Unacceptable", created_at__date__range=(start_date, end_date)).count()}

        print("from = {}, end = {}, total = {}".format(start_date, end_date, Bottle.objects.filter(created_at__date__range=(start_date, end_date)).count()))

    print("*********** here is data **************")
    print(last_6_months_data)


    params = {
        "count_of_total_bottles": count_of_total_bottles, 
        "count_of_acceptable_bottles": count_of_acceptable_bottles, "count_of_unacceptable_bottles": count_of_unacceptable_bottles,
        "percentage_of_unacceptable_bottles": (count_of_unacceptable_bottles/count_of_total_bottles)*100,
        "percentage_of_acceptable_bottles": (count_of_acceptable_bottles/count_of_total_bottles)*100,
        "last_6_months_data": last_6_months_data
        }

    return render(request, "pages/home.html", {'showURL': urlObject, "params": params})


@login_required(login_url='login')
def quality_check_page(request):
    urlObject = request.get_host() + request.path
    return render(request, "pages/quality_check.html", {'showURL': urlObject})


@login_required(login_url='login')
def results_page(request):
    urlObject = request.get_host() + request.path
    # range_n = range(296)
    bottles = Bottle.objects.all()
    return render(request, "pages/results.html", {'showURL': urlObject, 'bottles': bottles})

def get_bottle_details(request):
    bottle_id = request.POST.get('bottle_id')
    bottle = Bottle.objects.filter(id=bottle_id)[0]
    params = getAllEntriesForBottle(bottle)

    return render(request, "pages/result_modal_body.html", params)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfull.')
                return redirect('home')
            else:
                messages.error(request, 'Username OR password is incorrect')

        return render(request, 'auth/login.html')


def saveBottleDefectEntry(defects):

    final_result = evaluate_final_result(defects)

    bottle = Bottle(result=final_result)
    bottle.save()

    for defect in defects:
        bottle_defect = BottleDefect(bottle=bottle, defect_name=defect["defect_name"], result=defect["defect_result"])
        bottle_defect.save()

    return bottle


def inspect(request):
    defects = []
    defects = cap_seated_defect_check(request.POST.get('bottle_size'), defects)
    if(defects[0]["defect_result"] != "Unacceptable"):
        defects = cap_cocked_defect_check(request.POST.get('bottle_size'), defects)
    else:
        defects.append({"defect_name" : str(len(defects)+1)+". Cap Cocked", "defect_result" : "Acceptable"})
    
    defects = cap_sealed_defect_check(request.POST.get('bottle_size'), defects)
    defects = product_on_bottle_check(request.POST.get('bottle_size'), defects)


    print("*********** final result +++++++++++++")
    print(defects)

    params = getAllEntriesForBottle(saveBottleDefectEntry(defects))

    return render(request, "pages/result_modal_body.html", params)


def evaluate_final_result(defects):
    acceptable = True
    for defect in defects:
        if defect["defect_result"] != "Acceptable":
            acceptable = False
    
    if acceptable:
        return "Acceptable"
    else:
        return "Unacceptable"


def cap_seated_defect_check(bottle_size, defects):
    front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        cap_seated = cap_seated_md(front_image)
    else:
        cap_seated = cap_seated_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Cap Not Seated", "defect_result" : cap_seated})

    return defects



def product_on_bottle_check(bottle_size, defects):
    front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        product_on_bottle = product_on_bottle_md(front_image)
    else:
        product_on_bottle = product_on_bottle_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Product On Bottle", "defect_result" : product_on_bottle})

    return defects



def cap_sealed_defect_check(bottle_size, defects):
    front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        cap_sealed = cap_sealed_md(front_image)
    else:
        cap_sealed = cap_sealed_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Cap Not Sealed", "defect_result" : cap_sealed})

    return defects



def cap_cocked_defect_check(bottle_size, defects):
    front_image = "./defect_algos/inp_img_1.jpg"
    # front_image = "fyp_project/defect_algos/inp_img_1.jpg"
    if(bottle_size == "md"):
        cap_cocked = cap_cocked_md(front_image)
    else:
        cap_cocked = cap_cocked_lg(front_image)

    defects.append({"defect_name" : str(len(defects)+1)+". Cap Cocked", "defect_result" : cap_cocked})

    return defects


def logoutUser(request):
    logout(request)
    messages.success(request, 'logout successfull.')
    return redirect('login')


def getAllEntriesForBottle(bottle_obj):
    bottle_defects = BottleDefect.objects.filter(bottle_id = bottle_obj)

    entries = []
    for bottle_defect in bottle_defects:
        temp = {}
        temp["defect_name"] = bottle_defect.defect_name
        temp["defect_result"] = bottle_defect.result
        
        entries.append(temp)

    params = {"result" : bottle_obj.result, "entries" : entries}

    return params


def save_img_on_server(request):
    i = request.POST.get('i')

    base64_img = request.POST.get('img_dataUrl')
    encoded_data = base64_img.split(',')[1]

    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    target_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    my_pic_path = "fyp_project/defect_algos/inp_img_" + str(i) + ".jpg"
    img_saved = cv2.imwrite(my_pic_path, target_img)
    print("image saved {} ".format(img_saved))

    return JsonResponse({"result" : "image saved {} ".format(img_saved)}, status=200)


def img_model_inspect(request):
    
    f = urllib.request.urlopen(request.POST.get('img'))
    myfile = f.read()
    r = base64.decodebytes(myfile)
    q = np.frombuffer(r, dtype="uint8")
    img = q.astype(np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = cv2.resize(img, (224, 224), 3)
    # print("start")
    # np_img = np.array(myfile)
    # img = cv2.resize(q, (224, 224))
    model = load_model('../mobilenetV2_original.h5')
    img = img / 255.0
    
    img = img.reshape(1,224,224, 3)
    label = model.predict(img)
    p=np.argmax(label)
    paras = {0: "acceptable", 1: "marginal", 2: "unacceptable"}
    par = {0:"cap", 1: "bottle", 2:"dent"}
    params = {"defect_name": par[p], "defect_result": paras[p]}
    return render(request, "pages/result_modal_body.html", params)