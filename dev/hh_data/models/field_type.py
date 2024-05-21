# -*- coding: utf-8 -*-
# *************************************************************
# author  : Peter
# Date    : 2024-05-17
# project : Demo_data
#
# *************************************************************
from odoo import models, fields


class DemoDataFieldType(models.Model):
    _name = 'hh_data.field_type'
    _description = 'Demo Data Field Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    odoo_field_type = fields.Char(
        string='Odoo Field Type', help="Corresponding Odoo field type (e.g., char, text, integer, etc.)")

    tag_color = fields.Integer(string='Tag Color')
