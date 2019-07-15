
#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Module of Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 03/10/2016
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api, _
from datetime import datetime
from openerp import exceptions
from openerp.exceptions import except_orm
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT


class GaHrAcademicFormation(models.Model):
	'''
	GaHrAcademicFormation class of the ga_hr_employee module.	
	It represents objects of data type of academic formation.
	Create the ga_hr_academic_formation entity.
		
	:param _name: GaHrAcademicFormation.
	:param _description: GaHrAcademicFormation class of the ga_hr_employee module. It represents objects of data type of academic formation.
	'''
	_name= 'ga.hr.academic.formation'
	_rec_name = 'obtained_title_id'	
	_description= 'Academic formation of the employee'

	education_level= fields.Selection([
								('primary_school','Primary school'),
								('high_school','High school'),
								('post_secondary1','Post secondary 1'),
								('post_secondary2','Post secondary 2'),
								('post_secondary3','Post secondary 3'),
								('post_secondary4','Post secondary 4'),
								('post_secondary5','Post secondary 5'),
								('post_secondary6','Post secondary 6'),
								], 
								'Education level',
								required=True
								)
	educational_branch= fields.Char('Branch educational',
								size=50,
								required=False
								)
	admission_date=fields.Date('Admission date',
								required=False
								)
	egress_date=fields.Date('Egress date',
								required=False
								)
	university_id= fields.Many2one('ga.hr.university',
								'University name')
	obtained_title_id= fields.Many2one('ga.hr.obtained.title', 
								'Obtained title')
	employee_id= fields.Many2one('hr.employee', 
								'Employee')

	
	@api.onchange('admission_date', 'egress_date')
	def _onchange_dates(self):
		if self.admission_date and self.egress_date and self.admission_date > self.egress_date:
			self.egress_date = ''
			error = {'title': 'Error en las fechas:',
			'message': 'La fecha de ingreso debe ser menor que la fecha de egreso.'
			}
			return {'warning': error}