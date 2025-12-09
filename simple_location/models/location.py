from odoo import api, fields, models

class LocationCountry(models.Model):
    _name = "location.country"
    _description = "Country"
    name = fields.Char(string="Country Name", required=True)

class LocationState(models.Model):
    _name = "location.state"
    _description = "State"
    name = fields.Char(string="State Name", required=True)
    country_id = fields.Many2one("location.country", string="Country")

class LocationCity(models.Model):
    _name = "location.city"
    _description = "City"
    name = fields.Char(string="City Name", required=True)
    state_id = fields.Many2one("location.state", string="State")
    country_id = fields.Many2one("location.country", string="Country", related="state_id.country_id", store=True)

class LocationSelector(models.Model):
    _name = "location.selector"
    _description = "Simple selector (Country->State->City)"
    name = fields.Char(string="Reference")
    country_id = fields.Many2one("location.country", string="Country")
    state_id = fields.Many2one("location.state", string="State")
    city_id = fields.Many2one("location.city", string="City")

    @api.onchange('country_id')
    def _onchange_country(self):
        if self.country_id:
            return {
                'domain': {
                    'state_id': [('country_id', '=', self.country_id.id)],
                    'city_id': [('country_id', '=', self.country_id.id)]
                },
                'value': {'state_id': False, 'city_id': False}
            }
        return {'domain': {'state_id': [], 'city_id': []}, 'value': {'state_id': False, 'city_id': False}}

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id:
            return {'domain': {'city_id': [('state_id', '=', self.state_id.id)]}, 'value': {'city_id': False}}
        return {'domain': {'city_id': []}, 'value': {'city_id': False}}
