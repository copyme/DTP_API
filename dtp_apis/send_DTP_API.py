# -*- coding: utf-8 -*-`

#  Copyright (c) Centre Inria d'Université Côte d'Azur, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import logging
import os
import uuid

import requests

from helpers import logger_global


class SendAPI:
    """
    Mixin send API class contains all send methods.

    Methods
    -------
    send_blob_as_text_get_uuid(filename, file_path)
        returns dictionary created from JSON
    send_blob_as_image_get_uuid(filename, file_path)
        return the UUID of the newly created blob
    """

    def send_blob_as_text_get_uuid(self, filename, file_path):
        """
        The method transfers a file as a text-stream to the platform and returns the UUID
        of the corresponding blob.

        Parameters
        ----------
        filename : str, obligatory
            the name of the file under which the file will be known on the platform
        file_path : str, obligatory
            the full path to the file, which will be transferred to the platform

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        str
            return the UUID of the newly created blob, which corresponds to the transferred file
        """

        payload = {
            "description": 'As-Built element, for now a copy of As-Designed',
            "tags": 'WP3,mislata2,integration_v1',
            "visibility": 0
        }

        files = [
            ('file', (filename, open(file_path, 'rb'), 'application/octet-stream'))
        ]
        headers = {
            'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
        }
        session = requests.Session()
        req = requests.Request("POST", self.DTP_CONFIG.get_api_url('send_blob'), headers=headers, data=payload,
                               files=files)
        prepared = req.prepare()

        logger_global.info('HTTP request: \n' + self.__pretty_http_request_to_string(prepared))

        if not self.simulation_mode:
            response = session.send(prepared)
            logger_global.info('Response code: ' + str(response.status_code))
            if response.status_code == 201:
                new_uuid = os.path.basename(response.headers.get('Location'))
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_BLOB: " + new_uuid)
                return new_uuid
            else:
                logger_global.error("Sending blob did not work! Status code: " + str(response.status_code))
                raise Exception("Sending blob did not work! Status code: " + str(response.status_code))
        return str(uuid.uuid4())

    def send_blob_as_image_get_uuid(self, filename, file_path):
        """
        The function transfers a file as an image to the platform and returns the UUID
        of the corresponding blob.

        Parameters
        ----------
        filename : str, obligatory
            the name of the file under which the file will be known on the platform
        file_path : str, obligatory
            the full path to the file, which will be transferred to the platform

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        str
            return the UUID of the newly created blob, which corresponds to the transferred file
        """

        payload = {
            "description": 'As-Built element, for now a copy of As-Designed',
            "tags": 'WP3,mislata2,integration_v1',
            "visibility": 0
        }

        extension = os.path.splitext(filename)[1]
        files = [
            ('file', (filename, open(file_path, 'rb'), 'image/' + extension[1:]))
        ]
        headers = {
            'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
        }
        session = requests.Session()
        req = requests.Request("POST", self.DTP_CONFIG.get_api_uri('send_blob'), headers=headers, data=payload,
                               files=files)
        prepared = req.prepare()

        logging.info('HTTP request: \n' + self.__pretty_http_request_to_string(prepared))

        if not self.simulation_mode:
            response = session.send(prepared)
            logging.info('Response code: ' + str(response.status_code))
            if response.status_code == 201:
                new_uuid = os.path.basename(response.headers.get('Location'))
                if not self.session_logger is None:
                    self.session_logger.info("DTP_API - NEW_BLOB: " + new_uuid)
                return new_uuid
            else:
                logging.error("Sending blob did not work! Status code: " + str(response.status_code))
                raise Exception("Sending blob did not work! Status code: " + str(response.status_code))
        else:
            return str(uuid.uuid4())
