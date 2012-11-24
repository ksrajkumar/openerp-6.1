# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from osv import osv, fields
import pooler
import re
from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
import netsvc
from datetime import date



class account_refund(osv.osv):
    _inherit = "account.invoice"


    def action_refundsurvey(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        value = {}
        data_obj = self.pool.get('ir.model.data')
        for opp in self.browse(cr, uid, ids, context=context):

            context.update({
                'default_oppor_link_id': opp.id,
                'default_name': opp.partner_id and opp.partner_id.id or False,
            })
            
            value = {
                'name': _('Survey'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'general.medical.survey',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'nodestroy': True
                }
        return value

account_refund()
