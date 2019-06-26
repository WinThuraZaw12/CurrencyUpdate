# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import openerp.addons.decimal_precision as dp


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    @api.depends('rate')
    def _compute_currency_rate(self):
    	for currency in self:
    		currency.rate = self.currency_id.rate

    rate = fields.Float(string='Current Rate', compute="_compute_currency_rate",readonly=True)

    @api.multi
    @api.onchange('currency_id')
    def currency_id_change(self):
        self.rate = self.currency_id.rate     


    @api.multi
    def action_wizard(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        view_id = ir_model_data.get_object_reference('synergy_account', 'view_currency_rate_update_form')[1]
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_currency_id': self.currency_id.id,
            'default_active': True,
        })
        return {
            'name': _('Currency'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.currency.rate',
            'views': [(view_id, 'form')],
            'view_id': view_id,            
            'target': 'new',
            'context': ctx,
        }