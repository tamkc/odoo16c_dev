# -*- coding: utf-8 -*-
# *************************************************************
# author  : Peter
# Date    : 2024-05-17
# project : Demo_data
#
# *************************************************************
from odoo import models, fields, api, _


class DemoDataSet(models.Model):
    _name = 'hh_data.demo_data_set'
    _description = 'Temporary Demo Data'

    name = fields.Char(string='Name', required=True,
                       default='Demo Data Set {}'.format(fields.Datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    description = fields.Text(string='Description')
    model_id = fields.Many2one(
        'ir.model', string='Model', required=True, ondelete='cascade')
    exclude_fields = fields.Text(string='Exclude Fields',
                                 default='id,create_date,write_date,create_uid,write_uid,__last_update', help='Comma-separated list of field names to exclude')

    data_field_ids = fields.One2many(
        'hh_data.demo_data_field', 'demo_data_set_id', string='Data Fields')

    ignore_field_types_ids = fields.Many2many(
        'hh_data.field_type',
        'demo_data_set_ignore_field_type_rel',
        'demo_data_set_id',
        'field_type_id',
        string='Ignore Field Types',
        help='Select field types to ignore',
        default=lambda self: self._default_ignore_field_types()
    )

    number_of_rows = fields.Integer(string='Number of Rows', default=1000)
    export_format = fields.Selection(
        [('csv', 'CSV'), ('json', 'JSON')], default='csv')
    include_header = fields.Boolean(string='Include Header')

    @api.model
    def _default_ignore_field_types(self):
        # Fetch field type ids where odoo_field_type is 'binary'
        field_type_ids = self.env['hh_data.field_type'].search(
            [('odoo_field_type', '=', 'binary')])
        return [(6, 0, field_type_ids.ids)]

    @api.onchange('model_id', 'exclude_fields', 'ignore_field_types_ids')
    def _onchange_model_id(self):
        """Fetch and create lines for the fields of the selected model
        This will also take into account the exclude_fields field and ignore field types already in ignore_field_types_ids.
        """
        if not self.model_id:
            return
        self.data_field_ids = [(5, 0, 0)]  # Clear existing lines
        model_obj = self.env[self.model_id.model]
        fields_info = model_obj.fields_get()
        excluded_fields = [
            field.strip() for field in self.exclude_fields.split(',') if field.strip()]
        ignore_field_types = self.ignore_field_types_ids.mapped(
            'odoo_field_type')

        data_fields = []

        # Create lines for fields
        for field_name, field_info in fields_info.items():
            # Skip excluded fields
            if field_name in excluded_fields:
                continue

            # Skip excluded field types
            if field_info['type'] in ignore_field_types:
                continue

            # Skip one2many, many2many, or many2one_reference fields
            if field_info['type'] in ['one2many', 'many2many', 'many2one_reference']:
                continue

            # Skip fields with 'depends' attribute
            if not field_info.get('depends'):
                continue

            field_type_record = self.env['hh_data.field_type'].search(
                [('odoo_field_type', '=', field_info['type'])], limit=1)

            field_type_id = field_type_record.id if field_type_record else False
            data_fields.append((0, 0, {
                'name': field_name,
                'field_description': field_info.get('string'),
                'field_type_id': field_type_id,
                'is_required': field_info.get('required'),
                'relation': field_info.get('relation') or self.model_id.model,
                'value': field_info.get('domain') or field_info.get('selection'),
            }))

        self.data_field_ids = data_fields

    def generate_data(self) -> str:

        # Print the generated CSV content
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/demo_data/export/csv?model={self._name}&id={self.id}',
            'target': 'new',
        }

    def get_fields_config(self) -> list:
        """
        Returns a list of configuration dictionaries for the fields of this demo data set.

        :return: List of configuration dictionaries.
        """
        data_fields = self.data_field_ids or []  # Check for null pointer references
        return [field.get_field_configuration() for field in data_fields]
