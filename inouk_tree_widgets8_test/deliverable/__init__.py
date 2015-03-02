# coding: utf-8
from openerp import models, fields, api
from openerp.tools.translate import _


class TreeDeliverable(models.Model):
    _name = 'ikt.deliverable'
    _description = "Inouk Tree Demo Deliverable"
    _parent_store = True
    _parent_name = 'parent_id'
    _parent_order = 'sequence, name'

    #
    # Fields definition
    #
    name = fields.Char(_("Name"), required=True)
    parent_id = fields.Many2one('ikt.deliverable', _("Parent"), index=True, required=False, ondelete='cascade')
    sub_deliverable_ids = fields.One2many('ikt.deliverable', 'parent_id', _("Sub Deliverables"), required=False)

    parent_left = fields.Integer("Left parent", index=True)
    parent_right = fields.Integer("Right parent", index=True)

    sequence = fields.Integer(_("Sequence"), help=_("Defines priority of sub deliverables"))
    alt_sequence = fields.Integer(_("Alternate sequence"), help=_("Defines alternate priority of sub deliverables"))

    dummy_text = fields.Char()
    responsible_id = fields.Many2one('res.users', _("Responsible"))
