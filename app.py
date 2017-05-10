# -*- coding: utf-8 -*-
import arrow
import requests
from box import Box
from flask import Flask, request

app = Flask(__name__)

CURRENT_EVENTS = 'https://api.meetup.com/Python-Milano/events'
PAST_EVENTS = 'https://api.meetup.com/milano-scala-group/events/?status=past'
MONTHS = ['GENNAIO', 'FEBBRAIO', 'MARZO', 'APRILE', 'MAGGIO', 'GIUGNO', 'LUGLIO', 'AGOSTO', 'SETTEBRE', 'OTTOBRE', 'NOVEMBRE', 'DICEMBRE']

def get_results(response, index=0):
    obj = Box(response.json()[index])
    return {
        'topic': obj.name,
        'day': arrow.Arrow.fromtimestamp(obj.time/1000).day,
        'month': MONTHS[arrow.Arrow.fromtimestamp(obj.time/1000).month - 1],
        'link': obj.link,
    }
    
def return_value():
    response = requests.get(CURRENT_EVENTS)
    if response.status_code == 200 and response.json():
        return get_results(response)

    response = requests.get(PAST_EVENTS)
    if response.status_code == 200 and response.json():
        return get_results(response, -1)

    return {
        'topic': 'TBA',
        'day': 'NA',
        'month': 'NA',
        'link': '#',
    }

@app.route('/meetup.js')
def hello_world():
    return """ $('#topic').text('{topic}');
        $('#day').text('{day}');
        $('#month').text('{month}');
        $('#meetup_link').attr('href', '{link}');
        """.format(**return_value())  