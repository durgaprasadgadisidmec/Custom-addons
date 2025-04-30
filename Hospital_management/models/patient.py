# patient.py
# from addons.spreadsheet.utils.validate_data import fields_in_spreadsheet
from odoo import models, fields, api
from datetime import date, datetime
import base64
from odoo.api import ValuesType, Self
from odoo.osv import expression


from odoo.api import ValuesType, Self
from odoo.osv import expression


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _rec_name = "patient_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # patient_code = fields.Char(string='Patient Code', readonly=True, copy=False)
    patient_name = fields.Many2one("res.partner", string="Name", tracking=True, required=True)
    email = fields.Char("Email")  # This is the change
    mobile = fields.Char("Mobile")
    date_of_birth=fields.Date(string="Date of Birth", tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age_from_dob" , store=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender")

    is_patient_in_ward = fields.Boolean("Is Patient in ward")
    admit_date = fields.Date("Admit Date")
    discharge_date = fields.Date("Discharge Date")

    doctor_id = fields.Many2one(domain=[("email", "!=", False)], comodel_name="hospital.doctor", string="Doctor_id")
    d_email = fields.Char(related="doctor_id.email", string="Doctor_Email")

    patient_names = fields.Many2many(comodel_name="res.partner", string="Contacts")

    patient_lines = fields.One2many("hospital.patient.line", "patient", "order lines")

    user_id = fields.Many2one("res.users", "user", compute="compute_user_company")
    company_id = fields.Many2one("res.company", "company", compute="compute_user_company")
    status = fields.Selection([("admit", "Admitted"), ("discharge", "Discharged")], "status", default="admit")
    image = fields.Binary(string="Patient Image")

#For auto update the age based on the Date of Birth
    @api.depends('date_of_birth')
    def _compute_age_from_dob(self):
        for record in self:
            if record.date_of_birth:
                # Calculate the age
                today = datetime.today()
                #print(">>>>>>>>",today)
                dob = fields.Date.from_string(record.date_of_birth)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                record.age = age
                #print(">>>>>>>>>>.",record.age)
            else:
                record.age = 0

    @api.onchange('patient_name')
    def _onchange_patient_name(self):
        if self.patient_name:
            self.email = self.patient_name.email
            self.mobile = self.patient_name.mobile
        else:
            self.email = False
            self.mobile = False

    # @api.onchange("patient_name")
    # def onchange_patient_name(self):
    #      for rec in self:
    #          print(rec)
    #          rec.email = rec.patient_name.email
    #
    # def compute_patient_email(self):
    #     for rec in self:
    #         rec.email = rec.patient_name.email

    @api.onchange('discharge_date')
    def compute_state(self):
        today = date.today()
        for rec in self:
            if rec.discharge_date:
                if today < rec.discharge_date:
                    rec.status = "admit"
                else:
                    rec.status = "discharge"
            else:
                rec.status = "admit"
    # @api.model
    # def create(self, vals):
    #     vals[' patient_code']= self.env['ir.sequence'].next_by_code('res.partner')
    #     return super(HospitalPatient , self).create(vals)

    def compute_user_company(self):
        for rec in self:
            rec.user_id = self.env.user
            rec.company_id = self.env.user.company_id.id

    def send_email(self):
        for rec in self:
            template = self.env.ref("Hospital_management.mail_template_patient_confirm")
            template.send_mail(rec.id, force_send=True)

    def view_patient_lines(self):
        self.ensure_one()
        return {
            'name': "view patient invoices",
            'view_mode': 'list',
            'res_model': 'hospital.patient.line',
            'domain': [('patient', '=', self.id)],
            'type': 'ir.actions.act_window',

        }

        # # To genetare the Uniue code for the customer
        # def _generate_patient_code(self):
        #     year = datetime.now().year
        #     seq_code = f'patient.code.{year}'
        #
        #     seq = self.env['ir.sequence'].sudo().search([('code', '=', seq_code)], limit=1)
        #     if not seq:
        #         seq = self.env['ir.sequence'].sudo().create({
        #             'name': f'Patient Code {year}',
        #             'code': seq_code,
        #             'prefix': f'PAT/{year}/',
        #             'padding': 4,
        #             'number_next': 1,
        #             'number_increment': 1,
        #             'implementation': 'no_gap',
        #         })
        #     return self.env['ir.sequence'].next_by_code(seq_code)

    # @api.model
    # def name_search(self, name, args=None, operator='ilike', limit=100):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', '|',
    #                   ('email', operator, name),
    #                   ('mobile', operator, name)]
    #         # ('patient_name', operator, name.id)
    #
    #     return self.search(domain + args, limit=limit).name_get()
    #     # return super(HospitalPatient, self).name_search(name, args=args, operator=operator, limit=limit)

    class ResPartner(models.Model):
        _inherit = 'res.partner'

        @api.model
        def name_search(self, name='', args=None, operator='ilike', limit=100):
            args = []
            domain = []
            if name:
                domain = expression.OR([
                    [('name', operator, name)],
                    [('phone', operator, name)],
                    # [('email ', operator, name)],
                    [('gst_number', operator, name)],
                ])
            records = self.search(expression.AND([args, domain]), limit=limit)
            return [(rec.id, f"{rec.name}") for rec in self.browse(records.ids)]

            def create(self, vals):
                vals["pseq"] = self.env['ir.sequence'].next_by_code('hospital.patient')
                if 'patient_code' not in vals:
                    vals['patient_code'] = self._generate_patient_code()
                return super(HospitalPatient, self).create(vals)



class HospitalPatientLines(models.Model):
    _name = "hospital.patient.line"

    product_id = fields.Many2one("product.product", "product Name")
    qty = fields.Integer("qty")
    unit_price = fields.Float("Unit Price", compute="compute_line")
    patient = fields.Many2one("hospital.patient", "patient")
    sub_total = fields.Float(string="SubTotal", compute="subtotal")

    def compute_line(self):
        for i in self:
            i.unit_price = i.product_id.list_price

    def subtotal(self):
        for i in self:
            i.sub_total = i.unit_price * i.qty


class PatientAccounting(models.Model):
    _inherit = 'account.move'
