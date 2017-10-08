# app/home/views.py
#-*-coding:utf-8 -*-
from flask import Flask, render_template, request, url_for
import requests
import json
import re
#import sys
#sys.path.append("C:\\Users\\CNNEZHA2\\mystuff\\Py104\\Py101-004\\Chap5\\project")
#sys.path.append("C:\\Users\\CNNEZHA2\\mystuff\\Py104\\Py101-004\\Chap5\\project\\instance")
#sys.path.append("C:\\Users\\CNNEZHA2\\mystuff\\Py104\\Py101-004\\Chap5\\project\\app")
from instance.config import API, KEY, UNIT, LANGUAGE, weathercode
from flask_sqlalchemy import SQLAlchemy
from . import home
from .. import db
from ..models import Weathers_xz, User
from flask_login import login_required, current_user

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

#API = 'https://api.seniverse.com/v3/weather/now.json'
# API 抓取信息，并设置location为待输入变量
history_list = [] #list
def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
        }, timeout=3)
    result = result.json() # Very import very import, if no this syntax, there is a erro called "subscriptable"
    weather = result['results'][0]['now']['text'] #因为result是由一个Dir+list+Dir组成, for [0],becaues it's a list which only have 1 element
    temperature = result['results'][0]['now']['temperature']
    updated_time = result['results'][0]['last_update']
    updated_time = updated_time.split('T')[0]

    #weather_str = f'{location}天气:{weather},气温:{temperature}℃\n更新时间:{updated_time}.\n'
    return updated_time, location, weather, temperature

@home.route('/')
def index():
    return render_template('home/index.html', title="Welcome")

@home.route('/user_request',methods=['GET', 'POST'])
def process_request():
    city = request.args.get('city')
    select = Weathers.query.filter_by(location=city).first()

    if request.args.get('query') == u'查询':
        #weather_str = retrieve_data(city) #this weather_str also came from the database.py
        select = Weathers.query.filter_by(location=city).first()
        if select:
            updated_time = select.day
            location = city
            weather = select.weather
            temperature = select.temperature
            return render_template("home/query.html", updated_time=updated_time, location=location, weather=weather, temperature=temperature)

        else:
            try:                                         # try must be in a very smart combined with except!!
                updated_time, location, weather, temperature = fetchWeather(city)
                select.location = location
                select.day = updated_time
                select.weather = weather
                select.temperature = temperature
                db.session.add(weathers)
                db.session.commit()
                #weather_str = '{}, {}的天气为{}, 气温{}°'.format(updated_time, location, weather, temperature) # must be here, or there will be error
                #history_list.append(weather_str) // this from the API
                return render_template("home/query.html", updated_time=updated_time, location=location, weather=weather, temperature=temperature, title="Query")
            except KeyError:
                return render_template("error.html",city=city)
    elif request.args.get('history') == u'历史':
        lists = Weathers.query.filter_by.all(location=city).first()
        history_list = lists
        return render_template("home/history.html", history_list=history_list)

    elif request.args.get('help') == '帮助':
        return render_template('home/help.html')

    elif request.args.get('update') == u'更新':
        try:
            location, weather = city.split(" ") #!!! say the web
            select = Weathers.query.filter_by(location=city).first()
            if select:
                if weather in weathercode.values():
                    select.weather = weather
                    select.day = now
                    db.session.commit()
                    return render_template('home/update.html')
                else:
                    is_updated = "输入天气信息有误！"
        except ValueError:
            return render_template("home/error.html")
