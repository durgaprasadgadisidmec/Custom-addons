from odoo import api, fields, models, _
from datetime import datetime

class CompletePair(models.Model):
    _name ='complete.pair'

    prescription_id = fields.Many2one('dr.prescription')
    frame_types = fields.Many2one('product.template',string='Frames',readonly=False)
    lens_types = fields.Many2one("product.template","Lens")

    def add_to_order(self):
        return {'type': 'ir.actions.act_window_close'}

    def cancel(self):
        print()