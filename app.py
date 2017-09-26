
"""
Meetup API proxy.
"""

import os

import arrow
import requests
from box import Box
from flask import Flask, jsonify
from flask_cors import cross_origin

app = Flask(__name__)

EVENTBRITE_API = 'https://www.eventbriteapi.com/v3/events/search/?token={token}&organizer.id={organizer_id}'

EVENTBRITE_SETTINGS = {
    'token': os.environ['EB_TOKEN'],
    'organizer_id': os.environ['EB_ORGANIZER_ID'],
}

MONTHS = ['', 'GENNAIO', 'FEBBRAIO', 'MARZO', 'APRILE', 'MAGGIO', 'GIUGNO',
          'LUGLIO', 'AGOSTO', 'SETTEMBRE', 'OTTOBRE', 'NOVEMBRE', 'DICEMBRE']


def get_results(response, index=0):
    """ Transform JSON to return dict """

    obj = Box(response.json()).events[index]
    date = arrow.get(obj.start.local)

    return {
        'topic': obj.name.text,
        'day': date.day,
        'month': MONTHS[date.month],
        'link': obj.url,
    }


def return_value():
    """ API call """

    response = requests.get(EVENTBRITE_API.format_map(EVENTBRITE_SETTINGS))
    if response.status_code == 200 and response.json():
        return get_results(response)
    return {
        'topic': 'TBA',
        'day': 'NA',
        'month': 'NA',
        'link': '#',
    }


@app.route('/meetup.js')
def meetup_js():
    """ API JSON to jQuery """

    return """ $('#topic').text('{topic}');
        $('#day').text('{day}');
        $('#month').text('{month}');
        $('#meetup_link').attr('href', '{link}');
        """.format(**return_value())


@app.route('/<meetup>.json')
@cross_origin()
def test_json(meetup):
    """ return JSON result with CORS """

    return jsonify(return_value(meetup))


@app.route('/')
def main():
    """ aka hello world :-) """
    return 'OMG! It works!'
