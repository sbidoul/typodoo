from odoo import fields, models, api
from odoo.addons.base.models.res_partner import Partner

from .thing import Thing


class ResPartner(Partner, extends=True):

    thing_ids: Thing = fields.One2many(inverse_name="partner_id")
    thing_count: int = fields.Integer(compute="_compute_thing_count_and_weight")
    thing_weight: float = fields.Float(compute="_compute_thing_count_and_weight")

    @api.depends("thing_ids")
    def _compute_thing_count_and_weight(self) -> None:
        for partner in self:
            partner.thing_count = len(partner.thing_ids)
            partner.thing_weight = sum(t.weight for t in partner.thing_ids)
