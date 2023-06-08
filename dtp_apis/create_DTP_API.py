# -*- coding: utf-8 -*-`

# Copyright Inria Sophia Antipolis-Méditerranée 2022. All Rights Reserved.
# Author: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
# This file cannot be used without a written permission from the author(s).

import json
import secrets

import validators
from helpers import logger_global


class CreateAPI:
    """
    Mixin create API class contains all create methods.

    Methods
    -------
    create_asbuilt_node(url)
        returns bool, True if success and False otherwise
    create_defect_node(url)
        returns bool, True if success and False otherwise
    create_kpi_nodefectsperwork(url)
        returns bool, True if success and False otherwise
    create_action_node(element_uuid)
        returns bool, True if success and False otherwise
    create_operation_node(blob_uuid)
        returns bool, True if success and False otherwise
    create_construction_node()
        returns bool, True if success and False otherwise
    create_kpi_zerodefectwork(IRI)
        returns bool, True if success and False otherwise
    """

    def create_asbuilt_node(self, element_iri_uri, progress, timestamp, element_type, target_iri):
        """
        The method creates a new As-Built element.

        Parameters
        ----------
        element_iri_uri : str, obligatory
            the full IRI of the new As-Built element
        progress : int, obligatory
            the progress in percentage of the new As-Built element
        timestamp : datetime, obligatory
            associated timestamp in the isoformat(sep="T", timespec="seconds")
        element_type : str, obligatory
            element type as defined by the ontology, normally it should be
            the same type as the type of the corresponding As-Designed element
        target_iri : str, obligatory
            the IRI of the associated element; here it should correspond to the IRI
            of the respective As-Designed element

        Raises
        ------
        It can raise an exception if the target or element IRIs are not valid URIs

        Returns
        ------
        bool
            True if the element has been created without an error, and False otherwise
        """

        if not validators.url(element_iri_uri):
            raise Exception("Sorry, the target IRI is not a valid URL.")

        if not validators.url(target_iri):
            raise Exception("Sorry, the target IRI is not a valid URL.")

        ontology_id = secrets.token_hex(11)

        if progress == 100:
            payload = json.dumps([
                {
                    "_classes": [self.DTP_CONFIG.get_ontology_uri('classElement')],
                    "_domain": self.DTP_CONFIG.get_domain(),
                    "_iri": element_iri_uri,
                    "_visibility": 0,
                    self.DTP_CONFIG.get_ontology_uri('id'): ontology_id,
                    self.DTP_CONFIG.get_ontology_uri('isAsDesigned'): False,
                    self.DTP_CONFIG.get_ontology_uri('timeStamp'): timestamp,
                    self.DTP_CONFIG.get_ontology_uri('progress'): progress,
                    self.DTP_CONFIG.get_ontology_uri('hasElementType'): element_type,
                    self.DTP_CONFIG.get_ontology_uri('hasGeometryStatusType'): self.DTP_CONFIG.get_ontology_uri(
                        'CompletelyDetected'),
                    "_outE": [
                        {
                            "_label": self.DTP_CONFIG.get_ontology_uri('intentStatusRelation'),
                            "_targetIRI": target_iri
                        }
                    ]
                }
            ])
        else:
            payload = json.dumps([
                {
                    "_classes": [self.DTP_CONFIG.get_ontology_uri('classElement')],
                    "_domain": self.DTP_CONFIG.get_domain(),
                    "_iri": element_iri_uri,
                    self.DTP_CONFIG.get_ontology_uri('id'): ontology_id,
                    self.DTP_CONFIG.get_ontology_uri('isAsDesigned'): False,
                    self.DTP_CONFIG.get_ontology_uri('timeStamp'): timestamp,
                    self.DTP_CONFIG.get_ontology_uri('progress'): progress,
                    self.DTP_CONFIG.get_ontology_uri('hasElementType'): element_type,
                    "_outE": [
                        {
                            "_label": self.DTP_CONFIG.get_ontology_uri('intentStatusRelation'),
                            "_targetIRI": target_iri
                        }
                    ]
                }
            ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_ELEMENT_IRI: " + element_iri_uri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True

    def create_defect_node(self, defect_class, defect_node_iri, defect_criticality, timestamp, defect_type):
        """
        The method counts defect nodes connected to a node identified by node_iri

        Parameters
        ----------
        node_iri : str, obligatory
            a valid IRI of a node.

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        int
            return True if a new defect node has been created and False otherwise.
        """

        if not validators.url(defect_node_iri):
            raise Exception("Sorry, the IRI is not a valid URL.")

        payload = json.dumps([
            {
                "_classes": [defect_class],
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": defect_node_iri,
                "_visibility": 0,
                self.DTP_CONFIG.get_ontology_uri('hasDefectType'): defect_type,
                self.DTP_CONFIG.get_ontology_uri('timeStamp'): timestamp,
                self.DTP_CONFIG.get_ontology_uri('defect_criticality'): defect_criticality
            }
        ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_DEFECT_IRI: " + defect_node_iri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True

    def create_kpi_nodefectsperwork(self, kpi_node_iri, task_type, value, ref_quant, sampl_quant, inter_start_date,
                                    inter_end_date):

        if not validators.url(kpi_node_iri):
            raise Exception("Sorry, the IRI is not a valid URL.")

        payload = json.dumps([
            {
                "_classes": [self.DTP_CONFIG.get_ontology_uri('kpiNumberOfDefectsPerWork')],
                "_domain": self.DTP_CONFIG.get_kpi_domain(),
                "_iri": kpi_node_iri,
                "_visibility": 0,
                self.DTP_CONFIG.get_ontology_uri('kpiHasTaskType'): task_type,
                self.DTP_CONFIG.get_ontology_uri('kpiValue'): value,
                self.DTP_CONFIG.get_ontology_uri('kpiReferenceQuantity'): ref_quant,
                self.DTP_CONFIG.get_ontology_uri('kpiSampleQuantity'): sampl_quant,
                self.DTP_CONFIG.get_ontology_uri('kpiIntervalStartDate'): inter_start_date,
                self.DTP_CONFIG.get_ontology_uri('kpiIntervalEndDate'): inter_end_date,
            }
        ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_KPI_IRI: " + kpi_node_iri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True

    def create_action_node(self, taskType, action_node_iri, target_task_iri, target_as_built_iri, contractor,
                           processStart, processEnd):
        """
        The method creates a new action.

        Parameters
        ----------
        node_iri : str, obligatory
            a valid IRI of a node.

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        int
            return True if a new defect node has been created and False otherwise.
        """

        if not validators.url(action_node_iri):
            raise Exception("Sorry, the IRI is not a valid URL.")

        payload = json.dumps([
            {
                "_classes": [self.DTP_CONFIG.get_ontology_uri('asPerformedAction')],
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": action_node_iri,
                "_visibility": 0,
                self.DTP_CONFIG.get_ontology_uri('hasTaskType'): taskType,
                self.DTP_CONFIG.get_ontology_uri('processStart'): processStart,
                self.DTP_CONFIG.get_ontology_uri('processEnd'): processEnd,
                self.DTP_CONFIG.get_ontology_uri('constructionContractor'): contractor,
                "_outE": [
                    {
                        "_label": self.DTP_CONFIG.get_ontology_uri('hasTarget'),
                        "_targetIRI": target_as_built_iri
                    },
                    {
                        "_label": self.DTP_CONFIG.get_ontology_uri('intentStatusRelation'),
                        "_targetIRI": target_task_iri
                    }
                ]
            }
        ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_ACTION_IRI: " + action_node_iri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True

    def create_operation_node(self, taskType, oper_node_iri, target_activity_iri, processStart, processEnd):
        """
        The method creates a new operation.

        Parameters
        ----------
        node_iri : str, obligatory
            a valid IRI of a node.

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        int
            return True if a new defect node has been created and False otherwise.
        """

        if not validators.url(oper_node_iri):
            raise Exception("Sorry, the IRI is not a valid URL.")

        payload = json.dumps([
            {
                "_classes": [self.DTP_CONFIG.get_ontology_uri('asPerformedOperation')],
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": oper_node_iri,
                "_visibility": 0,
                self.DTP_CONFIG.get_ontology_uri('hasTaskType'): taskType,
                self.DTP_CONFIG.get_ontology_uri('processStart'): processStart,
                self.DTP_CONFIG.get_ontology_uri('processEnd'): processEnd,
                "_outE": [
                    {
                        "_label": self.DTP_CONFIG.get_ontology_uri('intentStatusRelation'),
                        "_targetIRI": target_activity_iri
                    }
                ]
            }
        ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_OPERATION_IRI: " + oper_node_iri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True

    def create_construction_node(self, productionMethodType, constr_node_iri, workpkg_node_iri):
        """
        The method creates a new operation.

        Parameters
        ----------
        node_iri : str, obligatory
            a valid IRI of a node.

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        int
            return True if a new defect node has been created and False otherwise.
        """

        if not validators.url(constr_node_iri):
            raise Exception("Sorry, the IRI is not a valid URL.")

        payload = json.dumps([
            {
                "_classes": [self.DTP_CONFIG.get_ontology_uri('asPerformedConstruction')],
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": constr_node_iri,
                "_visibility": 0,
                self.DTP_CONFIG.get_ontology_uri('hasProductionMethodType'): productionMethodType,
                "_outE": [
                    {
                        "_label": self.DTP_CONFIG.get_ontology_uri('intentStatusRelation'),
                        "_targetIRI": workpkg_node_iri
                    }
                ]
            }
        ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_CONSTRUCTION_IRI: " + constr_node_iri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True

    def create_kpi_zerodefectwork(self, kpi_node_iri, value, ref_quant, sampl_quant, inter_start_date, inter_end_date):

        if not validators.url(kpi_node_iri):
            raise Exception("Sorry, the IRI: " + kpi_node_iri + " is not a valid URL.")

        payload = json.dumps([
            {
                "_classes": [self.DTP_CONFIG.get_ontology_uri('kpiZeroDefectWork')],
                "_domain": self.DTP_CONFIG.get_kpi_domain(),
                "_iri": kpi_node_iri,
                "_visibility": 0,
                self.DTP_CONFIG.get_ontology_uri('kpiValue'): value,
                self.DTP_CONFIG.get_ontology_uri('kpiReferenceQuantity'): ref_quant,
                self.DTP_CONFIG.get_ontology_uri('kpiSampleQuantity'): sampl_quant,
                self.DTP_CONFIG.get_ontology_uri('kpiIntervalStartDate'): inter_start_date,
                self.DTP_CONFIG.get_ontology_uri('kpiIntervalEndDate'): inter_end_date,
            }
        ])

        response = self.post_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('add_node'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info("DTP_API - NEW_KPI_IRI: " + kpi_node_iri)
                return True
            else:
                logger_global.error("Creating new element failed. Response code: " + str(response.status_code))
                return False
        return True
