# copyright  2018 Carlos Wong, Akurey SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CompanyElectronic(models.Model):
    _name = "res.company"
    _inherit = [
        "res.company",
        "mail.thread",
    ]

    # Province
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Province",
        compute="_compute_address",
        inverse="_inverse_state"
    )

    # County
    county_id = fields.Many2one(
        comodel_name="res.country.county",
        string="County",
        compute="_compute_address",
        inverse="_inverse_county"
    )

    # District
    district_id = fields.Many2one(
        comodel_name="res.country.district",
        string="District",
        compute="_compute_address",
        inverse="_inverse_district"
    )

    # Neighborhood
    neighborhood_id = fields.Many2one(
        comodel_name="res.country.neighborhood",
        string="Neighborhood",
        compute="_compute_address",
        inverse="_inverse_neighborhood"
    )

    # When you change the province you must clean the other fields to avoid inconveniences
    @api.onchange("state_id")
    def _change_state_id(self):
        for record in self:
            if not record.zip:
                record.county_id = False
                record.district_id = False
                record.neighborhood_id = False
                record.city = False
            record.city = record.state_id.name

    # When you change the canton you must clean the other fields to avoid inconveniences
    @api.onchange("county_id")
    def _change_county_id(self):
        for record in self:
            if not record.zip:
                record.district_id = False
                record.neighborhood_id = False

    # When you change the district you must clean the other fields to avoid inconveniences
    @api.onchange("district_id")
    def _calculate_postal_code(self):
        for record in self:
            if not record.zip:
                if record.state_id.code and record.county_id.code and record.district_id.code:
                    postal = str(record.state_id.code) + str(record.county_id.code) + str(record.district_id.code)
                    record.zip = postal
                else:
                    record.zip = False
                record.neighborhood_id = False

    @api.onchange("zip")
    def _change_zip(self):
        for record in self:
            # Province
            zip_code = record.zip

            if not zip_code:
                continue

            state_id = self.env["res.country.state"].search([("code", "=", zip_code[0:1])], limit=1)

            # Canton
            county_id = self.env["res.country.county"].search(
                [("code", "=", zip_code[1:3]), ("state_id", "=", state_id.id)], limit=1
            )

            # District
            district_id = self.env["res.country.district"].search(
                [("code", "=", zip_code[3:5]), ("county_id", "=", county_id.id)], limit=1
            )

            record.write(
                {
                    "state_id": state_id.id,
                    "county_id": county_id.id,
                    "district_id": district_id.id,
                    "neighborhood_id": False,
                }
            )

    def _get_company_address_field_names(self):
        """Return a list of fields coming from the address partner to match
        on company address fields. Fields are labeled same on both models."""
        res = super()._get_company_address_field_names()
        res.append("neighborhood_id")
        res.append("district_id")
        res.append("county_id")
        return res

    def _compute_address(self):
        for company in self.filtered(lambda company: company.partner_id):
            address_data = company.partner_id.sudo().address_get(adr_pref=["contact"])
            if address_data["contact"]:
                partner = company.partner_id.browse(address_data["contact"]).sudo()
                company.update(company._get_company_address_update(partner))

    def _inverse_state(self):
        for company in self:
            company.partner_id.state_id = company.state_id

    def _inverse_county(self):
        for company in self:
            company.partner_id.county_id = company.county_id

    def _inverse_district(self):
        for company in self:
            company.partner_id.district_id = company.district_id

    def _inverse_neighborhood(self):
        for company in self:
            company.partner_id.neighborhood_id = company.neighborhood_id
