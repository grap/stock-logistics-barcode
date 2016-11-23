# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# Copyright (C) 2016-Today La Louve (http://www.lalouve.net)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class BarcodeRule(orm.Model):
    _inherit = 'barcode.rule'

    _columns = {
        'generate_model': fields.selection(
            string='Generate Model',
            selection=[('product.product', 'Products')],
            help="if 'Generate Type' is set, mention the model related to this"
            " rule."),
    }
