# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime, timedelta
import requests
import os
from lxml import etree
from zeep import Client
import xml.etree.ElementTree
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ResCurrencyRateProviderCR(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("Hacienda", "Ministerio de Hacienda Costa Rica"), ("BCCR", "Banco Central de Costa Rica")],
        ondelete={"Hacienda": "set default", "BCCR": "set default"},
    )
    bccr_username = fields.Char(string="BCCR username")
    bccr_email = fields.Char(string="e-mail registered in the BCCR")
    bccr_token = fields.Char(string="Token to use in the BCCR",)

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service not in ("Hacienda", "BCCR"):
            return super()._get_supported_currencies()
        # List of currencies obrained from Costa Rica Central Bank
        return [
            "USD",
            #"EUR",
            #"CRC",
        ]

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service == "Hacienda":
            return self._obtain_rates_Hacienda(base_currency, currencies, date_from, date_to)
        elif self.service == "BCCR":
            return self._obtain_rates_BCCR(base_currency, currencies, date_from, date_to)
        else:
            return super()._obtain_rates(base_currency, currencies, date_from, date_to)

    def _obtain_rates_Hacienda(self, base_currency, currencies, date_from, date_to):
        initial_date = date_from.strftime('%Y-%m-%d')
        end_date = date_to.strftime('%Y-%m-%d')
        """proxies = {
                    'http': 'http://10.0.0.254:3128',
                    'https': 'http://10.0.0.254:3128',
        }
        auth = ('marioab', 'password')"""
        try:
            proxies = {
                'http': os.environ.get('http_proxy'),
                'https': os.environ.get('https_proxy')
            }
            _logger.error('FECCR - Proxy: %s', proxies )

            url = 'https://api.hacienda.go.cr/indicadores/tc/dolar/historico/?d='+initial_date+'&h='+end_date
            #response = requests.get(url, proxies=proxies, auth=auth, timeout=5, verify=False)
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, proxies=proxies, timeout=5, verify=True)

        except requests.exceptions.RequestException as e:
            raise UserError(
                _("Couldn't fetch data. Please contact your administrator.")
            ) from e

        if response.status_code in (200,):
            data = response.json()
            content = {}
            for rate_line in data:
                current_date = datetime.strptime(rate_line['fecha'], '%Y-%m-%d %H:%M:%S').date()
                vals = {'USD' : rate_line['venta']}
                content[current_date] = vals
        return content

    def _obtain_rates_BCCR(self, base_currency, currencies, date_from, date_to):
        initial_date = date_from.strftime('%d/%m/%Y')
        end_date = date_to.strftime('%d/%m/%Y')

        _logger.info("Getting exchange rates from BCCR")

        # Web Service Connection using the XML schema from BCCRR
        client = Client('https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx?WSDL')

        response = client.service.ObtenerIndicadoresEconomicosXML(
            Indicador='318', FechaInicio=initial_date, FechaFinal=end_date,
            Nombre=self.bccr_username, SubNiveles='N', CorreoElectronico=self.bccr_email, Token=self.bccr_token)

        xml_response = xml.etree.ElementTree.fromstring(response)
        selling_rate_nodes = xml_response.findall("./INGC011_CAT_INDICADORECONOMIC")

        node_index = 0
        rates_count = len(selling_rate_nodes)
        content = {}
        while node_index < rates_count:
            current_date_str = datetime.strptime(selling_rate_nodes[node_index].find("DES_FECHA").text,
                                                    "%Y-%m-%dT%H:%M:%S-06:00").strftime('%Y-%m-%d')

            selling_original_rate = float(selling_rate_nodes[node_index].find("NUM_VALOR").text)
            selling_rate = 1 / selling_original_rate

            current_date = datetime.strptime(selling_rate_nodes[node_index].find("DES_FECHA").text,
                                                "%Y-%m-%dT%H:%M:%S-06:00").strftime('%Y-%m-%d')
            vals = {'USD' : selling_original_rate}
            content[current_date] = vals
            node_index += 1
        return content
