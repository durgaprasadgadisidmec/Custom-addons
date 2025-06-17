from odoo import models, fields,api, _
from odoo.exceptions import ValidationError
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    material=fields.Char("Material")
    shape=fields.Char("Shape")
    frame_types =fields.Char("Frame Type")
    rim=fields.Char("Rim")

    frames =fields.Boolean( string="Frames")
    contact_lens =fields.Boolean( string="Contact Lens")
    lens_treatment =fields.Boolean( string=" Lens Treatment")
    service =fields.Boolean( string="Service")
    miscellaneous =fields.Boolean( string="Miscellaneous")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=True)
    property_account_income_id=fields.Many2one("account.account","Income Account")
    property_account_expense_id=fields.Many2one("account.account","Expense Account")
    property_account_creditor_price_difference=fields.Many2one("account.account","Price Difference Account")
    brand=fields.Char("Brand")
    collection=fields.Char("Collection")



    sale_ok = fields.Boolean(string='Sales')
    purchase_ok = fields.Boolean(string='Purchase')



    @api.onchange('sale_ok', 'purchase_ok')
    def _onchange_exclusive_flags(self):
        # If sale is checked, disable purchase; if purchase is checked, disable sale
        if self.sale_ok and self.purchase_ok:
            # Prioritize the most recently modified field
            if self.env.context.get('active_test') is not None:  # typically unneeded
                pass
        if self.sale_ok:
            self.purchase_ok = False
        elif self.purchase_ok:
            self.sale_ok = False

    @api.constrains('frames', 'lens')
    def _check_exclusive_flags(self):
        for rec in self:
            if rec.frames and rec.lens :
                raise ValidationError("You cannot select multiple at the same time.")



    manufacturer=fields.Char("Manufacturer")

    lens =fields.Boolean( string="Lens")
    product_category=fields.Selection([
        ("frames", "Frames"),
        ("lens", "Lens"),
        ("contact_lens", "Contact Lens"),
        ("lens_treatment", "Lens Treatment"),
        ("service", "Service"),
        ("miscellaneous", "Miscellaneous"),

    ], string="Product Category",)

    def _for_attribute(self, cabecera, list_v, x):
        for v_id in cabecera:
            list_v.append([v_id])
            if x > 0:
                i = 0
                while i < len(list_v):
                    # print(list_v[i])
                    if v_id not in list_v[i]:
                        sw = 0
                        for c in cabecera:
                            if c in list_v[i]:
                                sw = 1
                        if list_v[i][0] not in cabecera and sw == 0:
                            new = list_v[i].copy()
                            new.append(v_id)
                            list_v.append(new)

                    i += 1

        return list_v

    def generate_combinations(self):
        if self.id:
            p = self
            # array_att_lines = []
            combinations = self.env['product.template.attribute.value'].sudo()
            if p.attribute_line_ids:
                array = []
                for att_line in p.attribute_line_ids:
                    if att_line.attribute_id.in_pos:
                        if att_line.value_ids:
                            array.append(att_line.value_ids.ids)
            list_v = []
            i = 0
            if len(array)>0:
                for line in array:
                    list_v = self._for_attribute(line, list_v, i)
                    i += 1
                if list_v:
                    for val_ids in list_v:
                        combination = self.env['product.template.attribute.value'].search([('product_attribute_value_id', 'in', val_ids)])
                        if combination:
                            attribute_values = combination.mapped('product_attribute_value_id')

                            if not self._exists_product_by_combination(p, attribute_values):
                                product = self.env['product.product'].sudo().create({
                                    'product_tmpl_id': p.id,
                                    'attribute_value_ids': [(6, 0, attribute_values.ids)]
                                })
                                print(combination)
                                _logger.info("producto creado default_code %s" % (product.default_code))
                            else:
                                _logger.info("Ya existe la combinación para este product template")
                            # product = p._create_product_variant(product_template_attribute_values)
                            a = 1
            else:
                ValidationError (_("No hay ningún atributo asignado para punto de ventas."))

    def _exists_product_by_combination(self, product_tmpl_id, attribute_values):

        product_exists = self.env['product.product'].sudo().search([('product_tmpl_id', '=', product_tmpl_id.id), ('attribute_value_ids', 'in', attribute_values.ids)])
        if not product_exists:
            return False

        if product_exists:
            sw = 0
            for p in product_exists:
                if sorted(p.attribute_value_ids.ids) == sorted(attribute_values.ids):
                    sw = 1
                    break

            if sw == 1:
                return True
            else:
                return False
