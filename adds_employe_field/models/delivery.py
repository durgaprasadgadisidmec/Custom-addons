from odoo import models,fields

class Delivery(models.Model):
    _inherit = "stock.picking"

    empolyee_name = fields.Many2one(comodel_name= "hr.employee",string="Employee")