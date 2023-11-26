# Copyright 2019 Elico Corp, Dominique K. <dominique.k@elico-corp.com.sg>
# Copyright 2019 Ecosoft Co., Ltd., Kitti U. <kittiu@ecosoft.co.th>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

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
    price_discount = fields.Float(string="Price Discount", digits=(6, 2), default=60.0)
    documentation_provided = fields.Text(string="Documentation Provided", default="Sanitized Invoice Upon Request")
    commission_to_third_parties = fields.Selection([
        ('none', 'None'),
        ('yes', 'Yes')],
        string="Commission to Third Parties", default='none')


    def copy_data(self, default=None):
        if default is None:
            default = {}
        default["order_line"] = [
            (0, 0, line.copy_data()[0])
            for line in self.order_line
            if not line.is_deposit
        ]
        return super().copy_data(default)




class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    is_deposit = fields.Boolean(
        string="Is a deposit payment",
        help="Deposit payments are made when creating bills from a purchase"
        " order. They are not copied when duplicating a purchase order.",
    )

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=move)
        if self.is_deposit:
            res["quantity"] = -1 * self.qty_invoiced
        return res
