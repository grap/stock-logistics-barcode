# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# Copyright (C) 2016-Today La Louve (http://www.lalouve.net)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp.osv import osv, fields, orm
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    import barcode
except ImportError:
    _logger.debug("Cannot import 'barcode' python library.")
    barcode = None


class BarcodeGenerateMixin(orm.AbstractModel):
    _name = 'barcode.generate.mixin'

    # Column Section
    _columns = {
        'barcode_rule_id': fields.many2one(
            'barcode.rule', string='Barcode Rule'),
        'barcode_base': fields.integer(string='Barcode Base'),
        'generate_type': fields.related(
            'barcode_rule_id', 'generate_type', string='Generate Type',
            type='selection', readonly=True),
    }

    # View Section
    def generate_base(self, cr, uid, ids, context=None):
        sequence_obj = self.pool['ir.sequence']
        for item in self.browse(cr, uid, ids, context=context):
            if item.generate_type != 'sequence':
                raise osv.except_osv(_('Error'), _(
                    "Generate Base can be used only with barcode rule with"
                    " 'Generate Type' set to 'Base managed by Sequence'"))
            else:
                # TODO
                self.write(cr, uid, [item.id], {
                    'barcode_base': sequence_obj.next_by_id(
                        cr, uid, item.barcode_rule_id.sequence_id.id,
                        context=context)}, context=context)
                pass
#                item.barcode_base =\
#                    item.barcode_rule_id.sequence_id.next_by_id()

    def generate_barcode(self, cr, uid, ids, context=None):
        for item in self.browse(cr, uid, ids, context=context):
            padding = item.barcode_rule_id.padding
            str_base = str(item.barcode_base).rjust(padding, '0')
            custom_code = self._get_custom_barcode(
                cr, uid, item, context=context)
            if custom_code:
                custom_code = custom_code.replace('.' * padding, str_base)
                barcode_class = barcode.get_barcode_class(
                    item.barcode_rule_id.encoding)
                self.write(cr, uid, [item.id], {
                    'ean13': barcode_class(custom_code)}, context=context)

    # Custom Section
    def _get_custom_barcode(self, cr, uid, item, context=None):
        """
            if the pattern is '23.....{NNNDD}'
            this function will return '23.....00000'
            Note : Overload _get_replacement_char to have another char
            instead that replace 'N' and 'D' char.
        """
        if not item.barcode_rule_id:
                return False

        # Define barcode
        custom_code = item.barcode_rule_id.pattern
        custom_code = custom_code.replace('{', '').replace('}', '')
        custom_code = custom_code.replace(
            'D', self._get_replacement_char(cr, uid, 'D', context=context))
        return custom_code.replace(
            'N', self._get_replacement_char(cr, uid, 'N', context=context))

    def _get_replacement_char(self, cr, uid, char, context=None):
        """
        Can be overload by inheritance
        Define wich character will be used instead of the 'N' or the 'D'
        char, present in the pattern of the barcode_rule_id
        """
        return '0'
