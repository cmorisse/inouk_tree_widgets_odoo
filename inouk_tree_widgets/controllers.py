# -*- coding: utf-8 -*-
from openerp import http
from openerp.tools.translate import _
import logging

_logger = logging.getLogger('InoukTree')

class InoukTree(http.Controller):
    @http.route('/inouk-tree/ping', type='json', auth='none')
    def pong(self, **kw):
        return "JSON pong from InoukTree controller"


    def fetch_fancytree_nodes(self, model_name, search_domain, children_field_name, order_by):
        """

        :param model_name:
        :type model_name:
        :param search_domain:
        :type search_domain:
        :param children_field_name: x
        :type children_field_name:
        :param order_by:
        :type order_by:
        :return:
        :rtype:
        """
        tree_obj = http.request.env[model_name]
        node_list = tree_obj.search(search_domain, order=order_by)
        result = [
            {
                'key': n.id,
                'title': n.name,
                'folder': len(n.sub_deliverable_ids) > 0,
                'lazy': len(n.sub_deliverable_ids) > 0  # CMo: thinking about to optimize this
            } for n in node_list
        ]
        return result


    def fancytree_encoded_node_list(self, node_list, expand_nodes):
        """
        Recursively traverses the tree branch by branch.

        :param node_list: one level of the tree to process
        :type node_list: list
        :param expand_nodes: Should returned nodes be flagged as expanded
        :type expand_nodes: bool
        :return: encoded sub tree
        :rtype: list
        """
        result_list = []
        for node in node_list:
            has_children = len(node.sub_deliverable_ids) > 0  # TODO: use children field name
            node_dict = {
                'key': node.id,
                'title': node.name,  # TODO: use title field name
                'folder': has_children,
            }
            if has_children:
                node_dict['children'] = self.fancytree_encoded_node_list(node.sub_deliverable_ids, expand_nodes)
                if expand_nodes:
                    node_dict['expanded'] = True
            result_list.append(node_dict)
        return result_list

    def fetch_full_tree(self, model_name, search_domain, parent_field_name, order_by, expand_nodes=False):
        """
        Return a complete tree ; no node flagged lazy and all children nodes included

        :param model_name:
        :type model_name:
        :param search_domain: a domain to select all nodes of returned tree
        :type search_domain: list
        :param children_field_name: name of the field used to identify sub nodes
        :type children_field_name: str
        :param order_by:
        :type order_by:
        :return:
        :rtype:
        """
        tree_obj = http.request.env[model_name]

        node_search_domain = [(parent_field_name, '=', None)] if not search_domain else search_domain
        root_node_list = tree_obj.search(node_search_domain, order=order_by)
        full_tree_node_list = self.fancytree_encoded_node_list(root_node_list, expand_nodes)
        _logger.debug("Full tree = %s", full_tree_node_list)
        return full_tree_node_list


    @http.route('/inouk-tree/tree', type='json', auth='user')
    def get_tree(self, request,
                 search_mode='client', parent_field_name='parent_id', parent_id=None, model_name=None,
                 title_field_name='name', children_field_name=None, order_by=None, domain=None, expand_nodes=False, **kw):
        """

        :param request:
        :type request:
        :param search_mode: Defines whether search is done on the server or on the client (default).
        If tree has a lot of node, you must switch to server search mode.
        :type search_mode: str
        :param parent_field_name:
        :type parent_field_name: str
        :param parent_id:  id if the parent node that must be returned.
        :type parent_id: int
        :param model_name: Required name of the Odoo model that contains the tree.
        :type model_name: str
        :param title_field_name: Name of the field to use to generate tree labels
        :type title_field_name: str
        :param order_by: order by clause passed as value to search() order parameter
        :type order_by: str
        :param domain: a search domain appended to the search clause
        :type domain: str
        :return: an object that will be Json encoded

        Expected returned structure example:
        [
            {
                "title": "Node 1",
                "key": "1"
            },
            {
                "title": "Folder 2",
                "key": "2",
                "folder": True,

                    'lazy': True
                OR  "children": [
                    {
                        "title": "Node 2.1",
                        "key": "3"
                    },
                    {
                        "title": "Node 2.2",
                        "key": "4"
                    }
                ]
            }
        ]
        """
        # TODO: Shall we include asked id returned response
        assert model_name, _("Missing required 'model_name' attribute for widget 'InoukTree2One'")
        assert children_field_name, _("Missing required 'children_field_name' attribute for widget 'InoukTree2One'")
        expand_nodes = eval(expand_nodes) if expand_nodes else False

        _logger.debug("Inouk::get_tree() params=%s", request.params)

        if search_mode =='server':
            return self.fetch_full_tree(model_name, domain, parent_field_name, order_by, expand_nodes=expand_nodes)

        parent_id = int(parent_id) if parent_id else None
        node_search_domain = [(parent_field_name, '=', parent_id)] if not domain else domain
        return self.fetch_fancytree_nodes(model_name, node_search_domain, children_field_name, order_by)



    @http.route('/inouk-tree/nodes', type='json', auth='user')
    def fetch_nodes(self, request,
                    search_mode='client', parent_field_name='parent_id', parent_id=None, model_name=None,
                    title_field_name='name', children_field_name=None, order_by=None, **kw):
        """

        :param request:
        :type request:
        :param search_mode: Defines whether search is done on the server or on the client (default).
        If tree has a lot of node, you must switch to server search mode.
        :type search_mode: str
        :param parent_field_name:
        :type parent_field_name: str
        :param parent_id:  id if the parent node that must be returned.
        :type parent_id: int
        :param model_name: Required name of the Odoo model that contains the tree.
        :type model_name: str
        :param title_field_name: Name of the field to use to generate tree labels
        :type title_field_name: str
        :param order_by: order by clause passed as value to search() order parameter
        :type order_by: str
        :param domain: a search domain appended to the search clause
        :type domain: str
        :return: an object that will be Json encoded

        Expected returned structure example:
        [
            {
                "title": "Node 1",
                "key": "1"
            },
            {
                "title": "Folder 2",
                "key": "2",
                "folder": True,

                    'lazy': True
                OR  "children": [
                    {
                        "title": "Node 2.1",
                        "key": "3"
                    },
                    {
                        "title": "Node 2.2",
                        "key": "4"
                    }
                ]
            }
        ]
        """
        #TODO: document returned data structure

        assert model_name, _("Missing required 'model_name' attribute for widget 'InoukTree2One'")
        assert children_field_name, _("Missing required 'children_field_name' attribute for widget 'InoukTree2one'")

        _logger.debug("Inouk::fetch_nodes() params=%s", request.params)

        parent_id = int(parent_id) if parent_id else None

        # search all model_name nodes using parent_field_name and parent_id
        node_search_domain = [
            (parent_field_name, '=', parent_id),
        ]

        return self.fetch_fancytree_nodes(model_name, node_search_domain, children_field_name, order_by)



