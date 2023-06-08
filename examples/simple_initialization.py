# -*- coding: utf-8 -*-`

# Copyright Inria Sophia Antipolis-Méditerranée 2022. All Rights Reserved.
# Author: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
# This file cannot be used without a written permission from the author(s).

import sys
sys.path.insert(0, "../")


import argparse
from helpers import logger_global
from DTP_config import DTP_Config
from DTP_API import DTPApi


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
    response = dtp_api.activity_count_connected_task_nodes("http://bim2twin.eu/mislata_wp3/activity91217940_2")
    print('Response:\n', response)
