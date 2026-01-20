from odoo import models, fields, api

class RoutingTestWizard(models.TransientModel):
    _name = 'routing.test.wizard'
    _description = 'Test Routing Logic'

    # The Account we are testing (passed from context)
    account_id = fields.Many2one('routing.account', string="Account", required=True)

    # --- INPUTS (The criteria you want to test) ---
    jurisdiction_id = fields.Many2one('routing.jurisdiction', string="Jurisdiction")
    entity_id = fields.Many2one('routing.entity', string="Entity")
    case_type_id = fields.Many2one('routing.case.type', string="Case Type")
    doc_type = fields.Char(string="Document Type")

    # --- RESULTS ---
    result_ids = fields.One2many('routing.test.result', 'wizard_id', string="Results")
    
    # Final Outcome Display
    final_recipient_to = fields.Char(string="Final To Recipient", readonly=True)
    final_recipient_cc = fields.Char(string="Final CC Recipient", readonly=True)
    
    # --- NEW: Final Method of Delivery ---
    final_method_of_delivery = fields.Char(string="Method of Delivery", readonly=True)

    def action_run_test(self):
        self.ensure_one()
        # 1. Clear previous results
        self.result_ids.unlink()
        
        # 2. Get all rules for this account
        rules = self.env['routing.rule'].search([('account_id', '=', self.account_id.id)])
        
        results = []
        match_found = False
        winning_rule = None

        # 3. Iterate through every rule to check for a match
        for rule in rules:
            is_match = True
            
            # If rule has no conditions, it's a fallback (or invalid), usually assume False unless logic dictates otherwise
            if not rule.condition_ids:
                is_match = False
            
            # CHECK EACH CONDITION IN THE RULE
            for condition in rule.condition_ids:
                # A. Jurisdiction Check
                if condition.parameter == 'jurisdiction':
                    if not self.jurisdiction_id or self.jurisdiction_id != condition.value_jurisdiction_id:
                        is_match = False
                        break
                
                # B. Entity Check
                elif condition.parameter == 'entity':
                    if not self.entity_id or self.entity_id != condition.value_entity_id:
                        is_match = False
                        break

                # C. Case Type Check
                elif condition.parameter == 'case_type':
                    if not self.case_type_id or self.case_type_id != condition.value_case_type_id:
                        is_match = False
                        break

                # D. Doc Type Check (Text Match)
                elif condition.parameter == 'doc_type':
                    if not self.doc_type:
                        is_match = False
                        break
                    
                    val = self.doc_type.lower()
                    cond_val = (condition.value_doc_type or '').lower()
                    
                    if condition.operator == 'matches':
                        if val != cond_val:
                            is_match = False
                            break
                    elif condition.operator == 'contains':
                        if cond_val not in val:
                            is_match = False
                            break

            # Store Result
            results.append((0, 0, {
                'rule_name': rule.name,
                'matches': is_match,
                'recipient_to': rule.recipient_to,
                'recipient_cc': rule.recipient_cc,
            }))

            # Identify the FIRST match as the winner
            if is_match and not match_found:
                match_found = True
                winning_rule = rule
                self.final_recipient_to = rule.recipient_to
                self.final_recipient_cc = rule.recipient_cc
                # Get the readable label for the method (e.g. "Email Only") instead of the key ("email")
                self.final_method_of_delivery = dict(rule._fields['method_of_delivery'].selection).get(rule.method_of_delivery)

        # 4. DEFAULT ROUTING LOGIC
        # If no rules matched, add a "Default Routing" line
        if not match_found:
            self.final_recipient_to = "Default Mailroom" 
            self.final_recipient_cc = "None"
            self.final_method_of_delivery = "Physical Mail (Default)" # Default Method

            results.append((0, 0, {
                'rule_name': 'Default Routing',
                'matches': True, # It "matches" because it's the fallback
                'recipient_to': self.final_recipient_to,
                'recipient_cc': self.final_recipient_cc,
            }))

        self.result_ids = results
        
        # Return action to keep wizard open
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'routing.test.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

class RoutingTestResult(models.TransientModel):
    _name = 'routing.test.result'
    _description = 'Test Result Line'

    wizard_id = fields.Many2one('routing.test.wizard')
    rule_name = fields.Char(string="Rule Name")
    matches = fields.Boolean(string="Matches")
    recipient_to = fields.Char(string="To Recipients")
    recipient_cc = fields.Char(string="CC Recipients")