# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# Copyright (C) 2016-Today La Louve (http://www.lalouve.net)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, osv
from openerp.tools.translate import _


class ProductProduct(orm.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'barcode.generate.mixin']

    def _check_barcode_base_unicity(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            if product.barcode_rule_id and product.barcode_base:
                other_product_ids = self.search(cr, uid, [
                    ('id', '!=', product.id),
                    ('company_id', '=', product.company_id.id),
                    ('barcode_rule_id', '=', product.barcode_rule_id.id),
                    ('barcode_base', '=', product.barcode_base),
                    ], context=context)
                if len(other_product_ids):
                    return False
        return True

    _constraints = [
        (_check_barcode_base_unicity,
            "You cannot set such barcode base because other products have"
            " the same configuration",
            ['company_id', 'barcode_base', 'barcode_rule_id', 'active']),
    ]
