from odoo import models,fields


class HospitalDoctor(models.Model):
    _name="hospital.doctor"
    _description= "Hospital Doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char(string="Name",required=True,tracking=True)
    experience= fields.Integer(string="Experience")
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender")
    patients=fields.Many2many(comodel_name='hospital.patient',string="Patients")
    email=fields.Char(string="Doctor_Email")
