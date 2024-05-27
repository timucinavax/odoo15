from datetime import datetime
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    bid_type = fields.Selection([('cash', 'Cash'), ('postpaid', 'Postpaid')], string='Bid Type')
    payment_info_ids = fields.One2many('sale.order.payment.info', 'sale_order_id', string='Payment Information')

    def action_confirm(self):
        if self.bid_type == 'cash':
            if not self.payment_info_ids:
                raise ValidationError(_('Please provide payment information.'))
            
            total_payment = sum(payment_info.total for payment_info in self.payment_info_ids)
            
            for payment_info in self.payment_info_ids:
                if not payment_info.payment_type_id or payment_info.total <= 0:
                    raise ValidationError(_('Invalid payment type or total amount in payment information.'))
            if not float_is_zero(self.amount_total - total_payment, precision_rounding=self.currency_id.rounding):
                raise ValidationError(_('Please check the total amount.'))    
            super(SaleOrder, self).action_confirm()
            
            self._create_invoices()
            print("eeeeeeeeeeeeeeeeeeeeeeee")
            payments = []
            for pay in self.payment_info_ids:
                payment_vals = {
                    'amount': pay.total,
                    # 'payment_date': fields.Datetime.now(),
                    'payment_method_id':1,
                    # 'ref': self.invoice_ids.name,
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'partner_id': self.partner_id.id,
                    'journal_id': pay.payment_type_id.id,
                    'currency_id': self.currency_id.id,
                }
                payments.append(payment_vals)
                print("*** * * * * **      ", payment_vals)
            for payment in payments:
                self.env['account.payment'].create(payment).action_post()
        
        else:
            invoices = self.env['account.move'].search([('move_type', '=', 'out_invoice'),
                                                        ('partner_id', '=', self.partner_id.id)])
            total_un_paid = 0
            for invoice in invoices:
                if invoice.state == 'posted':
                    if invoice.payment_state == 'not_paid':
                        total_un_paid += invoice.amount_residual
            total_un_paid += self.amount_total
            remaining_credit = self.partner_id.limit - float(total_un_paid)
            if int(remaining_credit) <= 0:
                print("=======================================================================================================", remaining_credit)
                print("=======================================================================================================", total_un_paid)
                raise ValidationError(_('Please you have reach limited amount.'))
            else:
                super(SaleOrder, self).action_confirm()
                self._create_invoices().action_post()


    @api.onchange('bid_type')
    def _onchange_bid_type(self):
        domain =[]
        if self.bid_type == 'cash':
            domain.append(('cash', '=', True))
        else:
            domain.append(('postpaid', '=', True))
        return {'domain' : {'partner_id' : domain}}



# Sale Order Payment Info
class SaleOrderPaymentInfo(models.Model):
    _name = 'sale.order.payment.info'
    _description = 'Sale Order Payment Information'

    payment_type_id = fields.Many2one('account.journal', string='Payment Type', domain="[('name', 'in', ['Bank', 'Cash'])]")
    total = fields.Float(string='Total')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    
    @api.onchange('payment_type_id')
    def _onchange_payment_type_id(self):
        if self.sale_order_id:
            self.total = self.sale_order_id.amount_total
