# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo de Control de Acceso”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 20/12/2016
#moduleauthor: Rubén Garcia <garciara@guardiandelalba.pdvsa.com>
#moduleauthor: Miguel Villamizar <villamizarm@guardiandelalba.com>

from openerp import models, fields, api, tools
from datetime import datetime
from openerp.modules.module import get_module_resource

class ga_ac_visitant(models.Model):
    _name = 'ga.ac.visitant'
    _description = 'Visitant'
    _rec_name = 'full_name'

    identification_number = fields.Integer(string='Identification Id', required=True,)

    full_name = fields.Char(
        string='Full name', size=80, compute='_defined_full_name',
        store=False, required=True, search="_search_full_name"
    )

    name_visitant = fields.Char(string='Name',
                    size=60,
                    required=True,
                    help='Visitant.')

    surname_visitant = fields.Char(string='Surname',size=60,
                    required=True)

    telephone_mobile = fields.Char(string='Telephone',
                size=12,
                help='telephone mobile.')

    country_id = fields.Many2one('res.country')

    visitant_type_id = fields.Many2one('ga.ac.visitant.type', required=True,)
    
    image_medium = fields.Binary('Image')

    #assigned a default image for to create a visitant
    def _get_default_image(self, cr, uid, context=None):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_medium(open(image_path, 'rb').read().encode('base64'))

    #Create unique identification number
    _sql_constraints = [('identification_number_uniq',
        'UNIQUE (identification_number)',
        'The identification id number must be unique.')]

    #For moment to create a record to the image to resize
    @api.model
    def create(self, vals):
        vals['image_medium'] = tools.image_resize_image_medium(vals['image_medium'])
        rec = super(ga_ac_visitant, self).create(vals)
        return rec

    #Define to defaults values in the new record
    _defaults = {
        'country_id': 240,
        'image_medium': _get_default_image,
        'identification_number': None,
    }
    
    #Define the full name for the visitant
    @api.one
    @api.depends('name_visitant','surname_visitant')
    def _defined_full_name(self):
        self.full_name = (self.surname_visitant or '') + ' ' + (self.name_visitant or '')

    #Define the search a compute field
    @api.one
    @api.depends('name_visitant','surname_visitant')
    def _search_full_name(self,operator,value):
        return ['|',('name_visitant',operator,value),('surname_visitant',operator,value)]