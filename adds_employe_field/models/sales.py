from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = "sale.order"
    empolyee_name = fields.Many2one(comodel_name= "hr.employee",string="Employee")
