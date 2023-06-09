# -*- coding: utf-8 -*-`


#  Copyright (c) Sophia Antipolis-Méditerranée, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import os
import xml.etree.ElementTree as ET

import validators


class DTPConfig:
    """
    The class is used to map DTP configuration from an XML file.

    Attributes
    ----------
    version : str
        configuration file version
    token : str
        the developer token
    dtp_domain : str
        a domain URL
    api_uris : dictionary
        a map of the API uris
    ontology_uris : dictionary
        a map of the ontology uris        

    Methods
    -------
    get_api_uri(api_type, ID = ' ')
        if the type is a valid type from the XML configuration, then it returns the link,
        if the ID is provided, then the returned link will contain it
    get_ontology_uri(ontology_type)
        if the type is a valid type from the XML configuration, then it returns
        the corresponding ontology URI
    get_token()
        return the developer token
    get_domain()
        returns the DTP domain
    get_version()
        returns the config. file version
    get_object_types()
        returns list, str, object types
    get_object_type_classes()
        returns list, str, object type classes
    get_object_type_conversion_map()
        returns dictionary, str, object type maps   
    """

    def __read_dev_token(self, input_dev_token_file):
        if not os.path.exists(input_dev_token_file):
            raise Exception("Sorry, the dev token file does not exist.")

        token = ''

        f = open(input_dev_token_file, "r")
        lines = f.readlines()

        for line in lines:
            token = token + line.rstrip()
        f.close()

        if len(token) == 0:
            raise Exception("Sorry, the dev token file seems to be empty.")

        return token

    def __map_api_urls(self, uris):
        for uri in uris:
            self.api_uris[uri.attrib['function'].strip()] = uri.text

    def __map_ontology_uris(self, uris):
        for uri in uris:
            self.ontology_uris[uri.attrib['function'].strip()] = uri.text

    def __map_object_types(self, objet_types):
        for obj_type in objet_types:
            if not obj_type.text.strip() in self.objet_types:
                self.objet_types.append(obj_type.text.strip())
            if not obj_type.attrib['field'].strip() in self.objet_type_classes:
                self.objet_type_classes.append(obj_type.attrib['field'].strip())

    def __map_object_type_conversions(self, objet_type_map):
        for type_map in objet_type_map:
            self.objet_type_maps[type_map.attrib['from'].strip()] = type_map.attrib['to'].strip()

    def __init__(self, xml_path):
        config = ET.parse(xml_path).getroot()

        self.version = config.find('VERSION').text.strip()

        token_path = config.find('DEV_TOKEN').text.strip()
        self.token = self.__read_dev_token(token_path)

        self.dtp_domain = config.find('DTP_DOMAIN').text.strip()
        if not validators.url(self.dtp_domain):
            raise Exception("Sorry, the DTP domain URL is not a valid URL.")

        if self.dtp_domain[-1] != '/':
            self.dtp_domain = self.dtp_domain + '/'

        self.kpi_domain = config.find('KPI_DOMAIN').text.strip()
        if not validators.url(self.kpi_domain):
            raise Exception("Sorry, the DTP domain URL is not a valid URL.")

        if self.kpi_domain[-1] != '/':
            self.kpi_domain = self.kpi_domain + '/'

        self.api_uris = {}
        uris = config.find('API_URLS')
        if not uris is None:
            self.__map_api_urls(uris)

        self.ontology_uris = {}
        uris = config.find('ONTOLOGY_URIS')
        if not uris is None:
            self.__map_ontology_uris(uris)

        self.objet_type_classes = []
        self.objet_types = []
        objet_types = config.find('OBJECT_TYPES')
        if not objet_types is None:
            self.__map_object_types(objet_types)

        self.objet_type_maps = {}
        objet_type_map = config.find('OBJECT_TYPE_CONVERSIONS')
        if not objet_type_map is None:
            self.__map_object_type_conversions(objet_type_map)

    def get_api_url(self, api_type, id=' '):
        if len(id.strip()) == 0:
            return self.api_uris[api_type]
        else:
            return self.api_uris[api_type].replace('_ID_', id)

    def get_ontology_uri(self, ontology_type):
        return self.ontology_uris[ontology_type]

    def get_token(self):
        return self.token

    def get_kpi_domain(self):
        return self.kpi_domain

    def get_domain(self):
        return self.dtp_domain

    def get_version(self):
        return self.version

    def get_object_types(self):
        return self.objet_types

    def get_object_type_classes(self):
        return self.objet_type_classes

    def get_object_type_conversion_map(self):
        return self.objet_type_maps
