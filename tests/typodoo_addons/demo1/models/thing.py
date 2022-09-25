from odoo import models, fields


class Thing(models.Model):

    _name = "thing"
    _description = "Thing"

    partner_id = fields.Many2one(comodel_name="res.partner")
    name = fields.Char(required=True)
    weight = fields.Float()
