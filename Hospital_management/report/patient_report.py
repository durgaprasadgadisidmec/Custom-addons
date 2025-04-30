from odoo import models


class PatientReportXlsx(models.AbstractModel):
    _name = 'report.hospital_management.report_patient_excel'
    _inherit = 'report.report_xlsx.abstract'
    # _description = "Patient Excel Report"

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet("Patients")

        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': 'black',
            'font_size': 14,
            'font_name': 'Arial',
            'align': 'center',
        })

        cell_format = workbook.add_format({
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
        })

        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy',
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
        })

        # Set column widths
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 8)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:G', 25)

        # Headers
        # sheet.write('A1','Patient Name', style="'bold': True,'font_color': 'white','bg_color': '#4F81BD','font_size': 14,'font_name': 'Arial','align': 'center','valign': 'vcenter'")
        sheet.write('A1','Patient Name',header_format)
        sheet.write('B1','Gender', header_format)
        sheet.write('C1', 'Age', header_format)
        sheet.write('D1', 'Email', header_format)
        sheet.write('E1', 'Doctor', header_format)
        sheet.write('F1', 'Admit Date', header_format)
        sheet.write('G1', 'Discharge Date', header_format)

        row = 1
        for patient in wizard:
            sheet.write(row, 0, patient.patient_name.name, cell_format)
            sheet.write(row, 1, patient.gender or '', cell_format)
            sheet.write(row, 2, patient.age or '', cell_format)
            sheet.write(row, 3, patient.email or '', cell_format)
            sheet.write(row, 4, ', '.join(patient.doctor_id.mapped('name')) or '',cell_format)
            sheet.write(row, 5, patient.admit_date or '',date_format )
            sheet.write(row, 6, patient.discharge_date or '',date_format )