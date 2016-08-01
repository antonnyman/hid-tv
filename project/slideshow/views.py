import xmltodict
import requests
import datetime
import time
import json
import dateutil.parser
from os import listdir
from os.path import isfile, join

from flask import Blueprint, jsonify
from geopy.geocoders import Nominatim
from project import db, app, render_template

from project.config import Auth, Config
from project.models import User, Page

slideshow_blueprint = Blueprint('slideshow', __name__)

@app.route('/slideshow')
def slideshow():
    pages = Page.query.order_by(Page.position).all()
    return render_template('slideshow.html', images = pages)

@app.route('/pages')
def pages():
    pages = []
    pagelist = Page.query.order_by(Page.position).all()
    for p in pagelist:
        pages.append({
            "id": p.id,
            "picture": p.picture,
            "created_at": p.created_at,
            "created_by": p.created_by,
            "position": p.position,
            "name": p.name
        })
    return jsonify(pages)

@app.route('/bus-times')
def bus_times():
    r = requests.get("http://www.labs.skanetrafiken.se/v2.2/stationresults.asp?selPointFrKey=81240")
    doc = xmltodict.parse(r.content)
    lines = doc['soap:Envelope']['soap:Body']['GetDepartureArrivalResponse']['GetDepartureArrivalResult']['Lines']['Line']

    first = lines[0]
    second = lines[1]

    return jsonify(first, second)

@app.route('/lunch')
def lunch():
    r = requests.get("http://www.fazer.se/api/location/menurss/current?pageId=28022&language=sv")
    doc = xmltodict.parse(r.content)
    lunch = doc['rss']['channel']['item']['description']
    #lunch.replace('</p>', '')
    luncharray = lunch.replace('<p>', '').replace('</p>', '').split("\n")
    weekarray = []
    for day in luncharray:
        daysplit = day.split("<br />")
        daysplit = list(filter(None, daysplit))
        weekarray.append(daysplit)

    daynames = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]

    week = {}
    today = ""
    for day in weekarray:
        if day[0] == daynames[datetime.datetime.now().weekday()]:
            print(day) 
            today = day

    return jsonify(today)

@app.route('/in-office')
def in_office():
    users = User.query.all()

    user_pos = []

    for user in users:
        if user.lifelog_token_expires_in is not None:
            if datetime.datetime.now() > user.lifelog_token_expires_in:
                refresh_lifelog(user)
            
            # get steps
            url = Auth.LIFELOG_GET_DATA 
            headers = {'Authorization': 'Bearer %s' %user.lifelog_token}
            r = requests.get(url, headers = headers)
            data = {} 

            if r.status_code == 500 or r.status_code == 401:
                refresh_lifelog()
                headers = {'Authorization': 'Bearer %s' %user.lifelog_token}
                r = requests.get(url, headers = headers)
                connected = "Connected"
            elif r.status_code == 200:
                connected = "Connected"
            else:
                connected = "Disconnected"

            data = r.json()
            steps = 0
            times_walking = []

            for d in data['result']: 
                if d['type'] == "physical":  
                    if 'steps' in d['details']:
                        for det in d['details']['steps']: 
                            steps += det
                if 'subtype' in d: 
                    if d['subtype'] == "walk":
                        startTime = dateutil.parser.parse(d['startTime'])
                        endTime = dateutil.parser.parse(d['endTime'])
                        timestamps = endTime - startTime 
                        times_walking.append(timestamps)

            total_time = sum(times_walking, datetime.timedelta())


            #get location
            geourl = Auth.LIFELOG_GET_LOCATION
            headers = {'Authorization': 'Bearer %s' %user.lifelog_token}
            print(user.lifelog_token) 
            geo_r = requests.get(geourl, headers = headers)  
            geodata = geo_r.json() 
            geolocation = Nominatim()

            latitude = geodata['result'][0]['position']['latitude']
            longitude = geodata['result'][0]['position']['longitude']

            location_raw = geolocation.reverse(("{}, {}".format(latitude, longitude)))

            location = location_raw.raw['address']['road']

            user_pos.append({
                "user_id": user.id, 
                "picture": user.picture,
                "location": location,
                "given_name": user.given_name,
                "projects": user.projects,
                "vab": user.vab,
                "vacation": user.vacation,
                "ooo": user.ooo,
                "normal": user.normal,
                #"time_walking": json.dumps(total_time),
                "steps": steps,
                "lifelog_token_expires_in": user.lifelog_token_expires_in
                })

        else:
            user_pos.append({
                "user_id": user.id,
                "picture": user.picture,
                "given_name": user.given_name,
                "projects": user.projects,
                "vab": user.vab,
                "vacation": user.vacation,
                "ooo": user.ooo,
                "normal": user.normal
            })

    return jsonify(user_pos)


def refresh_lifelog(u):
    body = "client_id=" + Auth.LIFELOG_CLIENT_ID + "&client_secret=" + Auth.LIFELOG_SECRET + "&grant_type=refresh_token&refresh_token=" + u.lifelog_refresh_token
    headers = {'cache-control': "no-cache",'content-type': "application/x-www-form-urlencoded"}
    r = requests.post(Auth.LIFELOG_REFRESH_TOKEN, data = body, headers = headers)
    print(r.json())
    response = r.json()

    expires_in = response['expires_in']
    now = datetime.datetime.now()
    token_expires_in = datetime.datetime.fromtimestamp(time.mktime(now.timetuple()) + expires_in).strftime('%Y-%m-%d %H:%M:%S')

    user = User.query.filter_by(id = u.id).first()
    user.lifelog_token_expires_in = token_expires_in
    user.lifelog_token = response['access_token']
    user.refresh_token = response['refresh_token']
    db.session.commit()