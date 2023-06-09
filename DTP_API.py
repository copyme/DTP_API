# -*- coding: utf-8 -*-`

#  Copyright (c) Sophia Antipolis-Méditerranée, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).


"""
The file is a collection of methods used to interact with the DTP.
For more information, contact the author(s) listed above.
"""
import argparse
import logging

import requests
import validators
from file_read_backwards import FileReadBackwards

from DTP_config import DTPConfig
from dtp_apis.count_DTP_API import CountAPI
from dtp_apis.create_DTP_API import CreateAPI
from dtp_apis.fetch_DTP_API import FetchAPI
from dtp_apis.link_DTP_API import LinkAPI
from dtp_apis.revert_DTP_API import RevertAPI
from dtp_apis.send_DTP_API import SendAPI
from helpers import logger_global


class DTPApi(FetchAPI, CountAPI, CreateAPI, LinkAPI, RevertAPI, SendAPI):
    """
    Base API class for mixin classes.

    Attributes
    ----------
    simulation_mode : bool
        if True then no changes to the database are performed.
    DTP_CONFIG : class
        an instance of DTP_Config

    Methods
    -------
    init_logger(session_file)
        None
    init_external_logger(session_logger)
        None
    post_general_request(payload, url, headers)
        returns dictionary created from JSON
    general_guarded_request(req_type, payload, url, headers)
        returns dictionary created from JSON
    post_guarded_request(payload, url, headers)
        returns dictionary created from JSON
    put_guarded_request(payload, url, headers)
        returns dictionary created from JSON
    pretty_http_request_to_string(req)
        returns request string
    """

    def __init__(self, dtp_config, simulation_mode=False):
        """
        Parameters
        ----------
        dtp_config : DTP_Config, obligatory
            an instance of DTP_Config
        simulation_mode : bool, optional
            if set to True then method changing
            the database are not send.
        """

        self.simulation_mode = simulation_mode
        self.DTP_CONFIG = dtp_config
        self.session_logger = None

        self.log_markers_node_classes = {
            'new_element': 'NEW_ELEMENT_IRI',
            'new_defect': 'NEW_DEFECT_IRI',
            'new_action': 'NEW_ACTION_IRI',
            'new_operation': 'NEW_OPERATION_IRI',
            'new_constr': 'NEW_CONSTRUCTION_IRI',
            'new_kpi': 'NEW_KPI_IRI'}

        other_log_markers = {'link_elem_blob': 'NEW_LINK_ELEMENT_BLOB',
                             'new_blob': 'NEW_BLOB',
                             'update_asdesigned_param': 'UPDATE_isAsDesigned_PARAM_NODE_OPERATION'}

        try:
            self.log_markers = self.log_markers_node_classes | other_log_markers
        except TypeError:  # dictionary merge operator only in python 3.9+
            self.log_markers = {**self.log_markers_node_classes, **other_log_markers}

    def init_logger(self, session_file):
        """
        Method used for initializing a logger used to collect information about session: only node linking
        and creation is saved at the moment. The method should be used only for single core processing.
        For parallel processing use init_external_logger.

        Parameters
        ----------
        session_file: str obligatory
            the path to the log file, it does not need to exist.
        """

        if len(session_file.strip()) != 0:
            formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            handler = logging.FileHandler(session_file)
            handler.setFormatter(formatter)

            self.session_logger = logging.getLogger('session_DTP')
            self.session_logger.setLevel(logging.INFO)
            self.session_logger.addHandler(handler)

    def init_external_logger(self, session_logger):
        """
        The method allows for passing an external session logger to the instance of the class.

        Parameters
        ----------
        session_logger: Logger (see logging) obligatory
            an instance of the logger class.
        """

        self.session_logger = session_logger

    def post_general_request(self, payload, url=' ', headers=None):
        """
        The method allows for sending POST requests to the DTP. This version does not respect the simulation mode.
        For a simulation mode respecting version see: __post_guarded_request

        Parameters
        ----------
        payload: dict obligatory
            the query to be sent to the platform.
        url: str optional
            the URL used for the HTTPS request
        headers: dict optional
            the header of the request, if not provided the default one is used.
        """

        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
            }

        session = requests.Session()

        if not validators.url(url):
            raise Exception("Sorry, the URL is not a valid URL: " + url)
        req = requests.Request("POST", url, headers=headers, data=payload)

        prepared = req.prepare()

        logger_global.info('HTTP request: \n' + self.pretty_http_request_to_string(prepared))

        response = session.send(prepared)
        logger_global.info('Response code: ' + str(response.status_code))

        if response.ok:
            return response
        else:
            logger_global.error(
                "The response from the DTP is an error. Check the dev token and/or the domain. Status code: " + str(
                    response.status_code))
            raise Exception(
                "The response from the DTP is an error. Check the dev token and/or the domain. Status code: " + str(
                    response.status_code))

    def general_guarded_request(self, req_type, payload, url=' ', headers=None):
        """
        The method allows for sending POST requests to the DTP. This version does respect the simulation mode.
        For a none simulation mode respecting version see: __post_general_request

        Parameters
        ----------
        payload: dict obligatory
            the query to be sent to the platform.
        url: str optional
            the URL used for the HTTPS request
        headers: dict optional
            the header of the request, if not provided the default one is used.
        """

        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
            }

        req_type_fix = req_type.strip().upper()
        if len(req_type_fix) == 0:
            Exception("Request type cannot be empty!")

        if req_type_fix != 'PUT' or req_type_fix != 'POST':
            Exception("Request type has to be: PUT or POST!")

        session = requests.Session()
        req = requests.Request(req_type_fix, url, headers=headers, data=payload)
        prepared = req.prepare()
        logger_global.info('HTTP request: \n' + self.pretty_http_request_to_string(prepared))

        if not self.simulation_mode:
            response = session.send(prepared)
            logger_global.info('Response code: ' + str(response.status_code))
            return response
        return None

    def post_guarded_request(self, payload, url=' ', headers=None):
        return self.general_guarded_request('POST', payload, url, headers)

    def put_guarded_request(self, payload, url=' ', headers=None):
        return self.general_guarded_request('PUT', payload, url, headers)

    def pretty_http_request_to_string(self, req):
        """
        The method provides a printing method for pre-prepared HTTP requests.
        Source: https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw
        Author: AntonioHerraizS

        Usage
        -----
        req = requests.Request("POST", DTP_CONFIG.get_api_uri('send_blob'), headers=headers,
        data=payload, files=files) # any request prepared = req.prepare() __pretty_http_request_to_string(prepared)

        Parameters
        ----------
        req : Request, obligatory
            the pre-prepared request
        """

        request_str = '{}\n{}\r\n{}\r\n\r\n{}\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
            '-----------END-----------'
        )

        return request_str

    def revert_last_session(self, session_file):
        """
        The method can revert the last non-empty sessions.

        Parameters
        ----------
        session_file : str, obligatory
            path to the sessions file
        """

        counter = 0

        with FileReadBackwards(session_file, encoding="utf-8") as frb:
            for line in frb:
                # that will be the last date once the beginning of the file is reached
                msg_date = line[0: line.find(' : ')]
                if self.log_markers['link_elem_blob'] in line:
                    # extract ids from the log
                    index = line.find(self.log_markers['link_elem_blob'])
                    ids = line[index + len(self.log_markers['link_elem_blob']) + 1:].strip()
                    element_uuid = ids.split(',')[0].strip()
                    blob_uuid = ids.split(',')[1].strip()
                    counter = counter + 1
                    self.unlink_node_from_blob(element_uuid, blob_uuid)
                elif self.log_markers['new_blob'] in line:
                    index = line.find(self.log_markers['new_blob'])
                    blob_uuid = line[index + len(self.log_markers['new_blob']) + 1:].strip()
                    self.delete_blob_from_platform(blob_uuid)
                    counter = counter + 1
                elif self.log_markers['update_asdesigned_param'] in l:
                    index = l.find(self.log_markers['update_asdesigned_param'])
                    ids = l[index + len(self.log_markers['update_asdesigned_param']) + 1:].strip()
                    element_iri = ids.split(',')[0].strip()
                    self.undo_update_asdesigned_param_node(element_iri)
                else:
                    try:
                        node_class = next(
                            substring for substring in self.log_markers_node_classes.values() if substring in line)
                    except StopIteration as E:
                        continue
                    index = line.find(node_class)
                    node_iri = line[index + len(node_class) + 1:].strip()
                    try:
                        node_uuid = self.get_uuid_for_iri(node_iri)
                    except Exception as e:
                        if hasattr(e, 'message'):
                            e_msg = e.message
                        else:
                            e_msg = e
                        logger_global.error(
                            'Error at the session revert for entry at : ' + msg_date + ', the message: ' + str(
                                e_msg) + '.')
                        continue
                    self.delete_node_from_graph(node_uuid)
                    counter = counter + 1

        logger_global.info('The session started at: ' + msg_date + ', has been reverted.')


# Below code snippet for testing only

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
    dtp_config = DTPConfig(args.xml_path)
    dtp_api = DTPApi(dtp_config, simulation_mode=args.simulation)
    response = dtp_api.activity_count_connected_task_nodes("http://bim2twin.eu/mislata_wp3/activity91217940_2")
    print('Response:\n', response)
