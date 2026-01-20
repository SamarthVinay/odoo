from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoutingRule(models.Model):
    _name = 'routing.rule'
    _description = 'Routing Logic Rule'
    _inherit = ['mail.thread']

    name = fields.Char(string="Rule Name", required=True)
    account_id = fields.Many2one('routing.account', string="Account", required=True)

    method_of_delivery = fields.Selection([
        ('pdf', 'PDF Only'),
        ('email', 'Email Only'),
        ('email_pdf', 'Email Only with PDF Link'),
        ('physical', 'Physical Mail')
    ], string="Method of Delivery", required=True, default='email_pdf')

    condition_ids = fields.Many2many(
        'routing.condition',
        string="Rule Conditions"
    )

    recipient_to = fields.Char(string="To Recipients")
    recipient_cc = fields.Char(string="CC Recipients")

    title = fields.Char(string="Title")
    company_name = fields.Char(string="Company Name")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    
    street = fields.Char(string="Address 1")
    street2 = fields.Char(string="Address 2")
    
    city = fields.Char(string="City")
    zip_code = fields.Char(string="Zip")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")

    # --- VALIDATION CONSTRAINT ---
    @api.constrains('name', 'condition_ids', 'recipient_to', 'recipient_cc', 'method_of_delivery', 'street', 'city', 'state_id', 'country_id', 'zip_code')
    def _check_mandatory_fields(self):
        for record in self:
            # 1. NEW: Check Unique Name
            domain = [('name', '=ilike', record.name), ('id', '!=', record.id)]
            if self.search_count(domain) > 0:
                raise ValidationError(f"A Rule with the name '{record.name}' already exists! Please choose a unique name.")

            # 2. Check Conditions
            if not record.condition_ids:
                raise ValidationError("You must select at least one Condition to create a Rule.")
            
            # 3. Check To Recipient (Always Mandatory)
            if not record.recipient_to:
                raise ValidationError("You must enter a 'To Recipient' in the Recipient Details.")

            # 4. Check Physical Mail Address Requirements
            if record.method_of_delivery == 'physical':
                if not (record.street and record.city and record.state_id and record.country_id and record.zip_code):
                    raise ValidationError("For 'Physical Mail', you must provide a full Address (Address 1, City, State, Country, Zip).")

            # 5. Validate 'To' Email (Pure Python)
            if record.recipient_to:
                email_to = record.recipient_to.strip().lower()
                if "@" not in email_to:
                     raise ValidationError(f"Invalid 'To Recipient': {record.recipient_to}. It is missing the '@' symbol.")
                if not (email_to.endswith('.com') or email_to.endswith('.in')):
                    raise ValidationError(f"Invalid 'To Recipient': {record.recipient_to}. It must end with '.com' or '.in'")

            # 6. Validate 'CC' Email (Pure Python) - Only if typed
            if record.recipient_cc:
                email_cc = record.recipient_cc.strip().lower()
                if "@" not in email_cc:
                     raise ValidationError(f"Invalid 'CC Recipient': {record.recipient_cc}. It is missing the '@' symbol.")
                if not (email_cc.endswith('.com') or email_cc.endswith('.in')):
                    raise ValidationError(f"Invalid 'CC Recipient': {record.recipient_cc}. It must end with '.com' or '.in'")