from odoo import models, fields
class RoutingJurisdiction(models.Model):
    _name = 'routing.jurisdiction'
    _description = 'Jurisdiction'
    _rec_name = 'name'
    name = fields.Char(string="State/Region", required=True)