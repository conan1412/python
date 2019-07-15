# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo de Control de Acceso”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 20/12/2016
#moduleauthor: Rubén Garcia <garciara@guardiandelalba.pdvsa.com>

from openerp import models, fields, api
from datetime import datetime

class ga_ac_mark(models.Model):
    _name= 'ga.ac.mark'
    _description= 'Mark'
    mark = fields.Char(string='Mark',
                    size=100,
                    required=True,
                    help='Mark.')