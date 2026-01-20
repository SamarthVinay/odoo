from odoo import models, fields

class RoutingCaseType(models.Model):
    _name = 'routing.case.type'
    _description = 'Case Type'
    _rec_name = 'name'

    name = fields.Char(string="Case Type", required=True)

    # --- PREVENT DUPLICATES ---
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'A Case Type with this name already exists!'),
    ]