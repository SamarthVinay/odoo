# Import Odoo's base model class and field definitions
from odoo import models, fields


# Define a new Odoo model for Routing Accounts
class RoutingAccount(models.Model):

    # Technical name used internally by Odoo and for database table creation
    _name = 'routing.account'

    # Human-readable description of this model
    _description = 'Routing Account'

    # Field that will be shown as the record name in dropdowns and headers
    _rec_name = 'account_name'

    # Stores the name of the routing account (shown to users)
    account_name = fields.Char(required=True)

    # Stores a reference or account number for identification
    account_number = fields.Char(required=True)

    # Stores how many entities are linked to this account
    entities_count = fields.Integer(string="Entities")


    # One routing account can have many routing conditions
    # This links routing.account → routing.condition using account_id
    condition_ids = fields.One2many(
        'routing.condition',   # Model that holds the conditions
        'account_id',          # Field in routing.condition that links back here
        string="Conditions"    # Label shown in the UI
    )


    # Displays how many routing rules are active for this account
    # Value is calculated dynamically using a function
    rules_active_count = fields.Integer(
        compute='_compute_rules_count',
        string="Rules Active"
    )


    # Function that calculates how many rules are linked to each account
    def _compute_rules_count(self):

        # Loop through each routing account record
        for record in self:

            # Count how many conditions are linked to this account
            record.rules_active_count = len(record.condition_ids)


    # Function called when user clicks the "Rules" button
    def action_view_rules(self):

        # Ensure the action is performed on only one account at a time
        self.ensure_one()

        # Return an action that opens a new window
        return {
            # Title of the window shown to the user
            'name': 'Routing Rules',

            # Tells Odoo to open a list/form window
            'type': 'ir.actions.act_window',

            # Model whose records should be displayed
            'res_model': 'routing.rule',

            # Allows switching between list view and form view
            'view_mode': 'list,form',

            # Show only rules that belong to this routing account
            'domain': [('account_id', '=', self.id)],

            # Automatically set account_id when creating a new rule
            'context': {'default_account_id': self.id},
        }
