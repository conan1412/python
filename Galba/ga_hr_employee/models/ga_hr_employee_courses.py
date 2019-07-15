#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Module of Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 01/10/2016
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api, _
from datetime import datetime
from openerp import exceptions
from openerp.exceptions import except_orm
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

class GaHrEmployeeCourses(models.Model):
	'''
	GaHrEmployeeCourses class of the ga_hr_employee module.	
	It represents objects of data type of employee courses.
	Create the ga_hr_employee_courses entity.
		
	:param _name: GaHrEmployeeCourses.
	:param _description: GaHrEmployeeCourses class of the ga_hr_employee module. It represents objects of data type of employee courses.
	'''
	_name= 'ga.hr.employee.courses'
	_rec_name = 'courses_id'
	_description= 'Employee courses'
	
	start_date= fields.Date('Start date',
								required=False
								)
	end_date= fields.Date('End date',
								required=False
								)	
	number_hours= fields.Integer('Number hours',
								required=True
								)
	site= fields.Char('Site',
								size=100,
								required=False,
								help="You must enter the city or state where the employee did the course or workshop."
								)	
	employee_id= fields.Many2one('hr.employee', 
								'Employee')
	university_id= fields.Many2one('ga.hr.university',
								'University name')
	courses_id= fields.Many2one('ga.hr.courses', 
								'Certification name')

	@api.onchange('start_date', 'end_date')
	def _onchange_dates(self):
		if self.start_date and self.end_date and self.start_date > self.end_date:
			self.end_date = ''
			error = {'title': 'Error en las fechas:',
			'message': 'La fecha de inicio debe ser menor que la fecha de culminación.'
			}
			return {'warning': error}

