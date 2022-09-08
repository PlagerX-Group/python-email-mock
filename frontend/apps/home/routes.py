# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/smtp-messages')
@login_required
def smtp_messages():
    return render_template('home/smtp-messages.html', segment='smtp-messages')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception:
        return render_template('home/page-500.html'), 500


def get_segment(r):
    try:
        segment = r.path.split('/')[-1]

        if segment == '':
            segment = 'smtp-messages'

        return segment
    except Exception:
        return None
