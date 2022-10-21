from odoo import models, fields

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .res_partner import Partner as ResPartner

class Thing(models.Model):

    _name = "thing"
    _description = "Thing"

    # On a relational field if we use a ForwadRef to avoid circular import
    # the comodel_name is deduced from the convertion of the classname from
    # CamelCase to dot.case
    partner_id = fields.Many2one["ResPartner"]()
    name = fields.Char(required=True)
    weight = fields.Float()
