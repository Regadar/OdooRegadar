==================================
Facturación Electrónica Costa Rica
==================================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2|


Módulo para Odoo que implementa la Facturacion Electronica para Costa Rica actualmente en versión 4.3

- Agrega la generación de los archivos requeridos por el Ministerio de Hacienda al momento de generar una factura
- Comunicación con el API de Tributación para la presentación de las facturas y su validación
- Importación de facturas de proveedores y el envío del "Mensage Respuesta" (aceptación, aceptación parcial o rechazo).
- Envío de Facturas Electrónica de Compra

Más información en: https://atv.hacienda.go.cr/ATV/ComprobanteElectronico/frmAnexosyEstructuras.aspx

**Table of contents**

.. contents::
   :local:

Changelog
=========

12.0.1.0.0 (2019-06-25)
~~~~~~~~~~~~~~~~~~~~~~~

* Creation and first draft of the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OdooCR/l10n_cr/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OdooCR/l10n_cr/issues/new?body=module:%20l10n_cr%0Aversion:%2011.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~
Delfix S.A.
    * Mario Arias <the.clone.master@gmail.com>

* Charlie Monge <charlit02390@gmail.com>

* `TechMicro Inc S.A. <https://www.techmicrocr.com>`_
    * Jason Ulloa <jason.ulloa@techmicrocr.com>

* `AKUREY S.A. <https://www.akurey.com>`_
    * Carlos Wong <cwong@akurey.com>
    * Sergio Hidalgo <shidalgo@akurey.com>
    * Joaquin Mena <jmena@akurey.com>
    * Julio Barboza <jbarboza@akurey.com>

Contributors
~~~~~~~~~~~~
* Nehemias Herrera
* Esteban Monge <estebanmonge@riseup.net>

Configuración
===================

1. Ingresar a la compañía que deseamos configurar
    * Esto lo puede hacer desde Ajustes > Usuarios y compañías > Compañías

.. image:: doc/img/res_company_00.png
   :alt: Menú "Compañías" en Ajustes

2. Completar la siguiente información y luego presionar el botón de guardar:
    * Tipo de Identificación
    * NIF
    * Dirección
    * País, Provincia, Cantón, Distrito
    * Código Postal
    * Teléfono
    * Correo electrónico
    * Nombre Comercial
    * Nombre Legal

.. image:: doc/img/res_company_01.png
   :alt: Información general de la compañía

3. Hacer click en el botón "CONSULTAR ACTIVIDAD ECONÓMICA EN HACIENDA"
4. Elegimos la Actividad económica que deseamos se use por defecto
    * Esta actividad se completará automáticamente en los documentos, sin embargo, si posee más de una, podrá elegirla al momento de crear el documento electrónico
5. Completar la información sobre factura electrónica en la pestaña "Factura Electrónica"
    * Llave criptográfica
    * Usuario de facturación electrónica
    * Contraseña de facturación electrónica
    * Pin de la Llave criptográfica
    * Ambiente (Pruebas, Producción)

.. image:: doc/img/res_company_02.png
   :alt: Información de facturación electrónica de la compañía

El Ministrerio de Hacienda pone a disposición el siguiente PDF para revocar y generar nuevamente los datos de facturación electrónica del contribuyente https://www.hacienda.go.cr/docs/GuiaParaRevocarYGenerarLlaveCriptografica.pdf

6. El sistema cuenta con la posibilidad de notificarle X cantidad de días antes de llegue la fecha de vencimiento de su llave criptográfica, esto con el fin de que la vuelva a generar y evite que sus comprobantes electrónicos sean rechazados por el Ministerio de Hacienda, esta notificación puede enviarse a varios usuarios del sistema o a un correo en específico


7. Ingresar al listado de diarios contables
    * Community: Facturación > Configuración > Diarios contables
    * Enterprise: Contabilidad > Configuración > Diarios contables

.. image:: doc/img/account_journal_00.png
   :alt: Menú Diarios Contables

8. Ingresar al diario de tipo ventas y configurar las secuencias
    * En caso de que se esté migrando de otro sistema de facturación electrónica, deberá configurar las secuencias para que se ajusten al último documento emitido por tipo de comprobante

.. image:: doc/img/account_journal_01.png
   :alt: Diario Contable de tipo Ventas

9. Completar la Sucursal y Terminal en caso de que sea distinto a 1 (establecido por defecto)

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/l10n_cr <https://github.com/OCA/l10n_cr>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
