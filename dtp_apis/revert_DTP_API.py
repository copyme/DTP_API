# -*- coding: utf-8 -*-`

#  Copyright (c) Sophia Antipolis-Méditerranée, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import json

import requests
import validators

from helpers import logger_global


class RevertAPI:
    """
    Mixin revert API class contains revert function to roll back to previous stage with session logs.

    Methods
    -------
    delete_node_from_graph(node_uuid)
        returns bool, True if success and False otherwise
    delete_node_from_graph_with_iri(node_iri)
        returns bool, True if success and False otherwise
    unlink_node_from_blob(node_uuid, blob_uuid)
        returns bool, True if success and False otherwise
    delete_blob_from_platform(blob_uuid)
        returns bool, True if success and False otherwise
    undo_update_asdesigned_param_node(node_iri)
        returns bool, True if success and False otherwise
    """

    def delete_node_from_graph(self, node_uuid):
        """
        The method deletes a node from DTP.

        Parameters
        ----------
        node_uuid : str, obligatory
            a valid uuid of a node to remove.

        Returns
        ------
        bool
            True if an element has been deleted and False otherwise
        """

        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
        }

        session = requests.Session()
        req = requests.Request("DELETE", self.DTP_CONFIG.get_api_url('delete_avatar', node_uuid), headers=headers,
                               data=payload)
        prepared = req.prepare()

        logger_global.info('HTTP request: \n' + self.pretty_http_request_to_string(prepared))

        if not self.simulation_mode:
            response = session.send(prepared)
            logger_global.info('Response code: ' + str(response.status_code))

            if response.ok:
                logger_global.info("The node: " + node_uuid + ", has been deleted.")
                return True
            else:
                logger_global.error(
                    "The node: " + node_uuid + ", cannot be deleted. Status code: " + str(response.status_code))
                return False
        return True

    def delete_node_from_graph_with_iri(self, node_iri):
        """
        The method deletes a node from DTP.

        Parameters
        ----------
        node_iri : str, obligatory
            a valid iri of a node to remove.

        Returns
        ------
        bool
            True if an element has been deleted and False otherwise
        """

        if not validators.url(node_iri):
            raise Exception("Sorry, the target IRI is not a valid URL.")

        payload = json.dumps(
            {
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": node_iri
            }
        )

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                logger_global.info("The node: " + node_iri + ", has been deleted.")
                return True
            else:
                logger_global.error(
                    "The node: " + node_iri + ", cannot be deleted. Status code: " + str(response.status_code))
                return False
        return True

    def unlink_node_from_blob(self, node_uuid, blob_uuid):
        """
        The method unlinks a blob from a node.

        Parameters
        ----------
        node_uuid : str, obligatory
            UUID of a node from which the blob
            identified by blob_uuid will be unlinked
        blob_uuid : str, obligatory
            a valid uuid of a blob to be unlinked from
            the node identified by node_uuid

        Returns
        ------
        bool
            True if a blob has been unlinked and False otherwise
        """

        payload = json.dumps({
            "blob_uuid": blob_uuid,
            "avatar_uuids": [node_uuid],
            "ignore_conflicts": False
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
        }

        session = requests.Session()
        req = requests.Request("POST", self.DTP_CONFIG.get_api_url('unlink_blob'), headers=headers, data=payload)
        prepared = req.prepare()

        logger_global.info('HTTP request: \n' + self.pretty_http_request_to_string(prepared))

        if not self.simulation_mode:
            response = session.send(prepared)
            logger_global.info('Response code: ' + str(response.status_code))

            if response.ok:
                logger_global.info("The blob : " + blob_uuid + ", unlinked from the element: " + node_uuid)
                return True
            else:
                logger_global.error(
                    "Unlinking blob : " + blob_uuid + ", from the element: " + node_uuid + ",  failed. Status code: " + str(
                        response.status_code))
                return False
        return True

    def delete_blob_from_platform(self, blob_uuid):
        """
        The method deletes a blob from DTP

        Parameters
        ----------
        blob_uuid : str, obligatory
            a valid uuid of a blob to remove.

        Returns
        ------
        bool
            True if a blob has been deleted and False otherwise
        """

        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.DTP_CONFIG.get_token()
        }

        session = requests.Session()
        req = requests.Request("DELETE", self.DTP_CONFIG.get_api_url('delete_blob', blob_uuid), headers=headers,
                               data=payload)
        prepared = req.prepare()

        logger_global.info('HTTP request: \n' + self.pretty_http_request_to_string(prepared))

        if not self.simulation_mode:
            response = session.send(prepared)
            logger_global.info('Response code: ' + str(response.status_code))

            if response.ok:
                logger_global.error("The blob: " + blob_uuid + ", has been deleted.")
                return True
            else:
                logger_global.error(
                    "The blob: " + blob_uuid + ", cannot be deleted. Status code: " + str(response.status_code))
                return False
        return True

    def delete_asdesigned_param_node(self, node_iri):
        """
        The method removes isAsDesigned field from node identified with node_iri

        Parameters
        ----------
        node_iri: str, obligatory
            an iri of a node to act on

        Returns
        -------
        bool
            True if a blob has been node has been updated and False otherwise
        """
        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": node_iri,
            self.DTP_CONFIG.get_ontology_uri('isAsDesigned'): "delete"
            # 'delete' is a placeholder to ensure payload is valid
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_unset'))
        if not self.simulation_mode:
            if response.ok:
                logger_global.info(f"The asDesigned fields is removed from element: {node_iri}")
                return True
            else:
                logger_global.error("Updating nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def revert_node_update(self, node_iri, dump_path):
        """
        Method to revert a node from logged node json file

        Parameters
        ----------
        node_iri: str, obligatory
            an iri of a node to act on
        dump_path: str, obligatory
            path to logged node json file

        Returns
        -------
        bool
            True if node has been updated and False otherwise
        """
        with open(dump_path) as f:
            node_info = json.load(f)

        payload = node_info['items'][0]
        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                logger_global.info(f"Revert node: {node_iri}")
                return True
            else:
                logger_global.error(
                    "Revert updating node failed. Response code: " + str(response.status_code))
                return False
        return True
