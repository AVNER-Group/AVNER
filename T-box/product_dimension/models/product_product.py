# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_length = fields.Float("length")
    product_height = fields.Float("height")
    product_width = fields.Float("width")
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for length, height, width",
        default=lambda self: self.env.ref("uom.product_uom_meter"),
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )
    product_type = fields.Char(
        string="Product Type",
        default="Basic",
    )
    segment = fields.Char(
        string="Segment",
        default="SEGMENT",
    )

    product_line = fields.Char(
        string="Product Line",
    )

    product_category = fields.Char(
        string="Product Category",
    )

    pillar = fields.Char(
        string="Pillar",
    )

    family = fields.Char(
        string="Family",
    )

    pyramid = fields.Char(
        string="Pyramid",
    )

    shop_live = fields.Date(
        string="Shop Live",
        help="Date when the product is live in the shop.",
    )

    hs_code_eu = fields.Char(
        string="HS Code EU",
    )

    hs_code_ch = fields.Char(
        string="HS Code CH",
    )

    manufacturer = fields.Char(
        string="Manufacturer",
    )
    ass = fields.Char(
        string="ASS",
    )

    @api.depends(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def _compute_volume(self):
        template_obj = self.env["product.template"]
        for product in self:
            product.volume = template_obj._calc_volume(
                product.product_length,
                product.product_height,
                product.product_width,
                product.dimensional_uom_id,
            )

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]
