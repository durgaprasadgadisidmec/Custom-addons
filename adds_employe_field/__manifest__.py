{
    'name': 'Employee Custom Field',
    'version': '18.0',
    'author': 'Durgaprasad',
    'license': 'LGPL-3',
    'category': 'Sales, CRM, Accounting, Inventory',
    'summary': 'Add Employee field to Sale Order, CRM, Account and Stock modules',
    'meta search':'emplyee selection in slaes, crm, invoice, delivery',
    'description': """This module extends the core Odoo Sales, CRM,Invoice,Delivery and HR modules by adding a custom Employee field to key models such as:
                    - Sales Orders
                    - CRM Opportunities
                    - Invoices
                    - Delivery Orders""",

    'depends': ['sale_management','crm','account','stock','hr'
                ],
    'data': [
        'views/view_crm.xml',
        'views/view_delivery.xml',
        'views/view_invoice.xml',
        'views/view_sale.xml',
    ],
}
