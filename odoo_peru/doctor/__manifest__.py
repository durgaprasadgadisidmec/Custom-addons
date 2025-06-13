{
    "name": "doctor",
    "version": "18.0",
    "category": "hidden",
    "author": "Alhaditech",
    "website": "https://www.alhaditech.com/",
   'license': 'AGPL-3',
    'images': ['static/description/dr.jpg'],
    "depends": [
        'base','sale',
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "view/doctor_wizard.xml",
        "view/doctor.xml",
    ],
    "installable": True,
}
