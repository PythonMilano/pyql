
"""
Meetup API proxy.
"""

import requests

import arrow
from box import Box
from flask import Flask, jsonify
from flask_cors import cross_origin

app = Flask(__name__)

MONTHS = ['', 'GENNAIO', 'FEBBRAIO', 'MARZO', 'APRILE', 'MAGGIO', 'GIUGNO',
          'LUGLIO', 'AGOSTO', 'SETTEMBRE', 'OTTOBRE', 'NOVEMBRE', 'DICEMBRE']

CURRENT_EVENTS = 'https://api.meetup.com/{meetup}/events'
PAST_EVENTS = 'https://api.meetup.com/{meetup}/events/?status=past'


def get_results(response, index=0):
    """ Get results from meetup API"""
    obj = Box(response.json()[index])
    date = arrow.Arrow.fromtimestamp(obj.time / 1000)

    return {
        'topic': obj.name,
        'day': date.day,
        'month': MONTHS[date.month],
        'link': obj.link,
    }


def return_value(meetup='Python-Milano'):
    """ meetup API call """
    response = requests.get(CURRENT_EVENTS.format(meetup=meetup))
    if response.status_code == 200 and response.json():
        return get_results(response)

    response = requests.get(PAST_EVENTS.format(meetup=meetup))
    if response.status_code == 200 and response.json():
        return get_results(response, -1)

    return {
        'topic': 'TBA',
        'day': 'NA',
        'month': 'NA',
        'link': '#',
    }


@app.route('/meetup.js')
def meetup_js():
    """ Convert JSON to JS """
    return """ $('#topic').text('{topic}');
        $('#day').text('{day}');
        $('#month').text('{month}');
        $('#meetup_link').attr('href', '{link}');
        """.format(**return_value())


@app.route('/<meetup>.json')
@cross_origin()
def test_json(meetup):
    """ Test CORS JSON """
    return jsonify(return_value(meetup))
