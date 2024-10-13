# Copyright 2023 CYSFuturo - Mario Arias
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Currency Rate Update: Costa Rican Electronic Billing",
    "version": "16.0.1",
    "category": "Financial Management/Configuration",
    "summary": "Update exchange rates using BCCR or Hacienda",
    "author": "CYSFuturo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/currency",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "application": False,
    "depends": [
        "currency_rate_update",
    ],
    'data': [
        'data/currency_data.xml',
        "views/res_currency_rate_provider.xml",
    ],
}
