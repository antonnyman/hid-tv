import json
import requests
import datetime
import time
import dateutil.parser

from flask import Blueprint, jsonify, flash
from geopy.geocoders import Nominatim
from project import db, app, login_manager, login_required, \
    login_user, redirect, render_template, request, logout_user, \
    session, current_user, OAuth2Session, HTTPError, url_for
from project.config import Auth
from project.models import User

user_blueprint = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_google_auth(state = None, token = None):
    if token:
        return OAuth2Session(Auth.GOOGLE_CLIENT_ID, token = token)
    if state:
        return OAuth2Session(
            Auth.GOOGLE_CLIENT_ID,
            state = state,
            redirect_uri = Auth.GOOGLE_REDIRECT_URI
        )
    oauth = OAuth2Session(
        Auth.GOOGLE_CLIENT_ID,
        redirect_uri = Auth.GOOGLE_REDIRECT_URI,
        scope = Auth.GOOGLE_SCOPE
    )
    return oauth



def get_lifelog_auth(state = None, token = None):
    if token:
        return OAuth2Session(Auth.LIFELOG_CLIENT_ID, token = token)
    if state:
        return OAuth2Session(
            Auth.LIFELOG_CLIENT_ID,
            state = state,
            redirect_uri = Auth.LIFELOG_AUTH_URI
        )
    oauth = OAuth2Session(
        Auth.LIFELOG_CLIENT_ID,
        scope = Auth.LIFELOG_SCOPE,
    )
    return oauth


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    google_auth_url, state = google.authorization_url(Auth.GOOGLE_AUTH_URI, access_type = 'offline')
    session['oauth_state'] = state
    return render_template('login.html', google_auth_url = google_auth_url)

@app.route('/google-callback')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))

    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'Access denied.'
        return 'Encountered an error.'

    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))

    else:
        google = get_google_auth(state = session['oauth_state'])

        try:
            token = google.fetch_token(
            Auth.GOOGLE_TOKEN_URI,
            client_secret = Auth.GOOGLE_CLIENT_SECRET,
            authorization_response = request.url
            )
        except HTTPError:
            return 'HTTP Error.'

        google = get_google_auth(token = token)
        response = google.get(Auth.GOOGLE_USER_INFO)

        if response.status_code == 200:
            user_data = response.json()
            email = user_data['email']
            user = User.query.filter_by(email = email).first()
            if user is None:
                user = User(
                    picture = user_data['picture'],
                    family_name = user_data['family_name'],
                    link = user_data['link'],
                    email = user_data['email'],
                    google_id = user_data['id'],
                    name = user_data['name'],
                    verified_email = user_data['verified_email'],
                    gender = user_data['gender'],
                    given_name = user_data['given_name'],
                    locale = user_data['locale'],
                    tokens = json.dumps(token)
                )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch the information'


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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    lifelog = get_lifelog_auth()
    lifelog_auth_url, state = lifelog.authorization_url(Auth.LIFELOG_AUTH_URI)
    session['oauth_state'] = state

    vab_checked = ''
    vacation_checked = ''
    ooo_checked = ''

    if current_user.vab:
        vab_checked = 'checked'
    elif current_user.ooo:
        ooo_checked = 'checked'
    elif current_user.vacation:
        vacation_checked = 'checked'

    if current_user.lifelog_token_expires_in is not None:   
        if datetime.datetime.now() > current_user.lifelog_token_expires_in:
            print("Too old") 
            refresh_lifelog(current_user)

        url = Auth.LIFELOG_GET_DATA 
        headers = {'Authorization': 'Bearer %s' %current_user.lifelog_token}
        r = requests.get(url, headers = headers)
        data = {} 

        if r.status_code == 500 or r.status_code == 401:
            refresh_lifelog()
            headers = {'Authorization': 'Bearer %s' %current_user.lifelog_token}
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

        geourl = Auth.LIFELOG_GET_LOCATION
        geo_r = requests.get(geourl, headers = headers)
        geodata = geo_r.json()
        geolocation = Nominatim()
        

        latitude = geodata['result'][0]['position']['latitude']
        longitude = geodata['result'][0]['position']['longitude']

        location_raw = geolocation.reverse(("{}, {}".format(latitude, longitude)))

        location = location_raw.raw['address']['road']
        #if 'address' in location_raw:
         #   location = location_raw.raw['address']['road']
        #else:
        #    location = ""

        
    else:
        connected = "Disconnected"
        steps = ""
        total_time = ""
        location = ""

    if request.method == 'POST':
        if request.form:

            status = request.form['status']
            user = User.query.filter_by(id = current_user.id).first()
            if status == "normal":
                user.normal = True
                user.vab = False
                user.ooo = False
                user.vacation = False
            elif status == "vab":
                user.normal = False
                user.vab = True
                user.ooo = False
                user.vacation = False
            elif status == "ooo":
                user.normal = False
                user.vab = False
                user.ooo = True
                user.vacation = False
            elif status == "vacation":
                user.normal = False
                user.vab = False
                user.ooo = False
                user.vacation = True
            else:
                user.normal = True
                user.vab = False
                user.ooo = False
                user.vacation = False

            user.projects = request.form['projects']

            db.session.commit()
            flash("Success")    
 
    return render_template('profile.html', 
                            lifelog = lifelog_auth_url,
                            connected = connected, 
                            token = steps,
                            total_time = total_time, 
                            location = location
                            )

@app.route('/lifelog-auth')
@login_required
def lifelog_auth():

    lifelog = get_lifelog_auth()

    try:
        token = lifelog.fetch_token(
            Auth.LIFELOG_TOKEN_URI,
            client_id = Auth.LIFELOG_CLIENT_ID,
            client_secret = Auth.LIFELOG_SECRET,
            authorization_response = request.url
        )
    except HTTPError:
        return 'HTTPError'

    lifelog = get_lifelog_auth(token = token)
    response = lifelog.get(Auth.LIFELOG_USER_INFO)
    if response.status_code == 200:
        user = User.query.filter_by(id = current_user.id).first()
        now = datetime.datetime.now()
        token_expires_in = datetime.datetime.fromtimestamp(time.mktime(now.timetuple()) + token['expires_in']).strftime('%Y-%m-%d %H:%M:%S')
        if user is not None:
            lifelog_data = response.json()
            user.lifelog_token = token['access_token']
            user.lifelog_refresh_token = token['refresh_token']
            user.lifelog_token_expires_in = token_expires_in
            db.session.commit()
        #return jsonify({'result': response.json()})

    

    return redirect(url_for('profile'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


