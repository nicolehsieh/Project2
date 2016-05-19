import os
from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# app.use(express.static(__dirname + '/public'));


@app.route('/')
def index():
   return render_template('upload.html')
	

@app.route('/upload', methods = ['POST'])
def upload():
	# target = os.path.join(APP_ROOT, "gpx/")
	# print  (target)

	# # check if file path is correct
	# if not os.path.isdir(target):
	# 	os.mkdir(target)

	# # looping through a list, and return a list of file names
	# for file in request.files.getlist("file"):
	# 	print (file)
	# 	filename = file.filename
	# 	destination = "/".join([target, filename]) # adding file name to folder name(where we want to store the upload file)
	# 	print (destination)
	# 	file.save(destination)


	return render_template("leaf.html")


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/getgpx/<filename>', methods=['GET'])
def getgpx(filename):
	f = open(filename)
	result = ""
	for line in f:
		result += line

	return result

# read file as python, and return as JSON, easier for manipulation, then 


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)