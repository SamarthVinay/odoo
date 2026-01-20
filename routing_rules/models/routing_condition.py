from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoutingCondition(models.Model):
    _name = 'routing.condition'
    _description = 'Routing Logic Condition'
    _inherit = ['mail.thread']

    name = fields.Char(string="Condition Name", required=True)
    account_id = fields.Many2one('routing.account', string="Account")

    parameter = fields.Selection([
        ('entity', 'Entity'),
        ('jurisdiction', 'Jurisdiction'),
        ('case_type', 'Case Type'),
        ('doc_type', 'Document Type'),
    ], string="Parameter", required=True, default='jurisdiction')

    operator = fields.Selection([
        ('matches', 'Matches'),
        ('contains', 'Contains'),
    ], string="Operator", default='matches')

    value_entity_id = fields.Many2one('routing.entity', string="Entity Name")
    value_doc_type = fields.Char(string="Document Type Value")
    value_jurisdiction_id = fields.Many2one('routing.jurisdiction', string="Jurisdiction Value")
    value_case_type_id = fields.Many2one('routing.case.type', string="Case Type Value")

    create_uid = fields.Many2one('res.users', string="Creator", readonly=True)
    create_date = fields.Datetime(string="Date Created", readonly=True)

    # --- NEW: Python Constraint for Uniqueness (Replaces SQL Constraint) ---
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            # Search for other records with the same name (case-insensitive)
            # AND exclude the current record ID (so it doesn't find itself)
            domain = [
                ('name', '=ilike', record.name), 
                ('id', '!=', record.id)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(f"A Condition with the name '{record.name}' already exists! Please choose a unique name.")