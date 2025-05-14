from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warranty_available = fields.Boolean(string="Warranty Available")
    warranty_period=fields.Integer(string=" Period(Days)")
