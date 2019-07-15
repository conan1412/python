from openerp.osv import osv, fields
from openerp import api


class HrEmployee(osv.Model):
    """Inherit hr.employee to added fields to complete name
    """
    _inherit = 'hr.employee'

    def _get_full_name(self, cr, uid, ids, fields_name, args, context=None):
        """Method to concatenate last_name, second_last_name, name & second_name
        in a new field function
        """
        if context is None:
            context = {}
        res = {}
        for emp in self.browse(cr, uid, ids, context=context):
            res[emp.id] = (emp.last_name or '') + ' ' + (
                emp.second_last_name or '') + ' ' + (emp.first_name or '') + ' ' + (
                emp.second_name or '')
        return res

    def _update_fill_name(self, cr, uid, ids, context=None):
        """Method call function
        """
        return ids

    def _get_full_first_name(self, cr, uid, ids, fields_name, args,
                             context=None):
        if context is None:
            context = {}
        res = {}
        for emp in self.browse(cr, uid, ids, context=context):
            res[emp.id] = (emp.first_name or '') + ' ' + (emp.second_name or '')
        return res

    def _get_full_last_name(self, cr, uid, ids, fields_name, args,
                            context=None):
        if context is None:
            context = {}
        res = {}
        for emp in self.browse(cr, uid, ids, context=context):
            res[emp.id] = (emp.last_name or '') + ' ' + (
                emp.second_last_name or '')
        return res

    _columns = {
        'first_name': fields.char(
            'First Name', help='First employee name', required=True),
        'second_name': fields.char(
            'Second Name', help='Second employee name'),
        'last_name': fields.char(
            'First Last Name', help='Last employee name', required=True),
        'second_last_name': fields.char(
            'Second Last Name', help='Second employee last name'),
        'couple_last_name': fields.char(
            'Couple Last Name', help='Last name of employee couple'),
        'complete_name': fields.function(
            _get_full_name, string='Full Name', type='char', store={
                'hr.employee': (_update_fill_name, [
                    'name', 'second_name', 'last_name', 'second_last_name'],
                    50),
            }, method=True, help='Full name of employee, conformed by: Last \
            name + Second last name + Name + Second Name'),
        'full_first_name': fields.function(
            _get_full_first_name, string='Full First Name', type='char',
            store={
                'hr.employee': (
                    _update_fill_name, ['name', 'second_name'], 50),
            }, method=True, help='Full firs name of employee, conformed by: \
            Name + Second Name'),
        'full_last_name': fields.function(
            _get_full_last_name, string='Full last Name', type='char', store={
                'hr.employee': (_update_fill_name, [
                    'last_name', 'second_last_name'], 50),
            }, method=True, help='Full last name of employee, conformed by: \
            Last name + Second last name'),
    }

    @api.onchange('first_name')
    def change_first_name(self):
        return self._compute_first_name()

    @api.onchange('second_name')
    def change_second_name(self):
        return self._compute_first_name()

    @api.onchange('last_name')
    def change_last_name(self):
        return self._compute_first_name()

    @api.onchange('second_last_name')
    def change_second_last_name(self):
        return self._compute_first_name()


    def _compute_first_name(self):
        self.name = (self.last_name or '') + ' ' + (
            self.second_last_name or '') + ' ' + (self.first_name or '') + ' ' + (
            self.second_name or '')

    # @api.onchange('second_name')
    # def _compute_magic(self):
    #     self.name = (self.last_name or '') + ' ' + (
    #         self.second_last_name or '') + ' ' + (self.first_name or '') + ' ' + (
    #         self.second_name or '')
    #
    # @api.onchange('last_name')
    # def _compute_magic(self):
    #     self.name = (self.last_name or '') + ' ' + (
    #         self.second_last_name or '') + ' ' + (self.first_name or '') + ' ' + (
    #         self.second_name or '')
    #
    # @api.onchange('second_last_name')
    # def _compute_magic(self):
    #     self.name = (self.last_name or '') + ' ' + (
    #         self.second_last_name or '') + ' ' + (self.first_name or '') + ' ' + (
    #         self.second_name or '')
