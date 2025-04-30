from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gst_number = fields.Char(string="GST Number")
    auto_email = fields.Char(string="Dummy Email", compute="_compute_auto_email", store=True)
    mobile_number=fields.Char(string="Mobile Number")


#For GST number Conditions
    @api.constrains('gst_number')
    def _check_gst_number(self):
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        for rec in self:
            if rec.gst_number:
                if len(rec.gst_number) != 15 or not re.match(pattern, rec.gst_number):
                    raise ValidationError("Invalid GST Number! Try again")
#For Autoo fill Duplicate Email id
    @api.depends('name')
    def _compute_auto_email(self):
        for rec in self:
            if rec.name:
                email_name = rec.name.lower().replace(' ', '')
                rec.auto_email = f"{email_name}@example.com"
            else:
                rec.auto_email = False

#For Warning to Change the Country name
    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.state_id:
            self.state_id = False
            return {
                'warning': {
                    'message': "State has been cleared because the country has changed.",
                }
            }
#For Mobile contain only Digits
    @api.constrains('mobile_number')
    def _check_mobile_number(self):
        for rec in self:
            if rec.mobile_number:
                if not rec.mobile_number.isdigit() or len(rec.mobile_number) != 10:
                    raise ValidationError("The mobile number should only contain 10 digits.")


