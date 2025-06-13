from odoo import models,fields


class Crm(models.Model):
    _inherit = "crm.lead"

    empolyee_name = fields.Many2one(comodel_name="hr.employee", string="Employee")