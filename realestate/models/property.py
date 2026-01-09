from odoo import fields,models

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="date available")
    bedrooms = fields.Integer(string="bedrooms")
    garden = fields.Boolean(string="garden" , default=False)
    garden_orientation = fields.Selection(
        [('north','North'),('south','south'),('east','east'),('west','west')],
        string="garden_orientation",default='north')
    
    
    #id ,create date, create uid,write date and write uid are automatically loaded
    