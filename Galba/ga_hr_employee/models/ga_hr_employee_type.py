#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Module of Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 13/01/2017
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api
from datetime import datetime

class GaHrEmployeeType(models.Model):
	'''
	GaHrEmployeeTypes class of the ga_hr_employee module.
	It represents objects of data type of employee type.
	Create the ga_hr_employee_type entity.
		
	:param _name: GaHrEmployeeType.
	:param _description: GaHrEmployeeType class of the ga_hr_employee module. It represents objects of data type of employee type.
	'''
	_name= 'ga.hr.employee.type'
	_description= 'Employee type'

	name= fields.Char('Name',
								size=100,
								required=True
								)
	code = fields.Char('Code', size=52, required=True)
	_sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         'The code must be unique.')]