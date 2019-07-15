#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Módulo de Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 01/10/2016
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api
from datetime import datetime


class GaHrEmployeeCoursesUniversity(models.Model):
	'''
	GaHrEmployeeCoursesUniversity class of the ga_hr module.	
	It represents objects of data type of employee courses university.
	Create the ga_hr_employee_courses_university entity.
		
	:param _name: GaHrEmployeeCoursesUniversity.
	:param _description: GaHrEmployeeCoursesUniversity class of the ga_hr module. It represents objects of data type of employee courses university.
	'''
	_name= 'ga.hr.employee_courses_university'
	_description= 'Employee courses university'
	_inherits = {
				'hr.employee': 'employee_id',				
				'ga.hr.courses': 'courses_id',
				'ga.hr.university': 'university_id'}	

	
	start_date= fields.Date('Start date',
								required=True,
								help='Start date')
	end_date= fields.Date('End date',
								required=True,
								help='End date')	
	number_hours= fields.Integer('Number hours',
								required=True,
								help='Number hours')
	site= fields.Char('Site',
								size=100,
								required=True,
								help='Site')
	courses_id= fields.Many2one('ga.hr.courses', 
								'Employee courses university')
	employee_id= fields.Many2one('hr.employee', 
								'Employee courses university')
	university_id= fields.Many2one('ga.hr.university',
								'Employee courses university')




