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

class GaHrObtainedTitle(models.Model):
	'''
	GaHrObtainedTitle class of the ga_hr_employee module.	
	It represents objects of data type of obtained title.
	Create the ga_hr_obtained_title entity.
		
	:param _name: GaHrObtainedTitle.
	:param _description: GaHrObtainedTitle class of the ga_hr_employee module. It represents objects of data type of obtained title.
	'''
	_name= 'ga.hr.obtained.title'
	_description= 'Obtained title'

	name= fields.Char('Title',
								size=100,
								required=True
								)
