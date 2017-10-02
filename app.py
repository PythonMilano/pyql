
"""
Meetup API proxy.
"""

import os

import arrow
from box import Box
from flask import Flask, jsonify
from flask_cors import cross_origin
from eventbrite import Eventbrite

app = Flask(__name__)

eb_client = Eventbrite(os.environ['EB_TOKEN'])

MONTHS = ['', 'GENNAIO', 'FEBBRAIO', 'MARZO', 'APRILE', 'MAGGIO', 'GIUGNO',
          'LUGLIO', 'AGOSTO', 'SETTEMBRE', 'OTTOBRE', 'NOVEMBRE', 'DICEMBRE']


def return_value():
    """ Transform JSON to return dict """

    try:
        events = Box(eb_client.event_search(**{'organizer.id': os.environ['EB_ORGANIZER_ID']}))
    except:
        return {
            'topic': 'TBA',
            'day': 'NA',
            'month': 'NA',
            'link': '#',
        }
    else:
        obj = events.events[0]
        if events.pagination.object_count > 1:
            ev = {ev.start.local: idx for idx, ev in enumerate(events.events)}
            obj = events.events[ev[min(ev.keys())]]

        date = arrow.get(obj.start.local)

        return {
            'topic': obj.name.text,
            'day': date.day,
            'month': MONTHS[date.month],
            'link': obj.url,
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
