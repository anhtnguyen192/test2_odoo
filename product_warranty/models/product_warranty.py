

from odoo import models, fields, api

class ProductWarranty(models.Model):
    _inherit = 'product.template'

    date_to = fields.Date()
    date_from = fields.Date()
    product_warranty = fields.Text(compute="_create_warranty_code", store="True")
    discount_status = fields.Boolean(compute="_check_discount_status", store="True")


    def _convert_date(self, date):
        date_str = str(date.day)
        if date.day < 10:
            date_str = '0' + date_str
        if date.month < 10:
            date_str += '0' + str(date.month) + str(date.year - 2000)
        else:
            date_str += str(date.month) + str(date.year - 2000)
        return date_str

    @api.depends('date_to', 'date_from')
    def _check_discount_status(self):
        for r in self:
            date = fields.date.today()
            if r.date_to and r.date_from:
                if (date - r.date_from).days < 0 or (date - r.date_to).days > 0:
                    r.discount_status = True
                else:
                    r.discount_status = False
            else:
                r.discount_status = True


    @api.depends('date_to', 'date_from')
    def _create_warranty_code(self):
        for r in self:
            if r.date_to and r.date_from:
                date_to_str = self._convert_date(r.date_to)
                date_from_str = self._convert_date(r.date_from)
                r.product_warranty = 'PWR/' + str(date_from_str) + '/' + str(date_to_str)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    discount_status_unit = fields.Boolean(related="product_id.discount_status")
    sale_order_discount_unit = fields.Float('Unit Discount', compute="_estimate_discount_unit")

    @api.depends('product_id', 'price_unit')
    def _estimate_discount_unit(self):
        for r in self:
            if r.discount_status_unit:
                r.sale_order_discount_unit = r.price_unit / 10
            else:
                r.sale_order_discount_unit = 0.0


class SaleOderWarrant(models.Model):
    _inherit = 'sale.order'
    sale_order_discount_estimated = fields.Monetary(string="Estimated Discount", store=True, readonly=True, compute='_estimate_discount_all')

    @api.depends('order_line.sale_order_discount_unit')
    def _estimate_discount_all(self):
        for order in self:
            sale_order_discount_estimated = 0.0
            for line in order.order_line:
                sale_order_discount_estimated += line.sale_order_discount_unit
            order.update({
                'sale_order_discount_estimated': sale_order_discount_estimated,

            })











