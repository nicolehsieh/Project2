import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, g
from werkzeug import secure_filename

import sys

import gpxpy
import gpxpy.gpx

# Initialize the Flask application
app = Flask(__name__)

# UPLOAD_FOLDER is where we will store the uploaded files
# CHANGE with your own path for testing!!!!!!!
UPLOAD_FOLDER = './static/uploads'

# ALLOWED_EXTENSIONS is the set of allowed file extensions.
ALLOWED_EXTENSIONS = set(['gpx'])

# Added URL rule to let webserver serve these files for us 
# and so we only need a rule to generate the URL to these files.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# allowed_file() function checks if extension is valid
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# note - possible ambiguous routing in following two functions

@app.route('/')
def index():
    return render_template('index.html')

# upload_file() function upload file 
# and redirects the user to the URL for the uploaded file
@app.route('/display', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the name of the uploaded file
        file = request.files['file']

        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            
            # secure_filename() function secure a filename before storing it directly on the filesystem
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename) 

            # Move the file form the temporal folder to the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            points = load("static/uploads/" + filename, delta=100)
            g.points= points

            
            # session store filename in cookies
            # session['filename'] = filename
            # session allows you to store information specific to a user from one request to the next. 
            # This is implemented on top of cookies for you and signs the cookies cryptographically. 

            # Redirect the user to the uploaded_file route, which 
            # will basicaly show on the browser the uploaded file
            return render_template("leaf.html")
            

# serves(handle) uploaded file
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # display gpx path on a map
# @app.route('/display', methods = ['GET','POST'])
# def display():
#     # retrieve file name from cookies session
#     # filename = session['filename']
#     filename = request.args.get('filename')
#     return render_template("leaf.html")

# set the secret key. 
# app.secret_key = '\x81|fL\xec\xa2[\x12\xf0\x0f\xa8X'


# from https://bitbucket.org/MichalYoung/enroute-saunter/src/be98484f0ae062ac8ed0b5f2829f4b78d16911dc/htbin/gpx_from_file.cgi?at=master&fileviewer=file-view-default
def load(filename, delta = None):
    """
    Return a list of (lat, lon) pairs retrieved from gpx file
    
    Args:
        filename: path of gpx file
        delta: If provided, simplify path to max deviation of delta meters.
                100 meters will generally simplify
                a RideWithGPS route radically.
    Returns:
            A list of (lattitude, longitude) pairs.
    """
    contents = open(filename, 'r', encoding="utf-8", errors="replace")
    gpx = gpxpy.parse(contents)
    if delta:
        gpx.simplify(delta)
        points =[ ]
        #times  =[ ]
        
        for track in gpx.tracks:
            for segment in track.segments:
                    for point in segment.points:
                        points.append( [point.latitude, point.longitude] )                        
                        #times.append(point.time) #Maybe times.append(arrow.get(point.time).datetime)
        return points
### TODO: Write this function to make animation time-accurate

def calcDurations(times):
    '''
    total = times[-1]-times[0]
    anim_dur = 20000
        ## or somehow set anim_dur to total converted to milliseconds
        
    durations = [ ] 
    for i in range(10):
        if i != 0:
            diff = times[i]-times[i-1] #use datetime timedelta
            realdiff = (diff converted to milliseconds)
            dur = realdiff/anim_dur
            durations.append(dur)
    return durations
    '''
    return 0




# # get gpx file
# @app.route('/getgpx/<filename>', methods=['GET'])
# def getgpx(filename):
#   f = open(filename)
#   result = ""
#   for line in f:
#       result += line
#   return result

# read file as python, and return as JSON, easier for manipulation, then 


if __name__ == '__main__':
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000
    )
