from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np
from PIL import Image 
import json 

app = Flask(__name__)

model = load_model('my_model.h5')
print("+"*50, "Model is loaded")

labels = ['blackhead', 'eksim', 'flek hitam', 'herpes', 'jerawat', 'milia', 'panu', 'rosacea', 'tinea fasialis']
file_json = open("D:\Documents\Dicoding\Capstone Project\Deployment\static\solusi.json")
datasolusi = json.loads(file_json.read())

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
 
 
	if pred == labels[0]:definisi = datasolusi["blackhead"]["definisi"];solusi = datasolusi["blackhead"]["solusi"]
	if pred == labels[1]:definisi = datasolusi["eksim"]["definisi"];solusi = datasolusi["eksim"]["solusi"]
	if pred == labels[2]:definisi = datasolusi["flekhitam"]["definisi"];solusi = datasolusi["flekhitam"]["solusi"]
	if pred == labels[3]:definisi = datasolusi["herpes"]["definisi"];solusi = datasolusi["herpes"]["solusi"]
	if pred == labels[4]:definisi = datasolusi["jerawat"]["definisi"];solusi = datasolusi["jerawat"]["solusi"]
	if pred == labels[5]:    	definisi = datasolusi["milia"]["definisi"];		solusi = datasolusi["milia"]["solusi"]
	if pred == labels[6]:    	definisi = datasolusi["panu"]["definisi"];		solusi = datasolusi["panu"]["solusi"]
	if pred == labels[7]:    	definisi = datasolusi["rosacea"]["definisi"];		solusi = datasolusi["rosacea"]["solusi"]
	if pred == labels[8]:		definisi = datasolusi["tinea fasialis"]["definisi"];		solusi = datasolusi["tinea fasialis"]["solusi"]
		
	return render_template("index.html", prediction=pred, accuracy=acc, pathImage=img_path, definisi=definisi, solusi=solusi)
    


if __name__ == "__main__":
	app.run(debug=True)
