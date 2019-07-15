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

class GaHrUniversity(models.Model):
	'''
	GaHrUniversity class of the ga_hr_employee module.	
	It represents objects of data type of university name.
	Create the ga_hr_university entity.
		
	:param _name: GaHrUniversity.
	:param _description: GaHrUniversity class of the ga_hr_employee module. It represents objects of data type of university name.
	'''
	_name= 'ga.hr.university'
	_description= 'University'

	name= fields.Char('University',
								size=100,
								required=True
								)
	
