from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    hs_code_eu = fields.Char(
        "HS Code EU",
        help="Standardized code for international shipping and goods declaration.",
    )
    hs_code_ch = fields.Char(
        "HS Code CH",
        help="Standardized code for international shipping and goods declaration.",
    )
