# copyright  2018 Carlos Wong, Akurey SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict
from odoo import api, fields, models

ADDRESS_FIELDS = ('neighborhood_id', 'district_id', 'county_id')


class PartnerElectronic(models.Model):
    _inherit = "res.partner"

    # Province
    state_id = fields.Many2one("res.country.state", string="Province", tracking=True)

    # County
    county_id = fields.Many2one("res.country.county", string="County", tracking=True)

    # District
    district_id = fields.Many2one("res.country.district", string="District", tracking=True)

    # Neighborhood
    neighborhood_id = fields.Many2one("res.country.neighborhood", string="Neighborhood", tracking=True)

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

    # When you change the county you must clean the other fields to avoid inconveniences
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

            # County
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

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return super()._address_fields() + list(ADDRESS_FIELDS)

    def _prepare_display_address(self, without_company=False):
        address_format, args = super()._prepare_display_address(without_company=without_company)
        args.update({
            'neighborhood_code': self.neighborhood_id.code or '',
            'neighborhood_name': self.neighborhood_id.name or '',
            'district_code': self.district_id.code or '',
            'district_name': self.district_id.name or '',
            'county_code': self.county_id.code or '',
            'county_name': self.county_id.name or '',
        })
        
        return address_format, args
