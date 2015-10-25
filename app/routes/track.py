from flask import Blueprint, render_template,request, redirect, url_for
from app.models.tracks import Track,Layer
from bson.objectid import ObjectId
import os, datetime
from app import db


track = Blueprint('track', __name__, url_prefix='/track')


@track.route('/<trackID>')  
def track_page(trackID):
    track = Track.objects().get(id = ObjectId(trackID))
    return render_template('track.html',track = track)



@track.route('/save/<trackID>', methods = ["GET","POST"])
def save_layer(trackID):
	if request.method == "POST":
		track = Track.objects().get(id = ObjectId(trackID))

		layerName = request.form['layerName']
		startTime = request.form['startTime']
		layerFile = request.files['layerFile']

		layerPath = "/static/music/wedidit.wav"

		newLayer = Layer(
				layerName = layerName,
				layerPath = layerPath,
				createdBy = "Noah Zweben",
				startTime = startTime,
				layerID = ObjectId() )

		layerFile.save('app/'+layerPath)
		track.layers.append(newLayer)
		track.save()

	return redirect( url_for('track.track_page', trackID=trackID))

@track.route('/delete/<trackID>/<layerID>')
def del_layer(trackID,layerID):
	track = Track.objects().get(id = ObjectId(trackID))	
	track.update(pull__layers__layerID=ObjectId(layerID))
	track.save()
	
	if len(track.layers)-1 == 0: #why is -1 necessary?
		print "Deleting Track"
		track.delete()
		return redirect( url_for('home.home_page') )
	return redirect( url_for('track.track_page', trackID=trackID))

