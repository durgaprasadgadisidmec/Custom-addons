# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class InheritedSaleOrder(models.Model):
    _inherit = 'sale.order'

    prescription_id = fields.Many2one('dr.prescription')
    doctor = fields.Char(related='prescription_id.dr.name')
    prescription_date = fields.Date(related='prescription_id.checkup_date')

    @api.onchange('prescription_id')
    def test(self):
        product = self.env.ref('optical_erp.optical_erp_product')
        self.order_line = None
        if self.prescription_id.eye_examination_chargeable == True:
            self.order_line |= self.order_line.new({
                'name': '',
                'product_id': product.id,
                'product_uom_qty': 1,
                'qty_delivered': 1,
                'product_uom': '',
                'price_unit': '',

            })

    def complete_pair(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Complete Pair',
            'res_model': 'complete.pair',
            'view_mode': 'form',
            'target': 'new',

        }

    def lens_only(self):
        print()

    def frame_only(self):
        print()

    def contact_lens(self):
        print()

    def service(self):
        print()
