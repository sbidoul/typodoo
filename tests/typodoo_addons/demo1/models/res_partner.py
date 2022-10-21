from odoo import fields, api
from odoo.addons.base.models.res_partner import Partner

from .thing import Thing


class ResPartner(Partner):

    thing_ids = fields.One2many[Thing](inverse_name="partner_id")
    thing_count = fields.Integer(compute="_compute_thing_count_and_weight")
    thing_weight = fields.Float(compute="_compute_thing_count_and_weight")

    @api.depends("thing_ids")
    def _compute_thing_count_and_weight(self) -> None:
        for partner in self:
            partner.thing_count = len(partner.thing_ids)
            partner.thing_weight = sum(t.weight for t in partner.thing_ids)
