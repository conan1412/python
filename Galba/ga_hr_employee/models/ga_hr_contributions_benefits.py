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

class GaHrContributionsBenefits(models.Model):
	'''
	GaHrContributionsBenefits class of the ga_hr_employee module.	
	It represents objects of data type of contributions and benefits.
	Create the ga_hr_contributions_benefits entity.
		
	:param _name: GaHrContributionsBenefits.
	:param _description: GaHrContributionsBenefits class of the ga_hr_employee module. It represents objects of data type of contributions and benefits.
	'''
	_name= 'ga.hr.contributions.benefits'
	_description= 'Contributions and benefits of the employee'
	
	hcm= fields.Boolean('HCM',
	    						required=False,
	    						help="You must select this field if the employee applies for this benefit and has also entered the necessary requirements."
	    						)
	scholarship= fields.Boolean('Scholarship',
	    						required=False,
	    						help="You must select this field if the employee applies for this benefit and has also entered the necessary requirements."
	    						)
	school_tools= fields.Boolean('School tools',
	    						required=False,
	    						help="You must select this field if the employee applies for this benefit and has also entered the necessary requirements."
	    						)
	assignment_disability= fields.Boolean('Disability allowance',
	    						required=False,
	    						help="You must select this field if the employee applies for this benefit and has also entered the necessary requirements."
	    						)
	economic_support= fields.Boolean('Economic support',
	    						required=False,
	    						help="You must select this field if the employee applies for this benefit and has also entered the necessary requirements."
	    						)
	employee_id= fields.Many2one('hr.employee', 
								'Employee')