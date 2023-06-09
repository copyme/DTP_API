# -*- coding: utf-8 -*-`

#  Copyright (c) Centre Inria d'Université Côte d'Azur, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import sys
sys.path.insert(0, "../")


import argparse
from helpers import logger_global
from DTP_config import DTP_Config
from DTP_API import DTPApi


# This method iteretes over pages of 100 nodes until all the nodes are fetched.

def fetch_asbuilt_nodes(dtp_api):
    as_build_elements = dtp_api.fetch_asbuilt_nodes()
    elements = as_build_elements
    while 'next' in elements.keys() and elements['size'] != 0: # more pages detected
        elements = dtp_api.fetch_asbuilt_nodes(elements['next'])
        if elements['size'] <= 0:
            break
        as_build_elements.update(elements)

    return as_build_elements


def parse_args():
    """
    Get parameters from user
    """
    parser = argparse.ArgumentParser(description='Prepare DTP graph')
    parser.add_argument('--xml_path', '-x', type=str, help='path to config xml file', required=True)
    parser.add_argument('--simulation', '-s', default=False, action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    dtp_config = DTP_Config(args.xml_path)
    dtp_api = DTPApi(dtp_config, simulation_mode=args.simulation)
    asbuilt_nodes = fetch_asbuilt_nodes(dtp_api)
    print('Nodes:\n', asbuilt_nodes)
