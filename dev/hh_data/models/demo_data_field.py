# -*- coding: utf-8 -*-
# *************************************************************
# author  : Peter
# Date    : 2024-05-17
# project : Demo_data
#
# *************************************************************
from odoo import models, fields


class DemoDataField(models.Model):
    _name = 'hh_data.demo_data_field'
    _description = 'Demo Data Field'

    demo_data_set_id = fields.Many2one(
        'hh_data.demo_data_set', string='Demo Data Set', required=True, ondelete='cascade')
    name = fields.Char(string='Field Name', required=True)
    field_description = fields.Char(string='Field Description')
    field_type_id = fields.Many2one(
        'hh_data.field_type', string='Field Type')
    value = fields.Char(string='Value')
    min = fields.Float(string='Min')
    max = fields.Float(string='Max')
    decimals = fields.Integer(string='Decimals')
    
    is_required=fields.Boolean(string='Required')
