from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'hs_code' not in vals:
                category_id = vals.get('categ_id') or self.default_get(
                    ['categ_id']
                ).get('categ_id')
                if category_id:
                    category = self.env['product.category'].browse(category_id)
                    if category.hs_code_eu:
                        vals['hs_code_eu'] = category.hs_code_eu
                    if category.hs_code_ch:
                        vals['hs_code_ch'] = category.hs_code_ch
        return super().create(vals_list)
