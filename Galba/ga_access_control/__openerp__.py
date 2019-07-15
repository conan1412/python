# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo Galba Web Login Screen”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 21/11/2016
#moduleauthor: Yesenia Morales <ymorales@guardiandelalba.pdvsa.com>
#moduleauthor: Osvaldo López <olopez@guardiandelalba.pdvsa.com>
#moduleauthor: Rubén Garcia
#
{
	'name': 'Access Control PDVSA/PDVSA-INDUSTRIAL',
	'description': 'Resources Humans Module',
	'author': 'ESCM Guardián del ALBA.',
	'sequence': 2,
	'depends': ['hr_attendance',
				'ga_hr_employee',
				'ga_hr_lastname'],
	'data' : ['view/layouts.xml',
			'view/ga_ac.xml',
			'view/ga_ac_configuartion.xml',
			'view/ga_ac_view.xml',
			'view/ga_ac_visitant_view.xml',
			'view/ga_ac_vehicle_view.xml',
			'report/ga_ac_report.xml',
			'report/ga_ac_general_report.xml',
			'report/ga_ac_visitant_report.xml',
			'report/call_ac_general_report.xml',
			'wizard/ga_ac_general_wizard.xml',
			'wizard/ga_ac_visitant_wizard.xml',
			'wizard/ga_ac_wizard.xml',
			],
	'application': True,
	'sumary': 'Module for the registration and control of the access of employees and visitors to installations of companies of the petroleum industry',
	'category': 'Resources Humans'
}