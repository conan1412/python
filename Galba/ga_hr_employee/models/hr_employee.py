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

class HrEmployee(models.Model):
	'''
	HrEmployee class of the ga_hr_employee module.
	It represents objects of employee data type.
	Inherited by extension from hr.employee model.
	Add and modify fields to the hr_employee entity.

	:param _name: HrEmployee.
	:param _description: Employee class of the ga_hr_employee module. It represents objects of employee data type.
	'''

	_inherit = 'hr.employee'	    
	_description = 'Employee'

	# Inheritance by delegation
	_inherits = {'ga.hr.contributions.benefits': 'contributions_benefits_id',
				'ga.hr.deductions': 'deductions_id'}
	contributions_benefits_id = fields.Many2one('ga.hr.contributions.benefits', 'Contributions and Benefits', ondelete='cascade', required=True, auto_join=True)
	deductions_id = fields.Many2one('ga.hr.deductions', 'Deductions', ondelete='cascade', required=True, auto_join=True)
	extension= fields.Integer('Extension',
								help='You must enter only numeric characters.')
	years_service= fields.Integer('Service years', 
								compute='_compute_service_years',
								help="This field is automatically loaded by recording the date of entry pertaining to the employee's contract.",
								store=False
								)
	external_years_experience= fields.Integer('External experience years'
								)	
	assigned_to= fields.Char('Assigned to',
								size=100,
								help='You must enter the name of the company to which this employee was assigned.')
	assigned_from= fields.Char('Assigned from',
								size=100,
								help='You must enter the name of the company from which this employee comes.')
	seconded_labor_union= fields.Boolean('Seconded labor union')
	name_labor_union= fields.Char('Labor union name',
								size=100)

	cost_center= fields.Integer('Cost center',
								required=True)
	email= fields.Char('Email',
								size=100,
								help="You must enter the employee's personal email.")
	shirt_size= fields.Selection([
								('ss','SS'),
								('s','S'),
								('m','M'),
								('l','L'),
								('xl', 'XL'),
								('xxl', 'XXL'),
								('xxxl', 'XXXL')
								],
								'Shirt')
	pants_size= fields.Selection([
								('26','26'),
								('28','28'),
								('30','30'),
								('32','32'),
								('34','34'),
								('36','36'),
								('38','38'),
								('40','40'),
								('42','42'),
								('44','44'),
								('46','46'),
								('48','48'),
								('50','50'),								
								],
								'Pants')
	braga_size= fields.Selection([
								('ss', 'SS'),
								('s', 'S'),
								('m', 'M'),
								('l', 'L'),
								('xl', 'XL'),
								('xxl', 'XXL'),
								('xxxl', 'XXXL')
								], 
								'Braga')
	boots_size= fields.Selection([
								('34','34'),
								('35','35'),
								('36','36'),
								('37','37'),
								('38','38'),
								('39','39'),
								('40','40'),
								('41','41'),
								('42','42'),
								('43','43'),
								('44','44'),
								('46','46'),
								('48','48'),
								('50','50'),
								],
								'Boots')
	have_vehicle= fields.Boolean(string='Have vehicle')
	laterality_type= fields.Selection([
								('left_hand','Left hand'),
								('right_hand','Right hand')
								],
								'Laterality type')
	impairment= fields.Boolean(string='Has disability')

	impairment_type= fields.Char('Impairment type',
								size=50)

	description_activities= fields.Text(
							   	'Description activities')
	employee_type_id=fields.Many2one('ga.hr.employee.type', 'Employee type')

	# Edited fields
	gender= fields.Selection([								
								('feminine','Feminine'),
								('masculine','Masculine')
								], 
								'Gender',
								required=False,
								)
	birthday= fields.Date(required=False)

	_sql_constraints = [
        ('identification_id_uniq',
         'UNIQUE (identification_id)',
         'The identificationid number must be unique.')]


	# Inverse relationship
	academic_formation_ids= fields.One2many('ga.hr.academic.formation',
                            'employee_id',
                            'Academic formation of employee')
	courses_ids= fields.One2many('ga.hr.employee.courses',
                            'employee_id',
                            'Employee courses')
	work_experience_ids= fields.One2many('ga.hr.work.experience',
                            'employee_id',
                            'Work experience')
	family_ids= fields.One2many('ga.hr.family',
                            'employee_id',
                            'Employee families')
	contract_ids= fields.One2many('hr.contract',
                            'employee_id',
                            'Contract')
	

	# It is used to calculate years of service. 
	# The employee can have several contracts, each contract has start date and end date.
	# For the contract that does not have an end date, the end date is equal to the current date. 
	# Accumulate the days of all contracts and divide them between 365 to convert them to years.
	@api.multi
	@api.depends('contract_ids.date_start', 'contract_ids.date_end')
	def _compute_service_years(self):
		employee_contracts= self.env['hr.contract'].search([('employee_id','=',self.id)])
		daysService = 0
		if employee_contracts:
			for employee_contract in employee_contracts:
				dStart = employee_contract.date_start
				dEnd = employee_contract.date_end
				today = datetime.now().date()
				if dStart:					
					dStart = datetime.strptime(dStart, OE_DFORMAT).date()
					if dEnd:
						dEnd = datetime.strptime(dEnd, OE_DFORMAT).date()
						if dEnd > today:
	 						dEnd = today
					else:
						dEnd = today
					diff = dEnd - dStart
					if diff.days > 0:
						daysService += diff.days
		self.years_service = daysService/365
	
	@api.model
	def _set_default_value_country_id(self):
		# Search default value
		country_obj= self.env['res.country'].search([('code','=','VE')], limit=1)		
		if country_obj:
			return country_obj[0].id
		return False
		
	_defaults = {
	'country_id': _set_default_value_country_id,	
	}

	@api.constrains('identification_id')
	def _check_identificaction_id(self):	
		identificacionNumber = self.identification_id
		if identificacionNumber and not(identificacionNumber.isdigit()):
			self.identification_id = ''
			raise except_orm('Error en el campo cédula de identidad:',
							'La cédula de identidad debe contener sólo caracteres numéricos. Ej. 12345678')
				
	@api.onchange('identification_id')
	def _onchange_identificaction_id(self):
		identificacionNumber = self.identification_id
		if identificacionNumber and not(identificacionNumber.isdigit()):
			self.identification_id = ''
			error = {'title': 'Error en el campo cédula de identidad:',
			'message': 'La cédula de identidad debe contener sólo caracteres numéricos. Ej. 12345678'
			}
			return {'warning': error}			
				
	@api.onchange('birthday')
	def _onchange_birthday(self):
		if self.birthday:
			dateBirthday = datetime.strptime(self.birthday, OE_DFORMAT).date()
			dateToday = datetime.now().date()
			if dateBirthday > dateToday:
				self.birthday = ''
				error = {'title': 'Error en el campo fecha de nacimiento:',
				'message': 'La fecha de nacimiento debe ser menor o igual que la fecha actual.'
				}
				return {'warning': error}

	def total_paid_amount_of_salary_rule(self,employee_id,code_of_payslip_type,code_of_salary_rule,date_from,date_to):		
		
		total = 0
		
		if employee_id and code_of_payslip_type and code_of_salary_rule:

			# Object that is used to obtain the payroll id with code code_of_payslip_type
			payslipType = self.env['ga.hr.payslip.type'].search([('code','=',code_of_payslip_type)])
						
			if payslipType:	
				# Object that is used to obtain payslipType type payrolls paid to the employee during the dateFrom and dateTo dates						
				payslips =  self.env['hr.payslip'].search([('employee_id','=',employee_id),('payslip_type_id','=',payslipType.id),('date_from','>=',date_from),('date_to','<=',date_to),('state','=','done')])
				
				if payslips:	
					for payslip in payslips:
						 
						# Object that is used to obtain the paid amount of the payroll corresponding to the salary rule code_of_salary_rule
						paid_amount_of_salary_rule = self.env['hr.payslip.line'].search([('slip_id','=',payslip.id),('code','=',code_of_salary_rule)])		
					
						if paid_amount_of_salary_rule:								
							total = total + paid_amount_of_salary_rule.total
			
		return total

		
	def is_trimester_of_pay_of_social_benefits(self, contract, payslip_date_to):				
		
		isTrimesterOfPay = 0

		if contract and payslip_date_to:				
			startDateOfContract = datetime.strptime(contract.date_start, OE_DFORMAT).date()
			dateEndOfPayslip = datetime.strptime(payslip_date_to, OE_DFORMAT).date()
			
			dateIterator = startDateOfContract
			monthIterator = startDateOfContract.month
			yearIterator = startDateOfContract.year			
			stopDate= dateEndOfPayslip.replace(day = startDateOfContract.day)		

			while True:
				if(startDateOfContract == dateIterator):
					monthIterator += 2
				else:
					monthIterator += 3										
				if monthIterator > 12:
					monthIterator -= 12
					yearIterator += 1				
				dateIterator = dateIterator.replace(year = yearIterator,month = monthIterator)

				# Thi if is used to simulate a "do while" in python
				if(dateIterator >= stopDate):
					break

			if(dateIterator.month == stopDate.month):
				isTrimesterOfPay = 1				

		return isTrimesterOfPay


