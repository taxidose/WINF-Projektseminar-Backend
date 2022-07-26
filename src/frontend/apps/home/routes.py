# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
from apps.home import blueprint
from flask import render_template
from flask_login import login_required
from jinja2 import TemplateNotFound
import datetime

import sys
sys.path.append("..")
from backend.xml_script import XMLProcessing, URLs


@blueprint.route("/index")
@blueprint.route("/index.html")
@login_required
def index():
    xml_data_all_wiso_publs = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PUBLICATIONS"])
    publs_selected_attributes = ["cfTitle", "publYear", "srcAuthors", "Language"]
    filtered_data_all_wiso_publs = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_publs,
                                                                                  publs_selected_attributes)

    xml_data_all_wiso_projects = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PROJECTS"])
    selected_xml_attributes = ["relPersIDlead", "cfTitle", "funderlink", "Project Type", "cfStartDate", "cfEndDate"]
    filtered_data_all_wiso_projects = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_projects,
                                                                                     selected_xml_attributes)

    for i in range(0, len(filtered_data_all_wiso_projects)):
        filtered_data_all_wiso_projects[i]["project_start"] = datetime.datetime.strptime(
            filtered_data_all_wiso_projects[i]["project_start"], '%Y-%m-%d').strftime('%d.%m.%Y')
        if filtered_data_all_wiso_projects[i]["project_end"] != "None":
            filtered_data_all_wiso_projects[i]["project_end"] = datetime.datetime.strptime(
                filtered_data_all_wiso_projects[i]["project_end"], '%Y-%m-%d').strftime('%d.%m.%Y')

    print(filtered_data_all_wiso_projects[2])

    return render_template('home/index.html',
                           publications=json.dumps(filtered_data_all_wiso_publs),
                           research_projects=json.dumps(filtered_data_all_wiso_projects))


@blueprint.route("/research-projects-table")
@blueprint.route("/tables")
@blueprint.route("/tables.html")
@login_required
def research_projects_table():
    xml_data_all_wiso_projects = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PROJECTS"])
    selected_xml_attributes = ["relPersIDlead", "cfTitle", "funderlink", "Project Type", "cfStartDate", "cfEndDate"]
    filtered_data_all_wiso_projects = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_projects,
                                                                                     selected_xml_attributes)

    for i in range(0, len(filtered_data_all_wiso_projects)):
        filtered_data_all_wiso_projects[i]["project_start"] = datetime.datetime.strptime(
            filtered_data_all_wiso_projects[i]["project_start"], '%Y-%m-%d').strftime('%d.%m.%Y')
        if filtered_data_all_wiso_projects[i]["project_end"] != "None":
            filtered_data_all_wiso_projects[i]["project_end"] = datetime.datetime.strptime(
                filtered_data_all_wiso_projects[i]["project_end"], '%Y-%m-%d').strftime('%d.%m.%Y')

    return render_template("home/tables.html",
                           research_projects=filtered_data_all_wiso_projects)


@blueprint.route("/publications-table")
@blueprint.route("/tables2")
@blueprint.route("/tables2.html")
@login_required
def publications_table():
    xml_data_all_wiso_publs = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PUBLICATIONS"])
    selected_xml_attributes = ["cfTitle", "publYear", "srcAuthors", "Language"]
    filtered_data_all_wiso_publs = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_publs,
                                                                                  selected_xml_attributes)


    return render_template("home/tables2.html",
                           publications=filtered_data_all_wiso_publs)





