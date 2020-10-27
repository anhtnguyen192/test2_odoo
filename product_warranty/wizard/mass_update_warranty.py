from odoo import models, fields, api

class MassUpdateWarranty(models.TransientModel):
    _name = 'mass.update.warranty'
    date_from = fields.Date()
    date_to = fields.Date()

    def mass_update_warranty(self):
        active_ids = self._context.get('active_ids', []) or []
        for record in self.env['product.template'].browse(active_ids):
            record.date_from = self.date_from
            record.date_to = self.date_to