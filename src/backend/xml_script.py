from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET
import numpy as np

SVEN_URL = r"https://cris.fau.de/ws-cached/public/infoobject/getautorelated/Person/203395223/PERS_2_PUBL_1"
ALL_WISO_PUBLICATIONS = r"https://cris.fau.de/ws-cached/public/infoobject/getautorelated/Organisation/105979734/ORGA_2_PUBL_1"
ALL_WISO_PROJECTS = r"https://cris.fau.de/ws-cached/public/infoobject/getautorelated/Organisation/105979734/ORGA_2_PROJ_1"


class XMLProcessing:
    def __init__(self, *, xml_path=None, xml_url=None, xml_url_txt_path=None):
        self.xml_path = xml_path
        self.xml_url = xml_url
        self.xml_url_txt_path = xml_url_txt_path
        self.xml_data_raw = None

    def load_xml_url_txt(self):
        if not self.xml_url_txt_path:
            raise FileNotFoundError(f"[ERROR] xml_url_txt fot found")
        with open(self.xml_url_txt_path, "r", encoding="utf-8") as file:
            self.xml_data_raw = file.read()
            print(file)

    @staticmethod
    def get_xml_data(*, path=None, xml_url=None):
        tree = None
        if path:
            tree = ET.parse(path)
        elif xml_url:
            xml_data = requests.get(xml_url)
            tree = ET.fromstring(xml_data.content)
        return tree

    @staticmethod
    def get_all_attributes_names(tree):
        attribute_list = []
        for child in tree.iter("*"):
            try:
                attribute_list.append(child.attrib["name"])
            except Exception:
                pass
        return list(set(attribute_list))

    #Filtermethode, filtert nach Kategorien (f_attr) und Werten (f_value). Der Rückgabewert (return_value) ist ein Attribut
    #der Puplikationen, das zurückgegeben werden soll
    @staticmethod
    def filter(tree, f_attr, f_value):
        puplis = []
        #Für jede Kategorie und dem dazu passenden Wert wird der Filterprozess einmal durchlaufen
        for (attr, value) in zip(f_attr, f_value):
            #------ Auswahl aller Puplikationen, auf die der Filter passt ------
            for data_object in tree:   #tree = <DataObjects>
                for attribute in data_object:  #elem = <DataObject>
                    if attribute.attrib.get("name") == attr:  #e = <Attribute>
                        for data in attribute:   #var = <Data>

                            if str(data.text).isdigit(): #Überprüfung, ob nummerische Werte verglichen werden
                                if value == str(data.text):
                                    #print("Zahl Filter")
                                    puplis.append(data_object) #Fügt alle Puplikationen, auf die der Filter zutrifft, einer Liste hinzu
                            else:
                                if value in str(data.text):
                                    #print("Wort Filter")
                                    puplis.append(data_object) #Fügt alle Puplikationen, auf die der Filter zutrifft, einer Liste hinzu
                                    #print(var.text)


        #------ Auswertung der Filterergebnisse ------

        #Kleine Erklärung, wie der multiple Filter funktioniert:
        #Alles landet in der Liste puplis, also alles, was zu attr 1, 2, 3, ..., n passt.
        #Am Ende überprüfe ich nur die Duplikate und filter' diese raus. Wenn ein Element genau so oft vorkommt,
        #wie es Attribute gibt, treffen alle Filter auf dieses Element zu.
        #Wichtig hierbei, das ganze muss noch weiter getestet werden, konnte es bisher nur mit einem kleinen Testdatensatz testen.
        dup = Counter(puplis)
        puplis = list([item for item in dup if dup[item] == len(list(f_attr))])

        #print(len(puplis))
        return puplis

    #Gibt den gewollten Wert (returnValue) aus einer beliebig langen Liste (oder was auch immer) von <dataObject>s zurück.
    #Der Wert wird als String wiedergegeben
    def get_wanted_data_from_data_object(dataObjects, returnValues):
        result = []
        for dataObj in dataObjects:
            return_object = []
            for attribute in dataObj:
                if attribute.attrib.get("name") in returnValues:
                    for data in attribute:
                        return_object.append([attribute.attrib.get("name"), str(data.text)])
            result.append(return_object)
        #print(len(result))
        return result

    #Gibt die Puplikationen ODER Projekte zurück, die in den letzten "lastDaysCount" Tagen veröffentlicht wurden bzw abgeschlossen
    #wurden. (Bei Pupl. veröffentlicht, bei Projekten abgeschlossen).
    @staticmethod
    def get_last_created_items(tree, lastDaysCount = 3, isPupl = True):
        results = []
        dateFormat = "%Y-%m-%d"  # Im XML werden Datumseinträge im Format Jahr/Monat/Tag angegeben.
        today = datetime.today()
        compareDate = today - timedelta(days=lastDaysCount)  # Heute - lastDaysCount Tage = compareDate

        print(type(compareDate))
        if isPupl:  #Für Puplikationen
            for child in tree:
                #Vergleicht, ob die Puplikation im CRIS System nach 'lastDaysCount' Tagen erstellt wurde
                createdOnDateString = child.attrib.get("createdOn").split('T')[0]
                #Schaut, ob die Puplikation nach dem compareDate erstellt wurde
                if datetime.strptime(createdOnDateString, dateFormat) >= compareDate:
                    results.append(child)
        else:   #Für Projekte
            for child in tree:
                for attribute in child:
                    if attribute.attrib.get("name") == 'cfEndDate':
                        for data in attribute:
                            if data.text is not None \
                                    and datetime.strptime(data.text, dateFormat) >= compareDate \
                                    and datetime.strptime(data.text, dateFormat) < today:
                                print(datetime.strptime(data.text, dateFormat))
                                results.append(child)

        print(len(results))
        return results

    #Parameter: tree = XML-Datei;
    # x_axis = Datenwert, der sich ändern soll (z.B. Jahr)
    # y_axis = Datenwert, der gleich bleiben soll (z.B. Autor)
    # x__values = Die Werte, für die der y-Wert ausgewertet werden soll (z.B. [2019, 2020, 2021, 2022])
    # y_value = Der Wert, der gleich bleibt (z.B. "Sven")
    @staticmethod
    def get_graph_data(tree, x_axis, y_axis, x__values, y_value):

        result = []
        attr = [x_axis, y_axis]
        test = 0
        print(attr)

        for x_val in x__values:
            values = [x_val, y_value]
            print(values)
            amount = XMLProcessing.filter(tree, attr, values)
            result.append((values, len(amount)))
            test += len(amount)
        print(result)
        print(test)
        return result

    @staticmethod
    def get_website_of_data_object(dataObject):
        url = "https://cris.fau.de/converis/portal/"
        dataObjectType = dataObject.attrib.get("type")
        dataObjectID = dataObject.attrib.get("id")
        suffix = "?auxfun=&lang=de_DE"
        return url + dataObjectType + "/" + dataObjectID + suffix

    #Gibt die Anzahl aller Einträge und die Wachstumsrate zurück
    def get_metrics(tree):
        #count_dooku = len(tree.getchildren()) #Anzahl aller Dateneinträge von tree
        count_dooku = tree.attrib.get("size")
        print(count_dooku)
        #print(count_dooku)
        currentYear = str(datetime.today().year)
        lastyear = str(int(currentYear) - 1)
        #print(currentYear + " " + lastyear)
        count_last_year = len(XMLProcessing.filter(tree, ["publYear"], [lastyear])) #Anzahl an DatenEinträgen aus diesem Jahr
        count_this_year = len(XMLProcessing.filter(tree, ["publYear"], [currentYear])) #Anzahl an DatenEinträgen aus letztem Jahr
        #print(str(count_this_year) + " " + str(count_last_year))
        growth = (count_this_year/ count_last_year) * 100
        growth = str(float("{:.2f}".format(growth))) + "%"
        print(growth)
        return [count_dooku, growth]

    def get_all_keywords(tree):
        keys = XMLProcessing.get_wanted_data_from_data_object(tree, ["Keywords"])
        keywords = []
        for element in keys:
            for subElement in element:
                keywords.append(str(subElement[1]))

        for i in range(0, 10):  #Ich habe keine Ahnung, warum, aber erst, wenn ich das mehrfach wiederhole, werden alle Nones entfernt
            for element in keywords:
                if element == 'None':
                    keywords.remove((element))

        keystring = ""
        for element in keywords:
            keystring += " " + element + ";"

        keystring = keystring.replace(";;", ";")
        keystring = keystring.replace(";", ",")
        #print(keystring)
        #print(keywords)
        keywords = keystring.split(",")

        final_keywords = []
        for element in keywords:
            temp = str(element)[1:]
            final_keywords.append(temp)
        #print(final_keywords)

        final_keywords = list(dict.fromkeys(final_keywords))
        #print(final_keywords)

        return final_keywords

#===================================Renes Testwiese=========================================

e = XMLProcessing.get_xml_data(xml_url=ALL_WISO_PUBLICATIONS)
#p = XMLProcessing.get_xml_data(xml_url=ALL_WISO_PROJECTS)
#filter = ["srcAuthors", "publYear"]
#value = ["Sven", "2020"]
#filter_result = XMLProcessing.filter(e, filter, value)
#print(filter_result)
#print(XMLProcessing.get_wanted_data_from_data_object(filter_result, "cfTitle"))
#for r in filter_result:
#    print(XMLProcessing.get_website_of_data_object(r))
#lc = XMLProcessing.get_last_created_items(e, 1000)
#print(XMLProcessing.get_wanted_data_from_data_object(e, ["cfTitle", "publYear", "srcAuthors"]))
#print(lc)
#x_values = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
#XMLProcessing.get_graph_data(e, 'publYear', 'srcAuthors', x_values, "Sven")

print(XMLProcessing.get_metrics(e))

#XMLProcessing.get_all_keywords(e)
#=============================================================================================


# XMLProcessor = XMLProcessing()
# data_sven = XMLProcessor.get_xml_data(xml_url=SVEN_URL)
# all_attributes_sven = XMLProcessor.get_all_attributes_names(data_sven)
#
# all_wiso_projects = XMLProcessor.get_xml_data(xml_url=ALL_WISO_PROJECTS)
# all_wiso_publications = XMLProcessor.get_all_attributes_names(xml_url=ALL_WISO_PUBLICATIONS)
#
# print(all_attributes)
# print(f"Anzahl Attribute: {len(all_attributes)}")
