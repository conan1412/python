# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo Galba Web Login Screen”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 15/11/2016
#moduleauthor:: Edison Molina <molinae@guardiandelalba.pdvsa.com>

{
    "name": "HR Employee Last Name",
    "version": "8.0",
    "author": "ESCM Guardian del ALBA",
    "category": "hr",
    "website": "",
    "license": "AGPL-3",
    "depends": [
        "ga_hr_employee",
    ],
    "test": [
        "test/test_employee.yml",
    ],
    "demo": [
        "demo/hr_employee.xml",
    ],
    "data": [
        "view/hr_employee_view.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': True
}
