# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AbcSaleStockLevelHistory(models.Model):
    """ABC Classification Product Level History

    This model is used to display the history of values collected and involved
    into the computation of the ABC classification level.

    To avoid performance issue, the table is populated by bypassing the ORM
    since a new line is inserted by product and classification profile,
    each time the computation of the classification levels occurs.

    Some could argue that the same functionality could be achieved by using the
    tracking of changes mechanism provided by mail.thread. Nevertheless,
    mail.thread introduce a to high performance footprint and the result is not
    usable into reports
    """

    _name = "abc.sale_stock.level.history"
    _description = "Abc Sale_stock Level History"

    computed_level_id = fields.Many2one(
        "abc.classification.level",
        string="Computed classification level",
        readonly=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        index=True,
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product template",
        related="product_id.product_tmpl_id",
        readonly=True,
        store=True,
    )
    # percentage
    profile_id = fields.Many2one(
        "abc.classification.profile",
        string="Profile",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    product_level_id = fields.Many2one(
        "abc.classification.product.level",
        required=True,
        index=True,
        readonly=True,
        ondelete="cascade",
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        "Warehouse",
        readonly=False,
        ondelete="cascade",
    )
    ranking = fields.Integer(
        required=True,
        readonly=True,
        help="Ranking by number of oder lines",
    )
    number_so_lines = fields.Integer(
        "Number of sale order lines",
        required=True,
        readonly=True,
    )
    total_so_lines = fields.Integer(
        "Total of sale order lines",
        required=True,
        readonly=True,
    )
    percentage = fields.Float(
        required=True,
        readonly=True,
        help="Percentage of total sale order lines",
        digits=(7, 4),
        group_operator="SUM",
    )
    cumulated_percentage = fields.Float(
        required=True,
        readonly=True,
        help="Cumulated percentage of all the products with a better ranking",
        digits=(7, 4),
        group_operator=None,
    )
    total_products = fields.Integer(
        "Total products analysed",
        required=True,
        readonly=True,
        group_operator=None,
    )
    percentage_products = fields.Float(
        "Percentage of products",
        required=True,
        readonly=True,
        help="Percentage of total products analyzed",
        digits=(7, 4),
        group_operator="SUM",
    )
    cumulated_percentage_products = fields.Float(
        "Cumulated percentage of products",
        required=True,
        readonly=True,
        help="Cumulated percentage of total products analyzed with a " "better ranking",
        digits=(7, 4),
        group_operator=None,
    )
    sum_cumulated_percentages = fields.Float(
        "Sum of cummulated percentages",
        required=True,
        readonly=True,
        help="Sum cumulated % so lines and cumulated % products",
        group_operator=None,
    )
    from_date = fields.Date(readonly=True)
    to_date = fields.Date(readonly=True)
