from odoo import models, fields
class RoutingEntity(models.Model):
    _name = 'routing.entity'
    _description = 'Legal Entity'
    _rec_name = 'name'
    name = fields.Char(string="Entity Name", required=True)