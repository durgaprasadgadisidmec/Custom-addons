from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class SaleTargetId(models.Model):
    _name = 'sale.target'
    _description = 'Sale Target '
    _rec_name = "target_id"

    target_line_ids = fields.One2many('sale.target.line', 'target_id', string="Target Lines")

    target_id = fields.Char(string="Target ID",copy=False,)
    from_date = fields.Date(string="From Date", )
    to_date = fields.Date(string="To Date", )
    conformed_only = fields.Char(string="Confirmed only ")
    including_draft = fields.Char(string="Including Draft")
    only_draft = fields.Char(string="Only Draft")
    state = fields.Selection([
        ('comformed', 'Completed'),
        ('closed', 'Closed'),
    ], string="State", tracking=True)

    @api.model
    def create(self, vals):
        today = datetime.today().strftime('%d/%m/%Y')
        today_date = datetime.today().date()
        count = self.search_count([
            ('create_date', '>=', datetime.combine(today_date, datetime.min.time())),
            ('create_date', '<=', datetime.combine(today_date, datetime.max.time())),
        ]) + 1
        number = str(count).zfill(4)
        vals['target_id'] = f"TG/{today}/{number}"
        return super().create(vals)

    def action_completed(self):
        for rec in self:
            rec.state = 'comformed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'


class SaleTargetIdLine(models.Model):
    _name = 'sale.target.line'
    _description = 'Sale Target Line'

    target_id = fields.Many2one('sale.target', string="Sale Target")

    user_employee = fields.Many2one(comodel_name="hr.employee", string="User", required=True)
    target_amount= fields.Float(string="Target Amount")
    achievement = (fields.Float(string="Achievement"))
    balance = fields.Float(string="Balance", compute="_compute_balance", store=True)


    @api.depends('target_amount', 'achievement')
    def _compute_balance(self):
        for record in self:
            record.balance = (record.target_amount or 0.0) - (record.achievement or 0.0)

    @api.constrains('target_amount', 'achievement')
    def _check_achievement(self):
        for record in self:
            if (record.achievement or 0.0) > (record.target_amount or 0.0):
                raise ValidationError("Achievement cannot be greater than Target Amount.")


