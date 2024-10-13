# -*- coding: utf-8 -*-
from odoo import models, fields, api

element_status = [('OtroTexto', 'OtroTexto'), ('OtroContenido', 'OtroContenido')]

class fe_special_tags_invoice_line(models.Model):
    _name = 'fe.special.tags.invoice.line'
    code = fields.Char('Código Técnico')
    content = fields.Char('Contenido')
    content_label = fields.Char('Campo / Ayuda')
    element = fields.Selection(element_status, 'Elemento')
    invoice_id = fields.Many2one('account.move', string='Factura')
    python_code = fields.Text('Codigo Python')
    read_only = fields.Boolean('Solo lectura')
    read_only_content = fields.Boolean('Solo lectura (Contenido)')
    rel_id = fields.Integer('Id de special tags')
    required = fields.Boolean('Requerido')
    type_add = fields.Char('Tipo de agregado de linea')


class fe_special_tags_partner_line(models.Model):
    _name = 'fe.special.tags.partner.line'
    code = fields.Char('Código Técnico')
    content = fields.Char('Contenido')
    content_label = fields.Char('Nombre a mostrar / Ayuda')
    element = fields.Selection(element_status, 'Elemento')
    partner_id = fields.Many2one('res.partner', string='Contacto')
    python_code = fields.Text('Codigo Python')
    read_only = fields.Boolean('Solo lectura (Elemento y Código Técnico)')
    read_only_content = fields.Boolean('Solo lectura (Contenido)')
    required = fields.Boolean('Requerido (Contenido)')
    state = fields.Selection(element_status, 'Elemento')


class fe_special_tags_company_line(models.Model):
    _name = 'fe.special.tags.company.line'
    code = fields.Char('Código Técnico')
    company_id = fields.Many2one('res.company', string='Conpania')
    content = fields.Char('Contenido')
    content_label = fields.Char('Nombre a mostrar / Ayuda')
    element = fields.Selection(element_status, 'Elemento')
    python_code = fields.Text('Codigo Python')
    read_only = fields.Boolean('Solo lectura (Elemento y Código Técnico)')
    read_only_content = fields.Boolean('Solo lectura (Contenido)')
    required = fields.Boolean('Requerido (Contenido)')
    state = fields.Selection(element_status, 'Elemento')


class ResPartnerSpecialTags(models.Model):
    _inherit = 'res.partner'

    special_tags_lines = fields.One2many('fe.special.tags.partner.line', 'partner_id',
                                         string='Líneas de etiquetas adicionales XML')

class ResCompanySpecialTags(models.Model):
    _inherit = 'res.company'
    special_tags_lines = fields.One2many('fe.special.tags.company.line', 'company_id',
                                         string='Líneas de etiquetas adicionales XML')



class AccountMoveSpecialTagsLines(models.Model):
    _inherit = 'account.move'

    special_tags_lines = fields.One2many('fe.special.tags.invoice.line', 'invoice_id',
                                         string='Líneas de etiquetas adicionales XML')

