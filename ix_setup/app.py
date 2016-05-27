import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, g
from werkzeug import secure_filename

import sys

# Python libraries
import gpxpy
import gpxpy.gpx
import arrow
import datetime


import logging
import CONFIG


# Initialize the Flask application
app = Flask(__name__)
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

# UPLOAD_FOLDER is where we will store the uploaded files
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


@app.route('/')
def index():
    return render_template('index.html')


# upload_file() function upload file and redirects the user to the URL for the uploaded file
@app.route('/display', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the name of the uploaded file
        file = request.files['file']
        

        animlength = 20
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            
            # secure_filename() function secure a filename before storing it directly on the filesystem
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename) 

            # Move the file form the temporal folder to the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # arrays holds the points array and the times array corresponding to the gpx file
            arrays = []					
            arrays = load("static/uploads/" + filename, delta=100)
            g.points= arrays[0]
            
            # calculate the durations using the time array
            durations = calcDurations(arrays[1], animlength)
            g.durations = durations
            
            return render_template("leaf.html")
            


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



# From https://bitbucket.org/MichalYoung/enroute-saunter/src/be98484f0ae062ac8ed0b5f2829f4b78d16911dc/htbin/gpx_from_file.cgi?at=master&fileviewer=file-view-default
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
        points =[ ] # to hold points (latitude, longitude)
        times  =[ ]	# to hold times 
        arrays =[ ]	# to hold both of the above arrays
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append( [point.latitude, point.longitude] )                        
                    times.append(arrow.get(point.time).datetime)	# use arrow to interperet the time, then convert to datetime object
        arrays.append(points) 
        arrays.append(times)
        return arrays
        
def calcDurations(times, speed):
    '''
    Calculates time in milliseconds animation will take to get between each point
    Args:
    	times: array of datetime objects corresponding to each point in points array
    Returns:
    	array of durations (floats, in milliseconds)
    '''
    
    # calculate total elapsed time get timedelta, convert to floats, scale to animation
    timedelta = times[len(times)-1]-times[0] 
    totalElapsedTime = makeNumbers(timedelta)
    
    scaleAnimDur = speed*1000
    anim_dur = totalElapsedTime/scaleAnimDur
    
    durations = [ ]  # array to store durations
    for i in range(1, len(times)):
    	
        # calculate timedelta for difference between each point
        diff = times[i]-times[i-1]
        # convert to float value in milliseconds
        mil = makeNumbers(diff)
        # scale to animation duration
        dur = mil/anim_dur
        durations.append(dur)
    return durations

def makeNumbers(timedelta):
	'''
	Converts datetime.timedelta object into float value for milliseconds
	
	Args:
		time: a datetime.timedelta thing
	Returns:
		a float of the timedelta converted to milliseconds
	'''
	d = timedelta.days 		# get int number of days
	s = timedelta.seconds		# get int number of seconds
	m = timedelta.microseconds	# get int number of microseconds
	mil = (d*24*60*60000)+(s*1000)+(m/1000)		# add the days, seconds, and microseconds together and convert to milliseconds
	
	return mil

if __name__ == '__main__':
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(
        debug=True, 
        port=CONFIG.PORT,
        host='0.0.0.0'
    )
else:
    pass
