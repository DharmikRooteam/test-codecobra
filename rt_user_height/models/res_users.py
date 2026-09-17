from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

INCHES_PER_FOOT = 12
CM_PER_INCH = 2.54


class Users(models.Model):
    _inherit = 'res.users'

    height = fields.Float(
        string='Height (cm)',
        help='Height in centimetres. Converted to feet and inches automatically.',
    )
    height_ft = fields.Integer(
        string='Height (ft)',
        compute='_compute_height_ft_in',
        store=True,
        help='Whole feet part of the height.',
    )
    height_in = fields.Float(
        string='Height (in)',
        compute='_compute_height_ft_in',
        store=True,
        help='Remaining inches of the height (rounded to one decimal).',
    )
    height_display = fields.Char(
        string='Height',
        compute='_compute_height_ft_in',
        store=True,
        help='Height shown as e.g. "5 ft 9 in".',
    )

    @api.depends('height')
    def _compute_height_ft_in(self):
        for user in self:
            total_inches = user.height / CM_PER_INCH
            user.height_ft = int(total_inches // INCHES_PER_FOOT)
            user.height_in = round(total_inches % INCHES_PER_FOOT, 1)
            if user.height_ft and user.height_in:
                user.height_display = _('%(ft)s ft %(inch)s in') % {
                    'ft': user.height_ft,
                    'inch': f'{user.height_in:g}',
                }
            elif user.height_ft:
                user.height_display = _('%(ft)s ft') % {'ft': user.height_ft}
            elif user.height:
                user.height_display = _('%(inch)s in') % {'inch': f'{user.height_in:g}'}
            else:
                user.height_display = False

    @api.constrains('height')
    def _check_height(self):
        for user in self:
            if user.height < 0:
                raise ValidationError(_('Height cannot be negative.'))
            if user.height and user.height > 300:
                raise ValidationError(_('Height seems unrealistic (more than 300 cm).'))
