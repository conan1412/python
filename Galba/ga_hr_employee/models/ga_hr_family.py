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

class GaHrFamily(models.Model):
	'''
	GaHrFamily class of the ga_hr_employee module.	
	It represents objects of data type of employee family.
	Create the ga_hr_family entity.
		
	:param _name: GaHrFamily.
	:param _description: 	GaHrFamily class of the ga_hr_employee module. It represents objects of data type of employee family.
	'''
	_name= 'ga.hr.family'
	_rec_name = 'parentage'
	_description= 'Employee family'

	parentage= fields.Selection([
								('mother','Mother'),
								('father','Father'),
								('son','Son'),
								('partner','Partner'),
								],
								'Parentage',
								required=True
								)
	identification_number= fields.Char('Identification number',
								required=False,
								help="You must enter the family ID number. If you do not have an ID number enter the number 0. You only have to enter numeric characters."
								)
	family_name= fields.Char('First name',
								size=60,
								required=True
								)
	second_name= fields.Char('Second name',
								size=60,
								required=False
								)
	last_name_family= fields.Char('Last name',
								size=60,
								required=True
								)
	second_last_name_family= fields.Char('Second last name',
								size=60,
								required=False
								)
	birthday_family= fields.Date('Birthday',
								required=True
								)
			
	phone= fields.Char('Phone',
								size=12,
								required=False,
								help="You must enter the phone number of the family member by entering only numeric characters."
								)
	gender_family= fields.Selection([
								('feminine','Feminine'),
								('masculine','Masculine')
								
								], 
								'Gender',
								required=False
								)
	
	benefit_creche_family= fields.Boolean(
	    						string='Benefit creche',
	    						required=False,
	    						help="You must select this field if the familiar applies for this benefit and the employee has also consign the necessary requirements."
	    						)
	hcm_family= fields.Boolean(
	    						string='HCM',
	    						required=False,
	    						help="You must select this field if the familiar applies for this benefit and the employee has also consign the necessary requirements."
	    						)
	emergency_call= fields.Boolean(
	    						string='Emergency call',
	    						required=False
	    						)
	scholarship_family= fields.Boolean(
	    						string='Scholarship',
	    						required=False,
	    						help="You must select this field if the familiar applies for this benefit and the employee has also consign the necessary requirements."
	    						)
	school_tools_family= fields.Boolean('School tools',
	    						required=False,
	    						help="You must select this field if the familiar applies for this benefit and the employee has also consign the necessary requirements."
	    						)
	disability_family= fields.Boolean('Disability allowance',
	    						required=False,
	    						help="You must select this field if the familiar applies for this benefit and the employee has also consign the necessary requirements."
	    						)
	
	impairment= fields.Boolean('Has disability',
	    						required=False
	    						)

	impairment_type= fields.Char('Impairment type',
								size=50,
								required=False
								)
	employee_id= fields.Many2one('hr.employee', 
								'Family')
	country_id = fields.Many2one('res.country', 'Country of birth')
	
	age = fields.Integer('Age',        						
        						compute='_compute_age',
        						required=False,
        						help="This field is automatically loaded when registering the familiar's birth date.",
        						store=False
        						)

	@api.one
	@api.depends('birthday_family')
	def _compute_age(self):
		if self.birthday_family:
			dBday = datetime.strptime(self.birthday_family, OE_DFORMAT).date()
			dToday = datetime.now().date()
			age = dToday.year - dBday.year - ((dToday.month, dToday.day) < (dBday.month, dBday.day))
			if age > 0:
				self.age = age
			else:
				self.age = 0	

	@api.onchange('birthday_family')
	def _onchange_birthday_family(self):
		if self.birthday_family:
			dateBirthday = datetime.strptime(self.birthday_family, OE_DFORMAT).date()
			dateToday = datetime.now().date()
			if dateBirthday > dateToday:
				self.birthday_family = ''
				error = {'title': 'Error en el campo fecha de nacimiento:',
				'message': 'La fecha de nacimiento debe ser menor o igual que la fecha actual.'
				}
				return {'warning': error}

	@api.onchange('identification_number')
	def _onchange_identificaction_number(self):
		identificacionNumber = self.identification_number
		if identificacionNumber and not(identificacionNumber.isdigit()):
			self.identification_number = ''
			error = {'title': 'Error en el campo cédula de identidad:',
			'message': 'La cédula de identidad debe contener sólo caracteres numéricos. Ej. 12345678'
			}
			return {'warning': error}