# Copyright 2015 Opener B.V. (<https://opener.am>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    incoterm_address_id = fields.Many2one(
        comodel_name="res.partner",
        string="Incoterm Address",
    )
    delivery_time_frame = fields.Char(string='Delivery Time Frame', default='1 month')
    delivery_place = fields.Char(string="Delivery Place")
    mov = fields.Monetary(string="MOV", currency_field='currency_id')
    deposit_percentage = fields.Float(string="Deposit", digits=(6, 2), default=10.0)
    condition_of_goods = fields.Selection([
        ('current', 'Current'),
        ('other', 'Other')],
        string="Condition of the Goods", default='current')
    validity_of_offer = fields.Char(string="Validity of the Offer")
    restrictions = fields.Text(string="Restrictions")
    # price_discount = fields.Float(string="Price Discount", digits=(6, 2), default=60.0)
    price = fields.Char(string="Price")
    documentation_provided = fields.Text(string="Documentation Provided", default="Sanitized Invoice Upon Request")
    commission_to_third_parties = fields.Selection([
        ('none', 'None'),
        ('yes', 'Yes')],
        string="Commission to Third Parties", default='none')
    Dial_bracelets = fields.Char(string="Dial & bracelets")
    SRP_CHF = fields.Char(string="SRP CHF")
    SRP_US = fields.Char(string="SRP US")
    SRP_JPN = fields.Char(string="SRP JPN")
    COST_CHF = fields.Char(string="COST CHF")
    Stock_HQ = fields.Char(string="Stock HQ")

    @api.onchange("partner_id")
    def onchange_partner_id_set_incoterm(self):
        partner = self.partner_id
        self.update(
            {
                "incoterm": partner.sale_incoterm_id.id,
                "incoterm_address_id": partner.sale_incoterm_address_id.id,
            }
        )
