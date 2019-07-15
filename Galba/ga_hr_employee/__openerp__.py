
#-*- coding: utf-8 -*-


# This file is part of “Sistema de Gestión de Recursos Empresariales.
# Module of Gestión de Talento Humano”.
# Empresa Socialista de Capital Mixto Guardián del ALBA.

# created at 01/10/2016
# moduleauthor:: Yenny Bustamante <bustamanteye@guardiandelalba.pdvsa.com>

{
	'author': 'ESCM Guardián del ALBA.',
	'version': '1.0',
	'license': 'AGPL-3', 
	'name': 'Employee Directory',
	'category': 'Human Resources',
	'description': 'Module used to manage employee data.',
	'summary': 'Module used to manage employee data.',
	'depends': ['hr', 'hr_contract'],
	'application': True,	
	'data': [
        'views/ga_hr_employee.xml',
        'views/ga_hr_family.xml',
        'views/ga_hr_employee_courses.xml',
        'views/ga_hr_academic_formation.xml',
        'views/ga_hr_work_experience.xml',
        'views/ga_hr_employee_type.xml'    
    ],
	
}
