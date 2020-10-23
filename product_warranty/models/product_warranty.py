

from odoo import models, fields, api

class ProductWarranty(models.Model):
    _inherit = 'product.template'
    product_warranty = fields.Text()
    date_to = fields.Date()
    date_from = fields.Date()

    def _convert_date(self, date):
        date_str = str(date.day)
        if date.day < 10:
            date_str = '0' + date_str
        if date.month < 10:
            date_str += '0' + str(date.month) + str(date.year - 2000)
        else:
            date_str += str(date.month) + str(date.year - 2000)
            return date_str

    @api.onchange('date_to', 'date_from')
    def _create_warranty_code(self):
        if self.date_to and self.date_from:
            date_to_str = self._convert_date(self.date_to)
            date_from_str = self._convert_date(self.date_from)
            self.product_warranty = 'PWR/' + str(date_from_str) + '/' + str(date_to_str)



