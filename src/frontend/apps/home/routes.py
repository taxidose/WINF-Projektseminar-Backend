# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template
from flask_login import login_required
from jinja2 import TemplateNotFound
import datetime

from backend.xml_script import XMLProcessing, URLs


@blueprint.route("/index")
@blueprint.route("/index.html")
@login_required
def index():
    xml_data_all_wiso_publs = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PUBLICATIONS"])
    selected_attributes = ["cfTitle", "publYear", "srcAuthors",
                           "Language"]  # TODO: "Language" not working correcty -> XML
    filtered_data_all_wiso_publs = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_publs,
                                                                                  selected_attributes)


    xml_data_all_wiso_pro = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PROJECTS"])
    selected_attributes2 = ["cfTitle", "cfStartDate", "cfEndDate", "relPersIDlead",
                          "funderlink", "Project Type"]  # TODO: "Language" not working correcty -> XML
    filtered_data_all_wiso_pro = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_pro,
                                                                                  selected_attributes2, True)

    for i in range(0, len(filtered_data_all_wiso_pro)):
        filtered_data_all_wiso_pro[i]["project_start"] = datetime.datetime.strptime(
            filtered_data_all_wiso_pro[i]["project_start"], '%Y-%m-%d').strftime('%d.%m.%Y')
        if filtered_data_all_wiso_pro[i]["project_end"] != "None":
            filtered_data_all_wiso_pro[i]["project_end"] = datetime.datetime.strptime(
                filtered_data_all_wiso_pro[i]["project_end"], '%Y-%m-%d').strftime('%d.%m.%Y')


    return render_template('home/index.html', data=data, publications=json.dumps(filtered_data_all_wiso_publs), research_projects=json.dumps(filtered_data_all_wiso_pro))


@blueprint.route("/research-projects-table")
@blueprint.route("/tables")
@blueprint.route("/tables.html")
@login_required
def research_projects_table():
    xml_data_all_wiso_publs = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PUBLICATIONS"])
    selected_attributes = ["cfTitle", "publYear", "srcAuthors", "Language"]  #TODO: "Language" not working correcty -> XML
    filtered_data_all_wiso_publs = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_publs,
                                                                                  selected_attributes)

    xml_data_all_wiso_pro = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PROJECTS"])
    selected_attributes2 = ["cfTitle", "cfStartDate", "cfEndDate", "relPersIDlead",
                            "funderlink", "Project Type"]  # TODO: "Language" not working correcty -> XML
    filtered_data_all_wiso_pro = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_pro,
                                                                                selected_attributes2, True)

    for i in range(0, len(filtered_data_all_wiso_pro)):
        filtered_data_all_wiso_pro[i]["project_start"] = datetime.datetime.strptime(
            filtered_data_all_wiso_pro[i]["project_start"], '%Y-%m-%d').strftime('%d.%m.%Y')
        if filtered_data_all_wiso_pro[i]["project_end"] != "None":
            filtered_data_all_wiso_pro[i]["project_end"] = datetime.datetime.strptime(
                filtered_data_all_wiso_pro[i]["project_end"], '%Y-%m-%d').strftime('%d.%m.%Y')

    return render_template("home/tables.html",
                           research_projects=filtered_data_all_wiso_pro,
                           publications=filtered_data_all_wiso_publs)


@blueprint.route("/publications-table")
@blueprint.route("/tables2")
@blueprint.route("/tables2.html")
@login_required
def publications_table():
    xml_data_all_wiso_publs = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PUBLICATIONS"])
    selected_attributes = ["cfTitle", "publYear", "srcAuthors", "Language", "Keywords"]  #TODO: "Language" not working correcty -> XML
    filtered_data_all_wiso_publs = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_publs, selected_attributes, True)

    xml_data_all_wiso_pro = XMLProcessing.get_xml_data(xml_url=URLs["ALL_WISO_PROJECTS"])
    selected_attributes2 = ["cfTitle", "cfStartDate", "cfEndDate", "relPersIDlead",
                          "funderlink"]  # TODO: "Language" not working correcty -> XML
    filtered_data_all_wiso_pro = XMLProcessing.get_wanted_data_from_data_object(xml_data_all_wiso_pro,
                                                                                  selected_attributes2, True)

    for i in range(0, len(filtered_data_all_wiso_pro)):
        filtered_data_all_wiso_pro[i]["project_start"] = datetime.datetime.strptime(
            filtered_data_all_wiso_pro[i]["project_start"], '%Y-%m-%d').strftime('%d.%m.%Y')
        if filtered_data_all_wiso_pro[i]["project_end"] != "None":
            filtered_data_all_wiso_pro[i]["project_end"] = datetime.datetime.strptime(
                filtered_data_all_wiso_pro[i]["project_end"], '%Y-%m-%d').strftime('%d.%m.%Y')

    return render_template("home/tables2.html",
                           research_projects=filtered_data_all_wiso_pro,
                           publications=filtered_data_all_wiso_publs)
