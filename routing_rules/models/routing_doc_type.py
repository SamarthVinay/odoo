from odoo import models, fields
class RoutingDocType(models.Model):
    _name = 'routing.doc.type'
    _description = 'Document Type'
    _rec_name = 'name'
    name = fields.Char(string="Document Type", required=True)