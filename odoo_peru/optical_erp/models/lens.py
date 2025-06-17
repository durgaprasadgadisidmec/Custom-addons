from odoo import models, fields,api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    material=fields.Char("Material")

    lens_types = fields.Char("Lens Type")
    lens_style = fields.Char("Lens Style")
    product_category = fields.Selection([
        ("frames", "Frames"),
        ("lens", "Lens"),
        ("contact_lens", "Contact Lens"),
        ("lens_treatment", "Lens Treatment"),
        ("service", "Service"),
        ("miscellaneous", "Miscellaneous"),

    ], string="Product Category", )
