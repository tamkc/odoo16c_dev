# -*- coding: utf-8 -*-
{
    "name": "hh_data",
    "category": "HungHing APP/",
    "summary": "Module to generate temporary demo data for Odoo.",
    "description": """
    HH Data
    =======
    This module is designed to facilitate the generation of temporary demo data within the Odoo environment.
    
    Features:
    ---------
    - Generate demo data for testing and development
    - Easy setup and configuration
    - Supports multiple data models
    
    Use Cases:
    ----------
    - Developers needing test data for new features
    - QA teams for testing various scenarios
    - Demonstrations and training sessions
    """,
    "author": "HungHing",
    "website": "http://www.yourcompany.com",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "installable": True,
    "application": True,
    "auto_install": False,
    "data": [
        "security/ir.model.access.csv",
        "views/demo_data_set.xml",
        "views/menu.xml",
        "data/field_type_data.xml",
        ]
}
