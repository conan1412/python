import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

class ga_ac_general_attendance(osv.osv_memory):

    _name = 'ga.ac.general.attendance'
    _description = 'Print Attendance General Report'
    _columns = {
        'init_date': fields.date('Starting Date', required=True),
        'end_date': fields.date('Ending Date', required=True),
    }
    _defaults = {
         'init_date': lambda *a: time.strftime('%Y-%m-%d'),
         'end_date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def print_reports(self, cr, uid, ids, context=None):
        emp_ids = []
        visit_ids = []
        data_error = self.read(cr, uid, ids, context=context)[0]
        date_from = data_error['init_date']
        date_to = data_error['end_date']
        cr.execute("SELECT id FROM hr_attendance WHERE to_char(name,'YYYY-mm-dd')<=%s AND to_char(name,'YYYY-mm-dd')>=%s AND action IN %s ORDER BY name" ,(date_to, date_from, tuple(['sign_in','sign_out'])))
        attendance_ids = [x[0] for x in cr.fetchall()]
        if not attendance_ids:
            raise osv.except_osv(_('No Data Available!'), _('No records are found for your selection!'))
        attendance_records = self.pool.get('hr.attendance').browse(cr, uid, attendance_ids, context=context)

        for rec in attendance_records:
            if(rec.employee_id.id == False):
                if(rec.visitant_id.id not in visit_ids):
                    visit_ids.append(rec.visitant_id.id)
            else:    
                if(rec.employee_id.id not in emp_ids):
                    emp_ids.append(rec.employee_id.id)

        data_error['emp_ids'] = emp_ids
        data_error['visit_ids'] = visit_ids
        datas = {
             'ids': [],
             'model': 'hr.attendance',
             'form': data_error
        }
        return self.pool['report'].get_action(
            cr, uid, [], 'ga_access_control.report_attendance_general', data=datas, context=context
        )