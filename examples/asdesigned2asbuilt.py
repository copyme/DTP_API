# -*- coding: utf-8 -*-`
#  Copyright (c) Sophia Antipolis-Méditerranée, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import argparse
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, "../")

from DTP_API import DTPApi
from DTP_config import DTPConfig
import helpers
from helpers import logger_global


def is_asdesigned(dtp_config, element):
    if dtp_config.get_ontology_uri('isAsDesigned') in element.keys():
        if element[dtp_config.get_ontology_uri('isAsDesigned')]:
            return True
        else:
            return False
    else:
        return True

def create_iri_as_built(as_designed_iri, nb_connected_components):
        base_name_as_designed = os.path.basename(as_designed_iri)
        if base_name_as_designed.lower().find('ifc') >= 0:
            as_built_iri = as_designed_iri.replace('ifc', 'asbuilt') + '_' + str(nb_connected_components + 1)
        else:
            as_built_iri = os.path.dirname(as_designed_iri) + '/asbuilt' + base_name_as_designed + '_' + str(
                nb_connected_components + 1)
        return as_built_iri


def parse_args():
    """
    Get parameters from user
    """
    parser = argparse.ArgumentParser(description='Fetch all element with additional filter')
    parser.add_argument('--xml_path', '-x', type=str, help='path to config xml file', required=True)
    parser.add_argument('--simulation', '-s', default=False, action='store_true')
    parser.add_argument('--log_dir', '-l', type=str, help='path to log dir', required=True)

    return parser.parse_args()


if __name__ == "__main__":
    logger_global.info('New session has been started.')
    args = parse_args()
    dtp_config = DTPConfig(args.xml_path)
    dtp_api = DTPApi(dtp_config, simulation_mode=args.simulation)
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    log_path = os.path.join(args.log_dir, f"db_session-{time.strftime('%Y%m%d-%H%M%S')}.log")
    dtp_api.init_logger(log_path)
    
    
    elements = dtp_api.query_all_pages(dtp_api.fetch_element_nodes, "ifc:Class", "IfcWall")
    
    for element in elements['items']:
        if is_asdesigned(dtp_config, element): #this soon should not be needed
            asbuild_iri = create_iri_as_built(element['_iri'], 0)
            timestamp = helpers.get_timestamp_dtp_format(datetime.now())
            element_type = helpers.get_element_type(dtp_config, element)
            
            # this soon should not be needed
            if element_type.strip() in dtp_config.get_object_type_conversion_map().keys():
                element_type = dtp_config.get_object_type_conversion_map()[element_type.strip()]            
            
            dtp_api.create_asbuilt_node(asbuild_iri, 100, timestamp, element_type, element['_iri'])
        

