# -*- coding: utf-8 -*-
"""cap_sealed_md_houghlines.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gTpwnCuYndZP1SQYW9rRTvpg3r3j0jBy

# for medium bottle, cap sealed defect with acceptable, marginal and unacceptable
 - light :add + 2 times
 - position large
"""

import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate

import PIL
from PIL import ImageEnhance
from PIL import Image

import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate

import PIL
from PIL import ImageEnhance
from PIL import Image

def cap_sealed_md(img_name):
    size = "md"
    path = img_name

    image_c = cv2.imread(path)
    image_c = np.rot90(np.rot90(image_c))

    image = cv2.imread(path,0)
    image = np.rot90(np.rot90(image))


    # plt.figure(figsize=(10,10))
    # plt.imshow(cv2.cvtColor(image_c,cv2.COLOR_BGR2RGB))

    # crop image
    if size == "lg":
        image_c = image_c[500:,800:2500]
        image = image[500:,800:2500]
    elif  size == "md":
        image_c = image_c[1000:,800:2500]
        image= image[1000:,800:2500]
    elif  size == "sm":
        image_c = image_c[500:,800:2500]
        image = image[500:,800:2500]
        
    # plt.imshow(cv2.cvtColor(image_c,cv2.COLOR_BGR2RGB))

    img = image
    img = cv2.medianBlur(img,5)

    ret,th1 = cv2.threshold(img,80,255,cv2.THRESH_BINARY)

    titles = ['org','Global Thresholding (v = 127)'
                ]
    images = [img, th1]
    # assert len(titles)==len(images)
    # for i in range(len(titles)):
    #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])
    # plt.show()

    bbox = cv2.boundingRect(th1)
    x, y, w, h = bbox

    if size == "lg":
        cropped = cv2.cvtColor(image_c[y-30:y+h+30, x:x+w], cv2.COLOR_BGR2RGB)

    if size == "md":
        cropped = cv2.cvtColor(image_c[y-160:y+h+30, x:x+w], cv2.COLOR_BGR2RGB)

    if size == "sm":
        cropped = cv2.cvtColor(image_c[y-160:y+h+30, x:x+w], cv2.COLOR_BGR2RGB)

    # cropped = cv2.cvtColor(image_c[y:y+h, x:x+w], cv2.COLOR_BGR2RGB)
        
    # plt.figure(figsize=(10,10))
    # plt.imshow(cropped,'gray',vmin=0,vmax=255)
    # plt.show()

    h,w, _ = cropped.shape
    md_crop_ratio =  0.65
    sm_crop_ratio = 0.8
    lg_crop_ratio = 0.5

    # h1 = int(h * 0.24)
    if size == "lg":
        h1 = int(h * lg_crop_ratio)
    elif  size == "md":
        h1 = int(h * md_crop_ratio)
    elif  size == "sm":
        h1 = int(h * sm_crop_ratio)
    # h1 = int(h * 0.55)
    cap_only = cropped[0:h1,:]
    # plt.imshow(cap_only)

    cap_lid = cap_only[190:350,200:]
    # plt.imshow(cap_lid)

    blur_lid = cv2.medianBlur(cap_lid,5) 
    # plt.imshow(blur_lid)

    cap_left = cap_lid[:,0:150]
    cap_right = cap_lid[:,450:]

    # plt.subplot(1,2,1),plt.imshow(cap_left)
    # plt.subplot(1,2,2),plt.imshow(cap_right)

    lid_grayl = cv2.cvtColor(cap_left, cv2.COLOR_RGB2GRAY)
    lid_grayr = cv2.cvtColor(cap_right, cv2.COLOR_RGB2GRAY)
    t =130
    edgesl = cv2.Canny(lid_grayl,t/3,t) 
    edgesr = cv2.Canny(lid_grayr,t/3,t) 

    # plt.subplot(1,2,1),plt.imshow(edgesl,"gray")
    # plt.subplot(1,2,2),plt.imshow(edgesr,"gray")

    kernelSizes = [(5, 5), (5, 5), (7, 7)]
    for kernelSize in kernelSizes:
        # construct a rectangular kernel form the current size, but this
        # time apply a "closing" operation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
        closingl = cv2.morphologyEx(edgesl, cv2.MORPH_CLOSE, kernel)
        closingr = cv2.morphologyEx(edgesr, cv2.MORPH_CLOSE, kernel)
        break
        
    # plt.subplot(1,2,1),plt.imshow(closingl,"gray")
    # plt.subplot(1,2,2),plt.imshow(closingr,"gray")

    cdst = cap_left.copy()
    rhos = []
    defect_left = 0
    # lines = cv2.HoughLines(closingl, 1.5, np.pi / 180, 50)
    lines = cv2.HoughLines(closingl, 1, np.pi / 180, 50)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
    #             if  theta == theta_min or theta==theta_max:
            if rho >= 5 and theta >= 1:
                rhos.append(rho)
                print("rho : {}   theta:{}".format(rho, theta))
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(cdst, pt1, pt2, (0,255,0), 3, cv2.LINE_AA)

    if rhos == []:
        pass
    else:
        diff = abs(min(rhos) - max(rhos))
        print(diff)
        if diff >30:
            defect_left = 1
            
            
    # plt.imshow(cdst)

    cdst = cap_right.copy()
    defect_right = 0
    # lines = cv2.HoughLines(closingr, 1.5, np.pi / 180, 50)
    # lines = cv2.HoughLines(closingr, 1, np.pi / 180, 50)
    lines = cv2.HoughLines(closingr, 1, np.pi / 180, 50)
    rhos = []
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
    #             if  theta == theta_min or theta==theta_max:
            if rho >= 0:
                rhos.append(rho)
                print("rho : {}   theta:{}".format(rho, theta))
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(cdst, pt1, pt2, (0,255,0), 3, cv2.LINE_AA)

    if rhos == []:
        pass
    else:
        diff = abs(min(rhos) - max(rhos))
        print(diff)
        if diff >30:
            defect_right = 1
    # plt.imshow(cdst)

    if defect_left or defect_right:
        return "Unacceptable"
    else:
        return "Acceptable"
        
    # plt.imshow(cap_only)







