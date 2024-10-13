from unittest.result import failfast
from odoo import models, fields, api, _

class AccountTaxTemplate(models.Model):
    _inherit = "account.tax.template"

    # ==============================================================================================
    #                                          ACCOUNT TAX TEMPLATE
    # ==============================================================================================

    tax_code = fields.Char(
        string="Tax Code"
    )
    iva_tax_desc = fields.Char(
        string="VAT Tax Rate",
        default='N/A'
    )
    iva_tax_code = fields.Char(
        string="VAT Rate Code",
        default='N/A'
    )
    non_tax_deductible = fields.Boolean(
        string='Indicates if this tax is no deductible for Rent and VAT'
    )

    def _get_tax_vals(self, company, tax_template_to_tax):
        """ This method generates a dictionary of all the values for the tax that will be created.
        """
        val = super(AccountTaxTemplate, self)._get_tax_vals(company, tax_template_to_tax)

        if self.tax_code:
            val['tax_code'] = self.tax_code
        if self.iva_tax_desc:
            val['iva_tax_desc'] = self.iva_tax_desc
        if self.iva_tax_code:
            val['iva_tax_code'] = self.iva_tax_code
        if self.non_tax_deductible:
            val['non_tax_deductible'] = self.non_tax_deductible
        return val
