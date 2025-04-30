from odoo import fields, models


class CustomerReport(models.TransientModel):
    _name = 'sales.wizard'
    _description = 'Salesman report Wizard'
    # _inherit = "sale.order"

    #salesperson = fields.Many2one("res.partner", String="Salesman")
    users = fields.Many2one("res.users", String="Users")
    from_date = fields.Date(String="From_date")
    to_date = fields.Date(String="to_date")

    def view_salesman_report(self):
        for rec in self:
            domain = [('user_id', '=', rec.users.id)]

            if rec.from_date:
                domain.append(('date_order', '>=', rec.from_date))
            if rec.to_date:
                domain.append(('date_order', '<=', rec.to_date))

            sale_orders = self.env["sale.order"].search(domain, limit=10, order='date_order desc')

            total_amount = sum(order.amount_total for order in sale_orders)

            data = {
                'sale_orders': [
                    {
                        'name': order.name,
                        'amount_total': order.amount_total,
                        'partner_name': order.partner_id.name,
                    }
                    for order in sale_orders
                ],
                'wizard': {
                    'sales_person': rec.users.name,
                    'from_date': rec.from_date,
                    'to_date': rec.to_date,
                    'total_amount': total_amount,
                }
            }

            return self.env.ref('Hospital_management.report_wizard_salesperson_pdf').report_action(self, data=data)

    # def get_report_values(self, docids, data=None):
    #     wizard = self.env['your.wizard.model'].browse(docids)
    #     sale_orders = [
    #         {
    #             'invoice_date': '20/04/2025',
    #             'invoice_no': 'INV001',
    #             'customer_name': 'ADDRESS BURGER',
    #             'invoice_amount': 7701.00,
    #             'pending_amount': 7701.00,
    #             'due_date': '30/04/2025',
    #             'days_over': 5
    #         },
    #         # add more rows here
    #     ]
    #     return {
    #         'doc_ids': docids,
    #         'doc_model': 'your.wizard.model',
    #         'wizard': {
    #             'salesperson_name': wizard.salesperson_id.name,
    #             'to_date': wizard.to_date,
    #             'generated_datetime': fields.Datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')
    #         },
    #         'sale_orders': sale_orders
    #     }
