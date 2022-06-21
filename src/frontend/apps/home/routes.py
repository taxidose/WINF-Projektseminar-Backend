# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from src.frontend.apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from src.backend.xml_script import XMLProcessing

@blueprint.route('/index')
@blueprint.route('/index.html')
@login_required
def index():

    # dummy data
    data = {}

    data["number_projects"] = 42
    data["percent_rise_projects"] = 43

    data["number_publications"] = 420
    data["percent_rise_publications"] = 69

    data["number_cooperations"] = 100
    data["percent_rise_cooperations"] = 10

    data["number_patents"] = 1337
    data["percent_rise_patents"] = 5


    return render_template('home/index.html', data=data)



@blueprint.route('/tables')
@blueprint.route('/tables.html')
@login_required
def tables():


    research_projects = []
    research_projects.append({"title": "Zukunftsforschung im Supply Chain Management", "project_leader": "Christoph Küffner", "funder": "Dr. Hans Riegel-Stiftung", "project_start": " 04.05.2022"})

    publications = []
    publications.append({"title": "The Non-Stop Disjoint Trajectories Problem", "author": "Hoch B, Liers F, Neumann S", "publish_year": 2020, "language": "Englisch"})

    return render_template("home/tables.html", research_projects=research_projects, publications=publications)




# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#
#     try:
#
#         if not template.endswith('.html'):
#             template += '.html'
#
#         # Detect the current page
#         segment = get_segment(request)
#
#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template)
#
#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404
#
#     except:
#         return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
