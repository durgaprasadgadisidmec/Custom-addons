from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_name =fields.Char(string="Contacts")

    customer_names= fields.Many2many(comodel_name="res.partner", string="Contacts")