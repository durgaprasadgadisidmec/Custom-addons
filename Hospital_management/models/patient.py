# patient.py
from odoo import models, fields ,api

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _rec_name = "patient_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']



    doctor_id= fields.Many2one(domain= [("email","!=",False)],comodel_name="hospital.doctor", string="Doctor_id")
    patient_name = fields.Many2one("res.partner",string="Name", tracking=True,required=True)
    email=fields.Char("Email")#This is the change
    d_email = fields.Char(related="doctor_id.email", string="Doctor_Email")
    age = fields.Integer(string="Age")
    gender=fields.Selection([("male","Male"),  ("female","Female"),  ("others","Others")], string="Gender")
    is_patient_in_ward=fields.Boolean("Is Patient in ward")
    admit_date=fields.Date("Admit Date")
    discharge_date=fields.Date("Discharge Date")

    patient_names = fields.Many2many(comodel_name="res.partner", string="Contacts")

    patient_lines= fields.One2many("hospital.patient.line" , "patient", "order lines")

    user_id=fields.Many2one("res.users","user" ,compute="compute_user_company")
    company_id=fields.Many2one("res.company","company",compute="compute_user_company")

    # @api.onchange("patient_name")
    # def onchange_patient_name(self):
    #      for rec in self:
    #          print(rec)
    #          rec.email = rec.patient_name.email
    #
    # def compute_patient_email(self):
    #     for rec in self:
    #         rec.email = rec.patient_name.email



    def compute_user_company(self):
        for rec in self:
            rec.user_id = self.env.user
            rec.company_id=self.env.user.company_id.id




class HospitalPatientLines(models.Model):
    _name="hospital.patient.line"

    product_id=fields.Many2one("product.product","product Name")
    qty  = fields.Integer("qty")
    unit_price=fields.Float("Unit Price",compute="compute_line")
    patient=fields.Many2one("hospital.patient","patient")
    sub_total=fields.Float(strin="SubTotal",compute="subtotal")

    def compute_line(self):
        for i in self:
            i.unit_price=i.product_id.list_price

    def subtotal(self):
        for i in self:
            i.sub_total=i.unit_price * i.qty


