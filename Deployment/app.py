from flask import Flask, render_template, request
from keras.models import load_model
import os
import numpy as np
import pandas as pd
from PIL import Image
from keras.preprocessing import image

app = Flask(__name__)

model = load_model('my_model.h5')
print("+"*50, "Model is loaded")

labels = ['blackhead', 'eksim', 'flek hitam', 'herpes', 'jerawat', 'milia', 'panu', 'rosacea', 'tinea fasialis']


@app.route('/')
def index():
	return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def prediction():

	img = request.files['img']
	img_path = "static/image/" + img.filename
	img.save(img_path)

	image = Image.open(img_path)
	
	
	nimg = image.convert('RGB').resize((160, 160), resample= 0)
	img_arr = (np.array(nimg))/255
    
	X = np.stack([img_arr], axis=0)
	y = model.predict(X)
	

	pred = np.argmax(y)

	pred = labels[pred]
	acc = np.max(y) * 100
	acc = "{:.2f}".format(acc)
	return render_template("index.html", prediction=pred, accuracy=acc, pathImage=img_path)


if __name__ == "__main__":
	app.run(debug=True)
