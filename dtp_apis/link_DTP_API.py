# -*- coding: utf-8 -*-`

#  Copyright (c) Centre Inria d'Université Côte d'Azur, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import json

from helpers import logger_global


class LinkAPI:
    """
    Mixin link API class contains all link methods.

    Methods
    -------
    link_node_element_to_blob(node_uuid, blob_uuid)
        returns bool, True if success and False otherwise
    link_node_element_to_defect(element_node_iri, defect_node_iri)
        returns bool, True if success and False otherwise
    link_node_operation_to_action(oper_node_iri, action_node_iri)
        returns bool, True if success and False otherwise
    link_node_schedule_to_constr(schedule_node_iri, constr_node_iri)
        returns bool, True if success and False otherwise
    link_node_constr_to_operation(constr_node_iri, oper_node_iri)
        returns bool, True if success and False otherwise
    """

    def link_node_element_to_blob(self, node_uuid, blob_uuid):
        """
        The method links a blob to an element.

        Parameters
        ----------
        node_uuid : str, obligatory
            a valid element UUID of an element which will be linked to a blob
        blob_uuid : str, obligatory
            a valid blob UUID

        Returns
        ------
        bool
            True if the element has been linked with a blob, and False otherwise
        """

        payload = json.dumps({
            "blob_uuid": blob_uuid,
            "avatar_uuids": [node_uuid],
            "ignore_conflicts": False
        })

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_LINK_ELEMENT_BLOB: " + node_uuid + ', ' + blob_uuid)
                return True
            else:
                logger_global.error("Linking nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def link_node_element_to_defect(self, element_node_iri, defect_node_iri):
        """
        The method links a defect with an element.

        Parameters
        ----------
        element_node_iri : str, obligatory
            a valid element IRI of an element, which will be linked to a defect
        defect_node_iri : str, obligatory
            a valid defect's IRI

        Returns
        ------
        bool
            True if the element has been linked with a defect, and False otherwise
        """

        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": element_node_iri,
            "_outE": [{
                "_label": self.DTP_CONFIG.get_ontology_uri('hasGeometricDefect'),
                "_targetIRI": defect_node_iri
            }]
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        "DTP_API - NEW_LINK_ELEMENT_DEFECT: " + element_node_iri + ', ' + defect_node_iri)
                return True
            else:
                logger_global.error("Linking nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def link_node_operation_to_action(self, oper_node_iri, action_node_iri):
        """
        The method links an action with an operation.

        Parameters
        ----------
        oper_node_iri : str, obligatory
            a valid operation IRI
        action_node_iri : str, obligatory
            a valid action IRI

        Returns
        ------
        bool
            True if the element has been linked with a defect, and False otherwise
        """

        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": oper_node_iri,
            "_outE": [{
                "_label": self.DTP_CONFIG.get_ontology_uri('hasAction'),
                "_targetIRI": action_node_iri
            }]
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        "DTP_API - NEW_LINK_OPERATION_ACTION: " + oper_node_iri + ', ' + action_node_iri)
                return True
            else:
                logger_global.error("Linking nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def link_node_schedule_to_constr(self, schedule_node_iri, constr_node_iri):
        """
        The method links a construction with a schedule.

        Parameters
        ----------
        schedule_node_iri : str, obligatory
            a valid schedule IRI
        constr_node_iri : str, obligatory
            a valid construction IRI

        Returns
        ------
        bool
            True if the element has been linked with a defect, and False otherwise
        """

        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": schedule_node_iri,
            "_outE": [{
                "_label": self.DTP_CONFIG.get_ontology_uri('hasConstruction'),
                "_targetIRI": constr_node_iri
            }]
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        "DTP_API - NEW_LINK_SCHEDULE_CONSTR: " + schedule_node_iri + ', ' + constr_node_iri)
                return True
            else:
                logger_global.error("Linking nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def link_node_constr_to_operation(self, constr_node_iri, oper_node_iri):
        """
        The method links a operation with a construction.

        Parameters
        ----------
        constr_node_iri : str, obligatory
            a valid construction IRI
        oper_node_iri : str, obligatory
            a valid operation IRI

        Returns
        ------
        bool
            True if the element has been linked with a defect, and False otherwise
        """

        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": constr_node_iri,
            "_outE": [{
                "_label": self.DTP_CONFIG.get_ontology_uri('hasOperation'),
                "_targetIRI": oper_node_iri
            }]
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        "DTP_API - NEW_LINK_CONSTR_OPERATION: " + constr_node_iri + ', ' + oper_node_iri)
                return True
            else:
                logger_global.error("Linking nodes failed. Response code: " + str(response.status_code))
                return False
        return True
