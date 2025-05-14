from odoo import models,fields,api
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    period = fields.Integer(string="Warranty Period (Days)")

class WarrantyMenu(models.Model):
    _name="warranty.menu"
    _description= "Warranty Menu"

    warranty_line_ids = fields.One2many('warranty.line','warranty_id',string="Warranty Lines")

    product_name=fields.Char(string="Product",)
    serial_number = fields.Char(string="Serical Number",)
    wh_doucment = fields.Char(string="WH Doument",store=True)
    source_document = fields.Char(string="Source Document", )
    delivery_date = fields.Datetime(string="Delivery Date",  )
    scheduled_date = fields.Datetime(string='Scheduled Date', )
    customer_name = fields.Char(string="Customer Name", )
    phone = fields.Char(string="Customer Phone", )
    warranty_period = fields.Integer(string="Warranty Period (Days)")
    warranty_remaining = fields.Integer(string="Warranty Remaining (Days)", compute="_compute_warranty_info",store=True)
    status = fields.Selection([('valid', 'Valid'), ('expired', 'Expired')], string="Status", compute="_compute_warranty_info", store=True)


    @api.depends('warranty_period', 'scheduled_date')
    def _compute_warranty_info(self):
        for record in self:
            if record.scheduled_date and record.warranty_period:
                days_passed = (datetime.now() - record.scheduled_date).days
                remaining = record.warranty_period - days_passed
                record.warranty_remaining = max(0, remaining)
                record.status = 'valid' if remaining > 0 else 'expired'
            else:
                record.warranty_remaining = 0
                record.status = 'expired'


class WarrantyLine(models.Model):
    _name = "warranty.line"
    _description = "Warranty Line"

    product_name = fields.Char(string="Product")
    quantity = fields.Integer("Quantity")
    serial_number = fields.Char(string="Serical Number")
    # wh_doucment = fields.Char(string="WH Document")
    # source_document = fields.Char(string="Source Document")
    # delivery_date = fields.Datetime(string="Delivery Date")
    # customer_name = fields.Char(string="Customer Name")
    # phone = fields.Char(string="Customer Phone")
    # warranty_period = fields.Integer(string="Warranty Period (Days)")
    # warranty_remaining = fields.Integer(string="Warranty Remaining (Days)")
    # status = fields.Char(string="Status")

    warranty_id = fields.Many2one("warranty.menu", string="Warranty Reference", ondelete="cascade")
