from datetime import datetime,timedelta,time
from openerp.osv import osv
from openerp.report import report_sxw
import pytz
from openerp import SUPERUSER_ID

class attendance_prints(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(attendance_prints, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'lst': self._lst,
            'total': self._lst_total,
            'get_employees':self._get_employees,
        })

    def _get_employees(self, emp_ids):
        emp_obj_list = self.pool.get('hr.employee').browse(self.cr, self.uid, emp_ids)
        return emp_obj_list

    def _lst(self, employee_id, dt_from, dt_to, *args):
        #consult the records in the range
        self.cr.execute("select date_in, date_out, authorizes, department_id, action, observations_output_id, observations_entry_id, irregularity_output_id, irregularity_entry_id from hr_attendance where employee_id=%s and to_char(name,'YYYY-mm-dd')<=%s and to_char(name,'YYYY-mm-dd')>=%s and action IN (%s,%s) order by name", (employee_id, dt_to, dt_from, 'sign_in', 'sign_out'))
        res = self.cr.dictfetchall()
        # get user's timezone
        # get localized dates
        user_pool = self.pool.get('res.users')
        user = user_pool.browse(self.cr, SUPERUSER_ID, self.uid)
        #if not assigned the timezone for default will been Caracas
        if user.partner_id.tz == False:
            tz = pytz.timezone('America/Caracas') or pytz.utc
        else:
            tz = pytz.timezone(user.partner_id.tz) or pytz.utc
        for r in res:
            r['authorizes'] = self.pool.get('res.users').browse(self.cr,self.uid,r["authorizes"]).name
            r['department_id'] = self.pool.get('hr.department').browse(self.cr,self.uid,r["department_id"]).name
            
            if(r['observations_entry_id'] == None):
                # if language is spanish Venezuelan defined values
                if(user.partner_id.lang == "es_VE"):
                    r['observations_entry_id'] = "No aplica" 
                else:
                    r['observations_entry_id'] = 'No apply'
            else:
                r['observations_entry_id'] = self.pool.get('ga.ac.observations.entry').browse(self.cr,self.uid,r['observations_entry_id']).name_observations_e 

            if(r['observations_output_id'] == None):
                # if language is spanish Venezuelan defined values
                if(user.partner_id.lang == "es_VE"):
                    r['observations_output_id'] = "No aplica" 
                else:
                    r['observations_output_id'] = 'No apply'
            else:
                r['observations_output_id'] = self.pool.get('ga.ac.observations.output').browse(self.cr,self.uid,r['observations_output_id']).name_observations_o 

            if(r['irregularity_entry_id'] == None):
                # if language is spanish Venezuelan defined values
                if(user.partner_id.lang == "es_VE"):
                    r['irregularity_entry_id'] = "No aplica"
                else:
                    r['irregularity_entry_id'] = 'No apply'
            else:
                r['irregularity_entry_id'] = self.pool.get('ga.ac.irregularity.entry').browse(self.cr,self.uid,r['irregularity_entry_id']).name_irregularity_e
            
            if(r['irregularity_output_id'] == None):
                # if language is spanish Venezuelan defined values
                if(user.partner_id.lang == "es_VE"):
                    r['irregularity_output_id'] = "No aplica"  
                else:
                    r['irregularity_output_id'] = 'No apply'
            else:
                r['irregularity_output_id'] = self.pool.get('ga.ac.irregularity.output').browse(self.cr,self.uid,r['irregularity_output_id']).name_irregularity_o

            signin_datetime = pytz.utc.localize(datetime.strptime(r['date_in'], '%Y-%m-%d %H:%M:%S')).astimezone(tz)
            r['date_in'] = str(signin_datetime.date()) + ' ' + str(signin_datetime.timetz())
            if r['action'] == 'sign_out':
                signout_datetime = pytz.utc.localize(datetime.strptime(r['date_out'], '%Y-%m-%d %H:%M:%S')).astimezone(tz)
                r['date_out'] = str(signout_datetime.date()) + ' ' + str(signout_datetime.timetz())
                r['delay'] = signout_datetime - signin_datetime
            else:
                r['delay'] = signin_datetime - signin_datetime

            # if language is spanish Venezuelan defined values
            if(user.partner_id.lang == "es_VE"):
                if(r["action"] == "sign_in"):
                    r["action"] == "Entrada"
                elif(r["action"] == "sign_out"):
                    r["action"] == "Salida"
            else:
                if(r["action"] == "sign_in"):
                    r["action"] = "Sign in"
                elif(r["action"] == "sign_out"):
                    r["action"] = "Sign out"
        return res

    def average_time(self,values):
        total = timedelta(seconds = 0, minutes = 0, hours = 0)
        if len(values) == 0:
            return total
        cont = 0
        for x in values:
            if type(x) == datetime:
                x = timedelta(seconds = x.second, minutes = x.minute, hours = x.hour)
            total += x  
            if(timedelta(seconds = 0, minutes = 0, hours = 0).total_seconds() != x.total_seconds()):
                cont += 1
        if cont != 0:
            total /= cont
        return total

    #calculate the average
    def _lst_total(self, employee_id, dt_from, dt_to, *args):
        self.cr.execute("select date_in, date_out, action from hr_attendance where employee_id=%s and to_char(name,'YYYY-mm-dd')<=%s and to_char(name,'YYYY-mm-dd')>=%s and action IN (%s,%s) order by name", (employee_id, dt_to, dt_from, 'sign_in', 'sign_out'))
        res = self.cr.dictfetchall()
        if not res:
            return ('/','/')
        average_in = []
        average_out = []
        average_time_in_instalations = []
        for r in res:
            # get user's timezone
            user_pool = self.pool.get('res.users')
            user = user_pool.browse(self.cr, SUPERUSER_ID, self.uid)
            if user.partner_id.tz == False:
                tz = pytz.timezone('America/Caracas') or pytz.utc
            else:
                tz = pytz.timezone(user.partner_id.tz) or pytz.utc
            # get localized dates
            signin_datetime = pytz.utc.localize(datetime.strptime(r['date_in'], '%Y-%m-%d %H:%M:%S')).astimezone(tz)
            r['date_in'] = signin_datetime
            average_in.append(r['date_in'])
            if r['action'] == 'sign_out':
                signout_datetime = pytz.utc.localize(datetime.strptime(r['date_out'], '%Y-%m-%d %H:%M:%S')).astimezone(tz)
                worked_hours = signout_datetime - signin_datetime
                r['date_out'] = signout_datetime
                average_time_in_instalations.append(worked_hours)
                average_out.append(r['date_out'])   
            else:
                average_time_in_instalations.append(signin_datetime - signin_datetime)

        total = self.average_time(average_time_in_instalations)
        AVI = self.average_time(average_in)
        AVO = self.average_time(average_out)
        result_dict = {
            'average_in':AVI and str(AVI).split('.')[0],
            'average_out':AVO and str(AVO).split('.')[0],
            'total_average': total and str(total).split('.')[0]
        }

        return [result_dict]

class report_hr_attendance_errors(osv.AbstractModel):
    _inherit = 'report.hr_attendance.report_attendanceerrors'
    _template = 'ga_access_control.report_attendanceerrors'
    _wrapped_report_class = attendance_prints