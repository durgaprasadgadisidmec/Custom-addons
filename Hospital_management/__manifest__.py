{
    "name": "Hospital management system",
    "author": "Durga",
    "version": "18.0",
    "license": "LGPL-3",
    "depends": ["base","account","web","sale_management", "mail","report_xlsx",],
    "data":
        [
            "security/ir.model.access.csv",
            "data/patient_confirm_mail.xml",
            "views/res_partner_gst_view.xml",
            "views/view_doctor.xml",
            "views/view_patient.xml",
            "views/view_sale_order.xml",
            "views/view_patient_lines.xml",
            "views/patient_invoices.xml",
            "wizard/discharge_wizard_view.xml",
            "wizard/patient_wizard_invoices.xml",
            "wizard/sale_order_wizard.xml",
            "report/report.xml",
            "report/report_patient_template.xml",
            "report/wizard_reports.xml",
            "report/salesperson_pdf_fromtodates_template.xml",
            "views/menu.xml",
        ]

}
