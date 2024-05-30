# -*- coding: utf-8 -*-
# *************************************************************
# author  : Peter
# Date    : 2024-05-28
# project : Demo_data
#
# *************************************************************

from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval, test_python_expr, wrap_module
import random
from faker import Faker
fake = Faker()


class DemoDataTemplate(models.Model):
    _name = 'hh_data.template'
    _description = 'Demo Data Template'

    type = fields.Selection([
        ('custom_list', 'Custom List'),
        ('code', 'code'),
    ])

    item_list = fields.Char(string='Item List', default='item1,item2,item3')

    code = fields.Text(string='Python Code',
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.",
                       default="random.choice(self.item_list.split(','))"
                       )

    preview_data_limit = fields.Integer(
        string='Number of Data to Preview', default=10)
    preview = fields.Text(string='Preview', readonly=True)
    is_tested = fields.Text(string='Test', readonly=True)

    template_type = fields.Selection([
        ('custom_list', 'Custom List'),
        ('code', 'Python Code'),
    ], default='custom_list')

    name_search_key = fields.Char(
        string='Search Key', help="used to match template")

    @api.onchange('template_type')
    def onchange_template_type(self):
        if self.template_type == 'custom_list':
            self.code = "random.choice(self.item_list.split(','))"
        else:
            self.code = ""

    def preview_data(self):
        for record in self:
            try:
                code = record.code.strip()
                # Define the context in which `exec` will run
                exec_globals = {'fake': fake, 'random': random, 'self': self}
                results = []

                # Generate the specified number of results
                for _ in range(record.preview_data_limit):
                    exec_code = f"result = {code}"
                    exec(exec_code, exec_globals)
                    results.append(exec_globals['result'])

                # Store the results in the record.preview
                record.preview = results
            except Exception as e:
                record.preview = f"Error: {str(e)}"
