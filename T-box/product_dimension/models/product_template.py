# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for length, height, width",
        readonly=False,
    )
    product_length = fields.Float(
        related="product_variant_ids.product_length", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
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

    country_of_origin = fields.Selection(
        selection=[
            ("VN", "Vietnam"),
            ("TH", "Thailand"),
            ("CN", "China"),
            ("HK", "Hong Kong"),
            ("CH", "Switzerland"),
            ("FR", "France"),
            ("AT", "Austria"),
            ("IN", "India"),
            ("XS", "Other"),
        ],
        string="Country of Origin",
    )
    ass = fields.Char(
        string="ASS",
    )
    commission_free = fields.Float(string='Commission Free')
    desc_limit = fields.Char(string='Description Limit')

    @api.model
    def _calc_volume(self, product_length, product_height, product_width, uom_id):
        volume = 0
        if product_length and product_height and product_width and uom_id:
            length_m = self.convert_to_meters(product_length, uom_id)
            height_m = self.convert_to_meters(product_height, uom_id)
            width_m = self.convert_to_meters(product_width, uom_id)
            volume = length_m * height_m * width_m

        return volume

    @api.depends(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def _compute_volume(self):
        for template in self:
            template.volume = template._calc_volume(
                template.product_length,
                template.product_height,
                template.product_width,
                template.dimensional_uom_id,
            )

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    def _prepare_variant_values(self, combination):
        """
        As variant is created inside template create() method and as
        template fields values are flushed after _create_variant_ids(),
        we catch the variant values preparation to update them
        """
        res = super()._prepare_variant_values(combination)
        if self.product_length:
            res.update({"product_length": self.product_length})
        if self.product_height:
            res.update({"product_height": self.product_height})
        if self.product_width:
            res.update({"product_width": self.product_width})
        return res
