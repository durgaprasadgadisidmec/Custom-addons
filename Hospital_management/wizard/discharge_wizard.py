from odoo import models, fields, api
from odoo.exceptions import UserError


class PatientDischargeWizard(models.TransientModel):
    _name = 'patient.discharge.wizard'
    _description = 'Wizard to discharge multiple patients'

    patient_ids = fields.Many2one('res.partner', string='Patients')

    def action_discharge_patients(self):
        for rec in self:
            if rec.patient_ids:
                patient = self.env["hospital.patient"].search([('patient_name', '=', rec.patient_ids.id)])
                for i in patient:
                    i.status='discharge'