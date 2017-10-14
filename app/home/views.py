# app/home/views.py
#-*-coding:utf-8 -*-
from flask import Flask, render_template, request, url_for
import requests
import json
import re
#from instance.config import UNIT, LANGUAGE, weathercode
from flask_sqlalchemy import SQLAlchemy
from . import home
from .. import db
from ..models import Weathers_xz, User
from flask_login import login_required, current_user
#from .forms import QueryForm

API = 'https://api.seniverse.com/v3/weather/now.json'
KEY = 'inpt4hjarhzfge3s'  # API key
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言
# 天气代码词典
weathercode = { "0": "晴",
                "1": "晴",
                "2": "晴",
                "3": "晴",
                "4": "多云",
                "5": "晴间多云",
                "6": "晴间多云",
                "7": "大部多云",
                "8": "大部多云",
                "9": "阴",
                "10": "阵雨",
                "11": "雷阵雨",
                "12": "雷阵雨伴有冰雹",
                "13": "小雨",
                "14": "中雨",
                "15": "大雨",
                "16": "暴雨",
                "17": "大暴雨",
                "18": "特大暴雨",
                "19": "冻雨",
                "20": "雨夹雪",
                "21": "阵雪",
                "22": "小雪",
                "23": "中雪",
                "24": "大雪",
                "25": "暴雪",
                "26": "浮尘",
                "27": "扬沙",
                "28": "沙尘暴",
                "29": "强沙尘暴",
                "30": "雾",
                "31": "霾",
                "32": "风",
                "33": "大风",
                "34": "飓风",
                "35": "热带风暴",
                "36": "龙卷风",
                "37": "冷",
                "38": "热",
"99": "未知"}
# API 抓取信息，并设置location为待输入变量
history_list = None #list
def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
        }, timeout=1)
    result = result.json() # Very import very import, if no this syntax, there is a erro called "subscriptable"
    weather = result['results'][0]['now']['text'] #因为result是由一个Dir+list+Dir组成, for [0],becaues it's a list which only have 1 element
    temperature = result['results'][0]['now']['temperature']
    updated_time_c = result['results'][0]['last_update']
    updated_time = updated_time_c.split('T')[0]

    #weather_str = f'{location}天气:{weather},气温:{temperature}℃\n更新时间:{updated_time}.\n'
    return location, weather, temperature, updated_time

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('index.html', title="Welcome")


@home.route('/query_xz', methods=['GET', 'POST'])
@login_required
def query_xz():
#    city = request.args.get['city']
    inquiry_outcome = None
    inquiry_history = None
    help_information = None
    is_updated = None
    error = None

    if request.method == "POST":
        if request.form['action'] == u'查询':
            select = Weathers_xz.query.filter_by(location=request.form['city'],
                                                user_id=current_user.id).first()

            if select:
                inquiry_outcome = select
            else:
                #city = request.form['city']
                inquiry = fetchWeather(request.form['city'])
                if inquiry:
                    try:
                        weather_xz = Weathers_xz(location=inquiry[0],
                                            weather=inquiry[1],
                                            temperature=inquiry[2],
                                            day=inquiry[3],
                                            user_id=current_user.id)
                        db.session.add(weather_xz)
                        db.session.commit()
                        inquiry_outcome = Weathers_xz.query.filter_by(location=inquir[0],
                                                                    user_id=current_user.id).first()
                    except ValueError:
                        is_updated = "亲，肯定是系统错误，您再试一下！"

                return render_template('home/query.html', updated_time=inquiry_outcome[3],
                                    location=inquiry_outcome[0],
                                    weather=inquiry_outcome[1],
                                    temperature=inquiry_outcome[2], title="Query")

        elif request.form['action'] == u'历史':
            lists = current_user.weather_xz.all()
            inquiry_history = lists
            return render_template('home/history.html', history_list=inquiry_history)


        elif request.form['action']== u'更新':
            try:
                location, weather = (request.form['location']).split(" ") #!!! say the web
                select = Weathers_xz.query.filter_by(location=location,
                                                    user_id=current_user.id).first()
                if select:
                    if weather in weathercode.values():
                        select.weather = weather
                        select.day = now
                        db.session.commit()
                        return render_template('home/update.html')
                    else:
                        is_updated = "输入天气信息有误！"
                else:
                    is_updated = "该城市不在查询历史中。"
            except ValueError:
                is_updated = "请按（城市名 常见天气）格式输入！"

        else:
            #request.args.get['action'] == u'帮助':
            help_information = 1
            return render_template('home/help.html', help_information=help_information)

    else:
        return render_template('index.html', title="Query")
