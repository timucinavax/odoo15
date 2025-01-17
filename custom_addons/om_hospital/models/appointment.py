from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'ref'


    patient_id = fields.Many2one('hospital.patient', string='Patient', help='Patient name', ondelete='cascade')
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now, help='Time of booking')
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today, help='Date of booking')
    ref = fields.Char(string='Reference', tracking=True, default='HP00', help='This is reference to the patient record')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priority')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string='Status', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')

    
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_('You can delete only draft appointments.'))
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref


    def action_test(self):
        print('Clicked Button !!!!!!!')
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Clicked Successfully',
                'type': 'rainbow_man',
            }
        }


    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'



class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default='1')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')