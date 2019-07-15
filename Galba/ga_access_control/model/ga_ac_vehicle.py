# -*- encoding: utf-8 -*-

#This file is part of “Sistema de Gestión de Recursos Empresariales.
#Módulo de Control de Acceso”.
#Empresa Socialista de Capital Mixto Guardián del ALBA.

#created at 20/12/2016
#moduleauthor: Rubén Garcia <garciara@guardiandelalba.pdvsa.com>
#moduleauthor: Miguel Villamizar <villamizarm@guardiandelalba.com>

from openerp import models, fields, api, _
from openerp.osv import osv
from datetime import datetime

class ga_ac_vehicle(models.Model):
    _name= 'ga.ac.vehicle'
    _description= 'Vehicle visitant'
    _rec_name = 'license_plate'
    license_plate = fields.Char(string='License',
                    size=10,
                    help='License.', required=True,)
    color = fields.Char(string='Color',
                    size=20,
                    help='Color.',required=True,)
    type_model_id = fields.Many2one('ga.ac.type.model', "Model", required=True, select=True)
    visitant_id = fields.Many2one('ga.ac.visitant', "Visitant", required=False, select=True)
    employee_id = fields.Many2one('hr.employee', "Employee", select=True)

    #Create unique license_plate
    _sql_constraints = [('license_plate_uniq',
     'UNIQUE (license_plate)',
     'The license plate must be unique.')]

    #Validate in the moment to create a vehicle, first that assigned a person and second cannot assigned two person
    @api.model
    def create(self, vals):
        if(vals['employee_id'] == False and vals['visitant_id'] == False):
            raise osv.except_osv(_('Alert!!!'), _('Sorry, You can select a person'))
        if(vals['employee_id'] != False and vals['visitant_id'] != False):
            raise osv.except_osv(_('Alert!!!'), _('Sorry, You can only select a person for vehicle'))
        rec = super(ga_ac_vehicle, self).create(vals)
        return rec

    #Validate in the moment to modified a field that just only can selected a person
    @api.multi
    def write(self, vals):
        self.env.cr.execute("select employee_id, visitant_id from "+ self._table +" where id=%s", [self.id])
        res = self.env.cr.dictfetchall()
        if("employee_id" in vals and "visitant_id" not in vals):
                vals['visitant_id'] = res[0]['visitant_id']
        if("employee_id" not in vals and "visitant_id" in vals):
                vals['employee_id'] = res[0]['employee_id']

        if(vals['employee_id'] != False and vals['visitant_id'] != False):
            raise osv.except_osv(_('Alert!!!'), _('Sorry, You can only select a person for vehicle')) 
        rec = super(ga_ac_vehicle, self).write(vals)
        return rec