# -*- coding: utf-8 -*-`
#  Copyright (c) Sophia Antipolis-Méditerranée, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import argparse
import os
import sys
import time

from DTP_API import DTPApi
from DTP_config import DTPConfig

sys.path.insert(0, "../")


def parse_args():
    """
    Get parameters from user
    """
    parser = argparse.ArgumentParser(
        description='Counts task nodes connected to a node identified by activity_node_iri')
    parser.add_argument('--xml_path', '-x', type=str, help='path to config xml file', required=True)
    parser.add_argument('--simulation', '-s', default=False, action='store_true')
    parser.add_argument('--log_dir', '-l', type=str, help='path to log dir', required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    dtp_config = DTPConfig(args.xml_path)
    dtp_api = DTPApi(dtp_config, simulation_mode=args.simulation)
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    log_path = os.path.join(args.log_dir, f"db_session-{time.strftime('%Y%m%d-%H%M%S')}.log")
    dtp_api.init_logger(log_path)
    response = dtp_api.activity_count_connected_task_nodes("http://bim2twin.eu/mislata_wp3/activity91217940_2")
    print('Response:\n', response)
