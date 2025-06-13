{
    "name": "Minutes Of Meeting",
    "version": "18.0",
    "summary": "Manage and track minutes of meetings",
    "description": "This module helps HR/project teams to record and follow up meeting minutes.",
    "author": "Durgaprasad",
    "license": "LGPL-3",
    "depends": ["base", "mail", "hr", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/meeting_views.xml",
        "report/report_minutes_meeting.xml",
        "data/mail_template.xml",
        "views/menu.xml",
    ],

}
