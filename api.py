from flask import Flask, flash, request, redirect, url_for, jsonify, send_file, make_response
from flask_cors import CORS, cross_origin
import numpy as np
import urllib
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import cv2

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def upload_file():
    if request.method == 'POST':
#         file = request.get_json()
        print(request.files)
        print(request.files["myfile"])
        if 'myfile' not in request.files:
            return "no file found"
        else:
#             print(dir(request))
#             print(request.get_data())
#             file = request.files.get("myfile")
#             print(file)
#             f = urllib.request.urlopen(file)
            a = request.files["myfile"]
            pil_image = Image.open(a)
            pix = np.array(pil_image)
            img = cv2.resize(pix, (224, 224))
            model = load_model('mobilenetV2_original.h5')
#             img=image.load_img(pil_image, target_size=(224,224))
            #img = tf.keras.utils.load_img(image_path, target_size=(224,224))
            img = np.array(img)
            img = img / 255.0
            img = img.reshape(1,224,224,3)
            label = model.predict(img)
            # print("Predicted score",label)
            #print("Predicted Clas, ls (0 - Cars , 1- Planes): ", label[1][1])
            p=np.argmax(label)
            if p==0:
                return "acceptable" 
            elif p==1:
                return "marginal" 
            else:
                return "unacceptable"
        

app.run(debug=False)