#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Module of Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 01/10/2016
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api
from datetime import datetime

class GaHrCourses(models.Model):
	'''
	GaHrCourses class of the ga_hr_employee module.
	It represents objects of data type of courses name.
	Create the ga_hr_courses entity.
		
	:param _name: GaHrCourses.
	:param _description: GaHrCourses class of the ga_hr_employee module. It represents objects of data type of courses name.
	'''
	_name= 'ga.hr.courses'
	_description= 'Employee courses'

	name= fields.Char('Name',
								size=100,
								required=True
								)
