# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo de Control de Acceso”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 20/12/2016
#moduleauthor: Rubén Garcia <garciara@guardiandelalba.pdvsa.com>

from openerp import models, fields, api
from datetime import datetime


class ga_ac_visitant_type(models.Model):
	_name= 'ga.ac.visitant.type'
	_description= 'Visitant type'
	_rec_name = 'type'
	type = fields.Char(string='Visitant type',
					size=60,
					required=True,
					help='Visitant type.')