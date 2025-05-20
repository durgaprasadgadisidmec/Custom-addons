from odoo import models,fields,api
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    period = fields.Integer(string="Warranty Period (Days)")


class WarrantyMenu(models.Model):
    _name="warranty.menu"
    _description= "Warranty Menu"

    product_name=fields.Char(string="Product",)
    quantity = fields.Integer("Quantity")
    serial_number = fields.Char(string="Serial Number",)
    wh_doucment = fields.Char(string="WH Doument",store=True)
    source_document = fields.Char(string="Source Document", )
    delivery_date = fields.Datetime(string="Delivery Date",  )
    scheduled_date = fields.Datetime(string='Scheduled Date', )
    customer_name = fields.Char(string="Customer Name", )
    phone = fields.Char(string="Customer Phone", )
    warranty_period = fields.Integer(string="Warranty Period (Days)")
    warranty_remaining = fields.Integer(string="Warranty Remaining (Days)", compute="_compute_warranty_info",store=True)
    status = fields.Selection([('valid', 'Valid'), ('expired', 'Expired')], string="Status", compute="_compute_warranty_info", store=True)
    quantity = fields.Integer("Quantity")


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


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            if picking.picking_type_code != 'outgoing':
                continue

            if not picking.origin:
                continue

            for move_line in picking.move_line_ids:
                product = move_line.product_id
                serial_number = move_line.lot_id.name if move_line.lot_id else 'No Serial'
                warranty_period = product.product_tmpl_id.period  # Correct field
                product_name = product.name
                quantity = move_line.quantity  # Add this line

                data = {
                    'product_name': product_name,
                    'serial_number': serial_number,
                    'wh_doucment': picking.name,
                    'source_document': picking.origin,
                    'delivery_date': picking.date_done,
                    'scheduled_date': picking.scheduled_date,
                    'customer_name': picking.partner_id.name,
                    'phone': picking.partner_id.phone,
                    'warranty_period': warranty_period,
                    'quantity': quantity,
                }

                self.env['warranty.menu'].create(data)

        return res


