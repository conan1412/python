#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Module of Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 02/12/2016
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api, _
from datetime import datetime
from openerp import exceptions
from openerp.exceptions import except_orm
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT


class GaHrWorkExperience(models.Model):
	'''
	GaHrWorkExperience class of the ga_hr_employee module.	
	It represents objects of data type of work experience.
	Create the ga_hr_work_experience entity.
		
	:param _name: GaHrWorkExperience.
	:param _description: GaHrWorkExperience class of the ga_hr_employee module. It represents objects of data type of work experience.
	'''
	_name= 'ga.hr.work.experience'
	_description= 'Work experience of the employee'

	
	name_business= fields.Char('Name business',
								size=100,
	    						required=True,
	    						help="You must enter the name of the company in which the employee worked."
	    						)
	charge= fields.Char('Charge',
	    						size=100,
	    						required=True,
	    						help="You must enter the work position of the employee."
	    						)
	contact_name= fields.Char('Contact name',
								size=100,
	    						required=False,
	    						help="You must enter the name of the reference person to whom you can contact to confirm the information recorded."
	    						)
	phone_contact= fields.Char('Phone contact',
								size=12,
	    						required=False,
	    						help="You must enter the telephone number of the reference person you can contact to confirm the information recorded. You must enter only numeric characters."
	    						)
	salary_received= fields.Float('Salary received',
	    						required=False,
	    						help="You must enter the last salary received by the employee in the company."
	    						)
	admission_date= fields.Date('Admission_date',
	    						required=False
	    						)
	egress_date= fields.Date('Egress date',
	    						required=False
	    						)	
	years= fields.Integer('Years', 
								compute='_compute_years',								
								required=False,
								help="This field is automatically loaded when registering the date of entry and the date of departure to the company.",
								store=True
								)
	employee_id= fields.Many2one('hr.employee', 
								'Employee')
	
	@api.one
	@api.depends('admission_date', 'egress_date')
	def _compute_years(self):
		if self.admission_date and self.egress_date:			
			aDate = datetime.strptime(self.admission_date, OE_DFORMAT).date()
			eDate = datetime.strptime(self.egress_date, OE_DFORMAT).date()
			years = eDate.year - aDate.year - ((eDate.month, eDate.day) < (aDate.month, aDate.day))
			if years > 0:
				self.years = years
			else:
				self.years = 0

	@api.onchange('admission_date', 'egress_date')
	def _onchange_dates(self):
		if self.admission_date and self.egress_date and self.admission_date > self.egress_date:
			self.egress_date = ''
			error = {'title': 'Error en las fechas:',
			'message': 'La fecha de ingreso debe ser menor que la fecha de egreso.'
			}
			return {'warning': error}