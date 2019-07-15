#-*- coding: utf-8 -*-
'''

This file is part of “Sistema de Gestión de Recursos Empresariales.
Module of Gestión de Talento Humano”.
Empresa Socialista de Capital Mixto Guardián del ALBA.

created at 01/12/2016
moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>
'''

from openerp import models, fields, api
from datetime import datetime

class GaHrDeductions(models.Model):
	'''
	GaHrDeductions class of the ga_hr_employee module.	
	It represents objects of data type of deductions.
	Create the ga_hr_deductions entity.
		
	:param _name: GaDeductions.
	:param _description: GaHrDeductions class of the ga_hr_employee module. It represents objects of data type of deductions.
	'''
	_name= 'ga.hr.deductions'
	_description= 'Deductions of the employee'

	
	maintenance= fields.Boolean('Maintenance',
	    						required=False,
	    						help="You must select this field if the employee applies to comply with this obligation."
	    						)
	amount_type= fields.Selection([
								('Porcentage','%'),
								('Fixed','Fixed'),
								],
								'Amount type',
								required=False
								)
	amount= fields.Float('Amount',
	    						required=False,
	    						help="You must enter the amount or percentage as appropriate with the type of amount selected, using only numeric characters."
	    						)
	saving_box= fields.Integer('Saving box',
	    						required=False,
	    						help="You must enter the percentage defined by the employee to be deducted from your salary by concept of the saving box. You must only enter numeric characters."
	    						)
	credit= fields.Integer('Credit',
	    						required=False,
	    						help="You must enter the percentage defined by the employee to be deducted from your salary by concept of the saving box credit. You must only enter numeric characters."
	    						)
	loan= fields.Integer('Loan',
	    						required=False,
	    						help="You must enter the percentage defined by the employee to be deducted from your salary by concept of the saving box loan. You must only enter numeric characters."
	    						)
	income_tax= fields.Integer('Income tax',
	    						required=False,
	    						help="You must enter the percentage defined by the employee to be deducted from your salary by concept of the  Income Tax. Apply under the instructions specified by the Tax Administration. It is a percentage field so you should only enter numeric characters."
	    						)
	syndicate= fields.Integer('Syndicate',
	    						required=False,
	    						help="You must enter the percentage defined by the employee to be deducted from your salary by concept of the syndicate. You must only enter numeric characters."
	    						)
	employee_id= fields.Many2one('hr.employee', 
								'Employee')
