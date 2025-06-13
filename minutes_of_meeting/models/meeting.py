from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Meeting(models.Model):
    _name = 'meeting.minutes'
    _description = 'Minutes of Meeting'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = "meeting_subjects"

    topic_line_ids = fields.One2many('meeting.topic.line', 'meeting_id', string=" ")

    sequence_id = fields.Char(string="Sequence", required=True, copy=False, readonly=True, default='/')
    meeting_subjects = fields.Char(string="Meeting Subject", )
    customer = fields.Char(string="Customer")
    company_name = fields.Many2one(comodel_name='hr.employee', string="Company Name")
    client_team = fields.Char(string="Client Team")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('post', 'Post'),
        ('sent', 'Sent')
    ], string="Status", default='draft', tracking=True)

    project = fields.Boolean(string="Project")
    project_names = fields.Many2one(comodel_name='project.project', string="Project Name")

    lead = fields.Boolean(string="Lead")
    select_leads = fields.Many2one(comodel_name='hr.employee', String="Select Lead")

    start_date = fields.Datetime(string="Date")
    end_date = fields.Datetime(string="Time")

    duration_hours = fields.Char(string="Duration", compute='_compute_duration', store=True)
    location= fields.Text(string="Location")

    responisible_users = fields.Many2one(comodel_name="res.partner",string="Responsible User")
    attenties = fields.Many2one(comodel_name="res.partner",string="Attendees")
    absenties= fields.Many2one(comodel_name="res.partner",string="Absenties")

    note_taker = fields.Many2one(comodel_name='hr.employee', string="Note Taker")

    conclusion_notes= fields.Text(string="Conclusion")

    @api.model
    def create(self, vals):
        today = datetime.today().strftime('%d/%m/%Y')
        today_date = datetime.today().date()
        count = self.search_count([
            ('create_date', '>=', datetime.combine(today_date, datetime.min.time())),
            ('create_date', '<=', datetime.combine(today_date, datetime.max.time())),
        ]) + 1
        number = str(count).zfill(3)
        vals['sequence_id'] = f"MEET/{today}/{number}"
        return super().create(vals)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date > rec.start_date:
                delta = rec.end_date - rec.start_date
                total_seconds = int(delta.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                rec.duration_hours = f"{hours} hr {minutes} min"
            else:
                rec.duration_hours = "-"

    @api.onchange('start_date', 'end_date')
    def _onchange_date_validation(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            warning = {
                'title': "Invalid Date Range",
                'message': "End Date should be greater than or equal to Start Date.",
                'type': 'warning',
            }
            return {'warning': warning}

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError("End Date should be greater than or equal to Start Date.")

    def action_confirm(self):
        for rec in self:
            rec.write({'state': 'post'})

    def action_send_email(self):
        template_id = self.env.ref('minutes_of_meeting.email_template_meeting_minutes').id
        if template_id:
            self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        self.state = 'sent'

    def action_print(self):
        return self.env.ref('minutes_of_meeting.action_report_minutes_meeting').report_action(self)

class MeetingTopicLine(models.Model):
    _name = 'meeting.topic.line'
    _description = 'Meeting Topic Line'


    meeting_id = fields.Many2one('meeting.minutes', string="Meeting")
    agenda_item = fields.Char(string="Agenda / Item")
    discussion_summary = fields.Text(string="Discussion Summary")
    decision_notes = fields.Text(string="Decision / Notes")
    responsible_persons = fields.Many2one(comodel_name='hr.employee', string="Responsible Person")
    deadline = fields.Date(string="Deadline")
