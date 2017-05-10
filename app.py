# -*- coding: utf-8 -*-
"""
Meetup API proxy.
"""

import calendar
import locale
import arrow
import requests
from box import Box
from flask import Flask


app = Flask(__name__)
locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

CURRENT_EVENTS = 'https://api.meetup.com/Python-Milano/events'
PAST_EVENTS = 'https://api.meetup.com/milano-scala-group/events/?status=past'


def get_results(response, index=0):
    """ Get results from meetup API"""
    obj = Box(response.json()[index])
    date = arrow.Arrow.fromtimestamp(obj.time / 1000)

    return {
        'topic': obj.name,
        'day': date.day,
        'month': calendar.month_name[date.month - 1].upper(),
        'link': obj.link,
    }


def return_value():
    """ meetup API call """
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
def meetup_js():
    """ Convert JSON to JS """
    return """ $('#topic').text('{topic}');
        $('#day').text('{day}');
        $('#month').text('{month}');
        $('#meetup_link').attr('href', '{link}');
        """.format(**return_value())
