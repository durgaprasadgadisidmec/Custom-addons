
{
    "name": "Optical ERP",
    "version": "18.0",
    "category": "Optical",
    'summary': "Solution for Optical(EYE) shops and clinics",
    'description': """""
    odoo Solution for Optical(EYE) shops and clinics.
    """,
    "author": "Alhaditech",
    "website": "www.alhaditech.com",
   'license': 'AGPL-3',
    'images': ['static/description/background.png','static/description/background2.png'],
    "depends": [
        'base','sale','doctor', 'point_of_sale','account'
    ],
    'price': 120, 'currency': 'EUR',
    'assets': {
    'point_of_sale._assets_pos': [
        'optical_erp/static/src/js/script.js',
        'optical_erp/static/src/js/create_product.js',
        'optical_erp/static/src/js/models.js',
        'optical_erp/static/src/js/receipt.js',
        'optical_erp/static/src/xml/pos.xml',
        'optical_erp/static/src/xml/prescription_history.xml',
    ],
    },
    "data": [
        'security/groups.xml',
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/sequence.xml",
        #"data/ir_cron.xml", #Nuevo 2021-10-30
        "report/reports.xml",
        "report/sale_report.xml",
        'views/pos_order_view.xml',
        "views/product_product.xml",
        "report/prescription_report.xml",
        "views/prescription.xml",
        "views/res_config_settings_views.xml",
        "views/partner.xml",
        "views/test_type.xml",
        "views/inerit_sale_order.xml",
        'views/pos_template.xml',
        'views/product_attribute_view.xml',
        'views/product_template_views.xml',#Nuevo 2021-10-30
        'data/optical_pos_product_variants.xml',
        "views/complete_pair.xml",
    ],
    'qweb': ['static/src/xml/pos.xml', 'static/src/xml/prescription_history.xml'],
    "installable": True,
    'application': True,
}
