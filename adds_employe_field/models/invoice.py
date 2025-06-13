from odoo import models,fields

class Invoice(models.Model):
    _inherit = "account.move"
    empolyee_name = fields.Many2one(comodel_name= "hr.employee",string="Employee")
