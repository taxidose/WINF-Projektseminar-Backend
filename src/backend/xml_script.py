from pathlib import Path
import requests
import xml.etree.ElementTree as ET

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

    #Filtermethode, filtert nach einer Kategorie (f_attr) und einem Wert (f_value). Der Rückgabewert (return_value) ist ein Attribut
    #der Puplikationen, das zurückgegeben werden soll
    def filter (tree, f_attr, f_value, return_value):
        puplis = []
        #------ Auswahl aller Puplikationen, auf die der Filter passt ------
        for elem in tree:   #tree = <DataObjects>
            for e in elem:  #elem = <DataObject>
                if e.attrib.get("name") == f_attr:  #e = <Attribute>
                    for var in e:   #var = <Data>
                        if f_value in str(var.text):
                            puplis.append(elem) #Fügt alle Puplikationen, auf die der Filter zutrifft, einer Liste hinzu
                            print(var.text)
        #------ Auswertung der Filterergebnisse und Rückgabe des gescuhten Attributs ------
        result = []
        for elem in puplis:
            for e in elem:
                if e.attrib.get("name") == return_value:
                    for var in e:
                        result.append(str(var.text))
        print(len(result))
        return result



e = XMLProcessing.get_xml_data(xml_url=ALL_WISO_PUBLICATIONS)
print(XMLProcessing.filter(e,"srcAuthors", "Sven", "cfTitle"))


# XMLProcessor = XMLProcessing()
# data_sven = XMLProcessor.get_xml_data(xml_url=SVEN_URL)
# all_attributes_sven = XMLProcessor.get_all_attributes_names(data_sven)
#
# all_wiso_projects = XMLProcessor.get_xml_data(xml_url=ALL_WISO_PROJECTS)
# all_wiso_publications = XMLProcessor.get_all_attributes_names(xml_url=ALL_WISO_PUBLICATIONS)
#
# print(all_attributes)
# print(f"Anzahl Attribute: {len(all_attributes)}")
