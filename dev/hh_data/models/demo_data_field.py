# -*- coding: utf-8 -*-
# *************************************************************
# author  : Peter
# Date    : 2024-05-17
# project : Demo_data
#
# *************************************************************
from odoo import models, fields, api
from datetime import datetime, timedelta


class DemoDataField(models.Model):
    _name = 'hh_data.demo_data_field'
    _description = 'Demo Data Field'

    def _default_date_from(self):
        # Get the current date
        today = datetime.now()
        # Calculate the date exactly one year before today
        return today - timedelta(days=365)

    def _default_date_to(self):
        # Return today's date
        return datetime.now()

    demo_data_set_id = fields.Many2one(
        'hh_data.demo_data_set', string='Demo Data Set', ondelete='cascade')
    name = fields.Char(string='Field Name', required=True)
    field_description = fields.Char(string='Field Description')
    field_type_id = fields.Many2one(
        'hh_data.field_type', string='Type')

    # ---------------------------- DateTime Interface ---------------------------- #
    date_from = fields.Datetime(
        string='Datetime From', default=_default_date_from)
    # Approximately 23:59 in 24-hour format
    date_to = fields.Datetime(string='Datetime To', default=_default_date_to)

    # ----------------------------- Common Interface ----------------------------- #
    is_required = fields.Boolean(string='Required')
    value = fields.Text(string='Value')

    # ------------------------------ Float Interface ----------------------------- #
    min = fields.Float(string='Min')
    max = fields.Float(string='Max')
    decimals = fields.Integer(string='Decimals')

    # ---------------------------- Many2one Interface ---------------------------- #
    relation = fields.Char(string='Model', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        field_type_model = self.env['hh_data.field_type']
        for vals in vals_list:
            field_type = field_type_model.browse(vals.get('field_type_id'))
            if field_type:
                if field_type.odoo_field_type == 'text':
                    vals['value'] = 'Default Text'
                elif field_type.odoo_field_type in ['integer', 'monetary']:
                    vals['min'] = 0
                    vals['max'] = 1000
                elif field_type.odoo_field_type == 'float':
                    vals['min'] = 0
                    vals['max'] = 1000
                    vals['decimals'] = 2
                elif field_type.odoo_field_type == 'json':
                    vals['value'] = '{"default_key": "default_value"}'
                elif field_type.odoo_field_type == 'html':
                    vals['value'] = '<p>Default HTML Content</p>'
                elif field_type.odoo_field_type == 'char':
                    vals['value'] = 'Default Char'

        return super(DemoDataField, self).create(vals_list)

    def get_field_configuration(self):
        field_type = self.field_type_id.odoo_field_type

        config = {
            'name': self.name,
            'type': field_type,
            'is_required': self.is_required,
        }

        if field_type in {'date', 'datetime'}:
            config['date_from'] = self.date_from
            config['date_to'] = self.date_to
        elif field_type in {'float', 'integer', 'monetary'}:
            config['min'] = self.min
            config['max'] = self.max
            config['decimals'] = self.decimals
        elif field_type == 'many2one':
            config['relation'] = self.relation
            config['domain'] = self.value
        elif field_type in {'char', 'text', 'html', 'json'}:
            config['value'] = self.value

        return config
