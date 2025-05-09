from odoo import models, fields, api
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    customers_name = fields.Char(string="Customer Name", compute="_compute_customer_info", store=True)
    phone = fields.Char(string="Phone", compute="_compute_customer_info", store=True)
    delivery_date = fields.Datetime(string="Delivery Date")



    @api.depends('partner_id')
    def _compute_customer_info(self):
        for record in self:
            if record.partner_id:
                record.customers_name = record.partner_id.name
                record.phone = record.partner_id.mobile
            else:
                record.customers_name = False
                record.phone = False


class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    serial_number = fields.Many2many('stock.lot','move_lot_rel',  'move_id','lot_id', string='Serial Number',domain="[('product_id', '=', product_id)]")
    wh_doucment=fields.Char(string="WH Doument",related="picking_id.name")
    source_document = fields.Char(string="Source Document", related="picking_id.origin",)
    delivery_date = fields.Datetime(string="Delivery Date",related="picking_id.delivery_date",)
    scheduled_date = fields.Datetime( string='Scheduled Date',related='picking_id.scheduled_date',store=True)
    customer_name = fields.Char(string="Customer Name",related="partner_id.name")
    phone = fields.Char(string="Customer Phone",related="picking_id.phone")
    warranty_period =fields.Integer(string="Warranty Period",related='product_id.product_tmpl_id.period',)
    warranty_remaining=fields.Integer(string="Warranty Remaining",compute="_compute_warranty_info")
    status = fields.Selection([
        ('valid' ,'Valid'),
        ('expired', 'Expired')
    ] ,string="Status" , )

    @api.depends('warranty_period', 'scheduled_date')
    def _compute_warranty_info(self):
        for record in self:
            if record.scheduled_date:
                days_passed = (datetime.now() - record.scheduled_date).days
                remaining = record.warranty_period - days_passed
                record.warranty_remaining = max(0, remaining)
                record.status = 'valid' if remaining > 0 else 'expired'
            else:
                record.warranty_remaining = 0
                record.status = 'expired'