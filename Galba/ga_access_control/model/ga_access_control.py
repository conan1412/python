# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo Galba Web Login Screen”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 21/11/2016
#moduleauthor: Yesenia Morales <ymorales@guardiandelalba.pdvsa.com>
#moduleauthor: Osvaldo López <olopez@guardiandelalba.pdvsa.com>
#moduleauthor: Rubén Garcia <garciara@guardiandelalba.pdvsa.com>
#moduleauthor: Miguel Villamizar <villamizarm@guardiandelalba.pdvsa.com>
#
from openerp import models, fields, api, _, tools
from openerp.osv import osv
from openerp.modules.module import get_module_resource
import pprint
import time
from datetime import datetime

"""
"" The hr_accesscontrol class, using a transient model, is used for wizard-like interaction
"" The search_employee method, refers to the button used in the view, mainly performs the
"" Search for the Employee ID number, and in turn loads the data in the referenced view to the
"" Attendance record.
"""
def _get_authorizes(self, cr, uid, context=None):
  user = uid
  return user

def _employee_get(obj, cr, uid, context=None):
  ## ---> Set BreakPoint
  if context.get("employes_id"):
      return context.get("employes_id")
  else:
      ids = None #obj.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
      return ids and ids[0] or False

def _visitant_get(obj, cr, uid, context=None):

  if context.get("visitant_id"):
      return context.get("visitant_id")
  else:
      ids2 = None
      return ids2 and ids2[0] or False

def _get_department(obj, cr, uid, context=None):
  if(context.get("department_id")):
      return context.get("department_id")
  else:
      ids3 = None
      return ids3 and ids3[0] or False


class hr_accesscontrol(models.TransientModel):
  _name = 'ga.access.control'
  identification_id = fields.Char('Identification card', translate=True, 
                                  help="Enter Employee Identification", 
                                  required=True, size=12)

  identificationE = fields.Char('Identification entrance',size=60,
                                compute="search_LastRecord")
  nameE = fields.Char('Name Entrance',size=60,compute="search_LastRecord")
  conditionE = fields.Char('Condition entrance',size=60, compute="search_LastRecord")
  positionE = fields.Char('Position entrance',size=60,compute="search_LastRecord")
  extensionE = fields.Char('Extension entrance',size=60,compute="search_LastRecord")
  identificationO = fields.Char('Identification output',size=60, compute="search_LastRecordexit")
  nameO = fields.Char('Name output',size=60,compute="search_LastRecordexit")
  conditionO = fields.Char('Condition output',size=60, compute="search_LastRecordexit")
  positionO = fields.Char('Position output',size=60, compute="search_LastRecordexit")
  extensionO = fields.Char('Extension output',size=60, compute="search_LastRecordexit")
  imageE = fields.Binary("Photo entrance",compute="search_LastRecord")
  imageO = fields.Binary("Photo ouput", compute="search_LastRecordexit")
  people = fields.Integer('People currently inside facility',compute="_compute_people_sign_in", store=False)

  #assigned a default image for to create a visitant
  @api.one
  def _get_default_image(self):
    image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
    return tools.image_resize_image_medium(open(image_path, 'rb').read().encode('base64'))

  #For the principal screen search the lastest record of the entrance
  @api.multi
  @api.depends('nameE','identificationE','imageE','positionE','extensionE')
  def search_LastRecord(self):
    consult = self.env['hr.attendance']
    lastrecord = consult.search([], limit=1, order='date_in desc') # find in the Base data the last record entry
    if lastrecord.employee_id:
      self.nameE = lastrecord.employee_id.complete_name
      self.identificationE = lastrecord.employee_id.identification_id
      self.imageE = lastrecord.employee_id.image_medium
      self.positionE = lastrecord.employee_id.job_id.name
      self.conditionE = lastrecord.department_id.name
      self.extensionE = lastrecord.employee_id.extension
    elif lastrecord.visitant_id:
      self.nameE = lastrecord.visitant_id.full_name
      self.identificationE = lastrecord.visitant_id.identification_number
      self.imageE = lastrecord.visitant_id.image_medium
      self.positionE = lastrecord.visitant_id.visitant_type_id.type
      self.conditionE = lastrecord.department_id.name
      self.extensionE = lastrecord.visitant_id.telephone_mobile
    else:
      self.imageE = self._get_default_image() #No record, assigned image default
  
  #Compute People currently inside facility  
  @api.one
  @api.depends('identification_id')
  def _compute_people_sign_in(self):
    self.people = len(self.env['hr.attendance'].search([('action','=','sign_in')]))

  #For the principal screen search the lastest record of the exit
  @api.multi
  @api.depends('nameO','identificationO','imageO','positionO','extensionO')
  def search_LastRecordexit(self):
    consult2 = self.env['hr.attendance']
    lastrecord2 = consult2.search([('action', '=', 'sign_out')],limit=1, order='date_out desc')# find in the Base data the last record exit
    if lastrecord2.date_out:
      if lastrecord2.employee_id:
        self.nameO = lastrecord2.employee_id.complete_name
        self.identificationO = lastrecord2.employee_id.identification_id
        self.imageO = lastrecord2.employee_id.image_medium
        self.positionO = lastrecord2.employee_id.job_id.name
        self.conditionO = lastrecord2.department_id.name
        self.extensionO = lastrecord2.employee_id.extension
      elif lastrecord2.visitant_id:
        self.nameO = lastrecord2.visitant_id.full_name
        self.identificationO = lastrecord2.visitant_id.identification_number
        self.imageO = lastrecord2.visitant_id.image_medium
        self.positionO = lastrecord2.visitant_id.visitant_type_id.type
        self.conditionO = lastrecord2.department_id.name
        self.extensionO = lastrecord2.visitant_id.telephone_mobile
    else:
      self.imageO = self._get_default_image() #No record, assigned image default

  #For discard the exit to a person is very needed restore the record
  @api.multi
  def restore(self,record,*variable):
    self.env.cr.execute('UPDATE '+self.env['hr.attendance']._table+' SET action = %s, date_out = %s WHERE id = %s',('sign_in',None,record))# change action at sign in

  #Search the entrance a person in the facility
  @api.multi
  def search_employee(self):
    context2 = self._context.copy()
    card = self.identification_id
    if(not card.isdigit()): # if not is a number, it does not do nothing 
      self.identification_id = ''
      return
    if(card[0]=='0'):#if the first argument is 0 to the pass is fast (case is code bar)
      code = True
    else:
      code= False
    card = int(card)
    consult = self.env['hr.employee'] 
    #search employee for identification card or internal identification
    employee = consult.search(['|',('identification_id', '=', card),('otherid','=',card)])
    idEmployee = employee.id
    consultStatus = self.env['resource.resource'] #cosult status of the employee
    statusEmployee = consultStatus.search([['id', '=', employee.resource_id.id]])
    if(statusEmployee.active): #if he/she is a employee active
        view_id = self.env['ir.ui.view'].search([('name', '=', 'hr.attendance form')])#defined the view
        consult = self.env['hr.attendance']
        #Consult the last record for is person
        lastRecord = consult.search([('employee_id', '=', idEmployee)], limit=1, order='id desc')

        if(lastRecord.action == 'sign_in'):#this is for the person that sign out
            record = lastRecord.id
            var_date_out = fields.Datetime.now()
            #Add the field date_out and change the action
            self.env.cr.execute('UPDATE '+self.env['hr.attendance']._table+' SET action = %s, date_out = %s WHERE id = %s',('sign_out',var_date_out,record))
        else:#this is for the person that sign in
            record = None

        #Define the employee, the view and department for the new record
        context2.update({
              'employes_id': employee.id,
              'view_id': view_id.id,
              'department_id': employee.department_id.id,
        })

        if(code):#if the entrance is for code bar
          if(lastRecord.action == 'sign_out' or lastRecord.action == False):
            vals = {
              'employee_id':employee.id,
              'department_id': employee.department_id.id,
            }
            self.env['hr.attendance'].create(vals) #create record
          return

        res = {
               'name': _('Attendance'),
               'type': 'ir.actions.act_window',
               'res_model': 'hr.attendance',
               'view_type': 'form',
               'view_id': view_id.id,
               'view_mode': 'form',
               'nodestroy': True,
               'target': 'current',
               'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
               'context': context2,
               'res_id': record # load if record exist
        }
        return res#Send a new screen
    else:
        consult = self.env['ga.ac.visitant']
        #search the visitant for identification card
        visitant = consult.search([['identification_number', '=', card]])
        idvisitant = visitant.id
        #defined the view for the visitant
        view_id = self.env['ir.ui.view'].search([('name', '=', 'hr.attendance form visitant')])
        if(idvisitant == False):#if visitant not exist validate that not is a Ex-employee
          exEmployee = self.env['hr.employee'].search([('identification_id','=',card),('active','!=','true')])
          if(exEmployee.id != False):#if is a Ex-employee
            #It define attributes
            vals = {
              'identification_number': exEmployee.identification_id,
              'name_visitant': exEmployee.full_first_name,
              'surname_visitant': exEmployee.full_last_name,
              'country_id': exEmployee.country_id.id,
              'telephone_mobile': exEmployee.mobile_phone,
              'visitant_type_id': 1,
              'image_medium':exEmployee.image_medium
            }
            #Create a record in visitant with data of the employee
            new_visitant = self.env['ga.ac.visitant'].create(vals)
            idvisitant = new_visitant.id
            visitant = new_visitant
          else:# Else generate an alert
              raise osv.except_osv(_('Alert!!!'), _('Sorry, this person is not registered'))

        if(idvisitant != False):
          consult = self.env['hr.attendance']
          #Consult the last record for is person
          lastRecord = consult.search([('visitant_id', '=', idvisitant)], limit=1, order='id desc')

          if(lastRecord.action == 'sign_in'):
            record = lastRecord.id
            var_date_out = fields.Datetime.now()
            #Add the field date_out and change the action
            self.env.cr.execute('UPDATE '+self.env['hr.attendance']._table+' SET action = %s, date_out = %s WHERE id = %s',('sign_out',var_date_out,record))
          else:
            record = None

          #Define the visitant, the view for the new record
          context2.update({
                  'visitant_id': visitant.id,
                  'view_id': view_id.id,
              })

          res = {
                 'name': _('Attendance'),
                 'type': 'ir.actions.act_window',
                 'res_model': 'hr.attendance',
                 'view_type': 'form',
                 'view_id': view_id.id,
                 'view_mode': 'form',
                 'nodestroy': True,
                 'target': 'current',
                 'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}, #to open in edit mode
                 'context': context2,
                 'res_id': record #load if record exist
              }
          return res#Send a new screen

"""
"" The _employee_get method is a global method for the model, which is used to perform
"" The employee data load, this performs a comparison between the arriving id and the
"" Which are in the reference table.
"""

class hr_employee_id(models.Model):
    _inherit = "hr.employee"
    otherid = fields.Char('Other Id',compute='_define_id',store=True,required=True,)
    
    #assigned a default image for to create a visitant
    def _get_default_image(self, cr, uid, context=None):
      image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
      return tools.image_resize_image_medium(open(image_path, 'rb').read().encode('base64'))
    
    #define a default image for employee
    _defaults= {
      'image_medium':_get_default_image,
    }

    #compute a other id "is a internal id for the employee"
    @api.one
    @api.depends("identification_id")
    def _define_id(self):
      employees = self.env['hr.employee'].search([],limit=1 ,order="id desc")
      self.otherid = employees.id
      

"""
"" The hr_attendance class redefines the parent class, and calls the global method _employee_get
"""
class hr_attendance(models.Model):
  _inherit = "hr.attendance"
  authorizes = fields.Many2one('res.users', 'Authorizes')
  employee_id = fields.Many2one('hr.employee','Employee', required=False) # remove NULL restrictions
  irregularity_output_id = fields.Many2one('ga.ac.irregularity.output', 'Irregularity Exit')
  observations_entry_id = fields.Many2one('ga.ac.observations.entry', 'Observations Entry')
  irregularity_entry_id = fields.Many2one('ga.ac.irregularity.entry', 'Irregularity Entry')
  observations_output_id = fields.Many2one('ga.ac.observations.output', 'Observations Exit')
  date_in = fields.Datetime('Date in', select=1)
  date_out = fields.Datetime('Date out', select=1)
  visitant_id = fields.Many2one('ga.ac.visitant', 'Visitant')
  vehicle_id = fields.Many2one('ga.ac.vehicle','Vehicle')
  post_service_id = fields.Many2one('ga.ac.service.post', 'Service post')
  department_id = fields.Many2one('hr.department', 'Department', required=True,)
  identification_employee = fields.Char(string='Identification Employee', related="employee_id.identification_id")
  identification_visitant = fields.Integer(string='Identification Visitant', related="visitant_id.identification_number")

  _defaults = {
    'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'), #please don't remove the lambda, if you remove it then the current time will not change
    'employee_id': _employee_get,
    'visitant_id': _visitant_get,
    'date_in': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    'action': 'sign_in',
    'department_id': _get_department,
    'authorizes': _get_authorizes
  }

  #It overwrites function _altern_si_so because it generates errors with the implementations of visitant
  def _altern_si_so(self, cr, uid, ids, context=None):#Do not touch
    return True

  _constraints=[(_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])]

  #it calculates hours in the installations
  @api.multi
  def worked_hours_compute(self,record,*variable):
    last_signin_datetime = datetime.strptime(self.date_in, '%Y-%m-%d %H:%M:%S')
    signout_datetime = datetime.strptime(self.date_out, '%Y-%m-%d %H:%M:%S')
    workedhours_datetime = (signout_datetime - last_signin_datetime)
    hours = ((workedhours_datetime.seconds)) / 60.0
    self.env.cr.execute('UPDATE '+self.env['hr.attendance']._table+' SET worked_hours = %s WHERE id=%s',(hours,record))
