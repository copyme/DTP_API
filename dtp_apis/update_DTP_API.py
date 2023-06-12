#  Copyright (c) Sophia Antipolis-Méditerranée, University of Cambridge 2023.
#  Authors: Kacper Pluta <kacper.pluta@inria.fr>, Alwyn Mathew <am3156@cam.ac.uk>
#  This file cannot be used without a written permission from the author(s).

import json
import os

from helpers import logger_global


class UpdateAPI:
    """
    Mixin update API class contains update node functions.

    Methods
    -------
    update_asdesigned_param_node(node_iri, is_as_designed)
        returns bool, True if success and False otherwise
    update_operation_node(per_node_iri, list_of_action_iri, process_start, process_end, log_path)
        returns bool, True if success and False otherwise
    update_construction_node(constr_iri, list_of_operation_iri, log_path)
        returns bool, True if success and False otherwise
    """

    def update_asdesigned_param_node(self, node_iri, is_as_designed):
        """
        The method updates AsDesigned parameters in the node corresponding to given iri

        Parameters
        ----------
        node_iri: str, obligatory
            an iri of a node to be updated
        is_as_designed: bool, obligatory
            the value of AsDesigned that will be used to update the node

        Returns
        -------
        bool
            True if a blob has been node has been updated and False otherwise
        """

        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": node_iri,
            self.DTP_CONFIG.get_ontology_uri('isAsDesigned'): is_as_designed
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        f"DTP_API - UPDATE_isAsDesigned_PARAM_NODE_OPERATION: {node_iri}, {is_as_designed}")
                return True
            else:
                logger_global.error("Updating nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def update_operation_node(self, oper_node_iri, list_of_action_iri, process_start, process_end, log_path):
        """
        The method updates a new operation.

        Parameters
        ----------
        oper_node_iri : str, obligatory
            a valid IRI of a node.
        list_of_action_iri : list, optional
            list of connection actions iri.
        process_start: str, obligatory
            Start date of the action
        process_end: str, obligatory
            End date of the action
        log_path: str, obligatory
            path to node dump file

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        bool
            return True if operation node has been updated and False otherwise.
        """
        # creating backup of the node
        node_info = self.fetch_nodes_with_iri(oper_node_iri)
        dump_path = os.path.join(log_path, f"{oper_node_iri.rsplit('/')[-1]}.json")
        with open(dump_path, 'w') as fp:
            json.dump(node_info, fp)

        if list_of_action_iri:
            # collecting already existing edges
            already_existing_edges = node_info['items'][0]['_outE']
            out_edge_to_actions = [*already_existing_edges]
            # create new out edges list of dictionaries
            for action_iri in list_of_action_iri:
                out_edge_dict = {
                    "_label": self.DTP_CONFIG.get_ontology_uri('hasAction'),
                    "_targetIRI": action_iri
                }
                out_edge_to_actions.append(out_edge_dict)

            payload = json.dumps([{
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": oper_node_iri,
                self.DTP_CONFIG.get_ontology_uri('processStart'): process_start,
                self.DTP_CONFIG.get_ontology_uri('processEnd'): process_end,
                "_outE": out_edge_to_actions
            }])
        else:
            payload = json.dumps([{
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": oper_node_iri,
                self.DTP_CONFIG.get_ontology_uri('processStart'): process_start,
                self.DTP_CONFIG.get_ontology_uri('processEnd'): process_end
            }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(f"DTP_API - UPDATE_OPERATION_IRI: {oper_node_iri}, {dump_path}")
                return True
            else:
                logger_global.error("Updating operation node failed. Response code: " + str(response.status_code))
                return False
        return True

    def update_construction_node(self, constr_iri, list_of_operation_iri, log_path):
        """
        The method updates construction node.

        Parameters
        ----------
        constr_iri : str, obligatory
            a valid IRI of a node.
        list_of_operation_iri : list, optional
            list of connection operation iri.
        log_path: str, obligatory
            path to node dump file

        Raises
        ------
        It can raise an exception if the request has not been successful.

        Returns
        ------
        bool
            return True if construction node has been created and False otherwise.
        """
        # update node if operation iri list has at least one item
        if len(list_of_operation_iri):
            # creating backup of the node
            node_info = self.fetch_nodes_with_iri(constr_iri)
            dump_path = os.path.join(log_path, f"{constr_iri.rsplit('/')[-1]}.json")
            with open(dump_path, 'w') as fp:
                json.dump(node_info, fp)

            # collecting already existing edges
            already_existing_edges = node_info['items'][0]['_outE']
            out_edge_to_operation = [*already_existing_edges]
            # create new out edges list of dictionaries
            for action_iri in list_of_operation_iri:
                out_edge_dict = {
                    "_label": self.DTP_CONFIG.get_ontology_uri('hasAction'),
                    "_targetIRI": action_iri
                }
                out_edge_to_operation.append(out_edge_dict)

            payload = json.dumps([{
                "_domain": self.DTP_CONFIG.get_domain(),
                "_iri": constr_iri,
                "_outE": out_edge_to_operation
            }])

            response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
            if not self.simulation_mode:
                if response.ok:
                    if self.session_logger is not None:
                        self.session_logger.info(f"DTP_API - UPDATE_CONSTRUCTION_IRI: {constr_iri}, {dump_path}")
                    return True
                else:
                    logger_global.error("Updating operation node failed. Response code: " + str(response.status_code))
                    return False
            return True
        else:
            return True

    def delete_param_in_node(self, node_iri, field, previous_field_value=None, field_placeholder="delete",
                             is_revert_session=False):
        """
        The method removes a specific field from a node

        Parameters
        ----------
        node_iri: str, obligatory
            an iri of a node to act on
        field: str, obligatory
            an url or str of node field
        previous_field_value: str, optional
            previous field value
        field_placeholder: str, optional
            placeholder for the deleting field
        is_revert_session: bool, optional
            true if reverting from session file

        Returns
        -------
        bool
            True if a blob has been node has been updated and False otherwise
        """
        if not is_revert_session:
            assert previous_field_value, 'previous_field_value needed for logging'
        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": node_iri,
            field: field_placeholder  # 'delete' is a placeholder to ensure payload is valid
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_unset'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        f"DTP_API - REMOVED_PARAM_NODE_OPERATION: {node_iri}, {field}, {previous_field_value} ")
                return True
            else:
                logger_global.error("Updating nodes failed. Response code: " + str(response.status_code))
                return False
        return True

    def add_param_in_node(self, node_iri, field, field_value):
        """
        The method add new parameter to the node

        Parameters
        ----------
        node_iri: str, obligatory
            an iri of a node to be updated
        field: str, obligatory
            url or str of the field name
        field_value: str, obligatory
            value of the adding field

        Returns
        -------
        bool
            True if a blob has been node has been updated and False otherwise
        """

        payload = json.dumps([{
            "_domain": self.DTP_CONFIG.get_domain(),
            "_iri": node_iri,
            field: field_value
        }])

        response = self.put_guarded_request(payload=payload, url=self.DTP_CONFIG.get_api_url('update_set'))
        if not self.simulation_mode:
            if response.ok:
                if self.session_logger is not None:
                    self.session_logger.info(
                        f"DTP_API - ADD_PARAM_NODE_OPERATION: {node_iri}, {field}, {field_value}")
                return True
            else:
                logger_global.error("Updating nodes failed. Response code: " + str(response.status_code))
                return False
        return True
