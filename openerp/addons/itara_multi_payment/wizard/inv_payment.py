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

import time

from osv import osv, fields
from tools.translate import _

import netsvc


class inv_make_payment(osv.osv_memory):
    _name = 'inv.make.payment'
    _description = 'invoice multi Payment'
    def check(self, cr, uid, ids, context=None):
        print "file: wiz/pos_payment.py/ funct check"
        """Check the order:
        if the order is not paid: continue payment,
        if the order is paid print ticket.
        """
        context = context or {}
        order_obj = self.pool.get('sale.order')
        obj_partner = self.pool.get('res.partner')
        active_id = context and context.get('active_id', False)

        order = order_obj.browse(cr, uid, active_id, context=context)
        print order.amount_total,"amount_total__________________amount_total"
        inv = self.pool.get('account.invoice').browse(cr, uid, active_id, context=context)

        amount = order.amount_total - inv.residual
        data = self.read(cr, uid, ids, context=context)[0]
        # this is probably a problem of osv_memory as it's not compatible with normal OSV's
        #data['journal'] = data['journal'][0]
        print amount, "amount------------amount"
        if amount != 0.0:
            #~ order_obj.add_payment(cr, uid, active_id, data, context=context)
            self.pool.get('account.invoice').add_payment(cr, uid, active_id, data, context=context)

        if order_obj.test_paid(cr, uid, [active_id]):
            #~ wf_service = netsvc.LocalService("workflow")
            #~ wf_service.trg_validate(uid, 'pos.order', active_id, 'paid', cr)
            return self.print_report(cr, uid, ids, context=context)

        return self.launch_payment(cr, uid, ids, context=context)

    def launch_payment(self, cr, uid, ids, context=None):
        print "file: wiz/pos_payment.py/ funct launch_payment"
        return {
            'name': _('Paiement'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'inv.make.payment',
            'view_id': False,
            'target': 'new',
            'views': False,
            'type': 'ir.actions.act_window',
        }

    def print_report(self, cr, uid, ids, context=None):
        print "file: wiz/pos_payment.py/ funct print_report"
        active_id = context.get('active_id', [])
        datas = {'ids' : [active_id]}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pos.receipt',
            'datas': datas,
        }

    def _default_journal(self, cr, uid, context=None):
        print "file: wiz/pos_payment.py/ funct _default_jornal"
        #~ res = pos_box_entries.get_journal(self, cr, uid, context=context)
        #~ return len(res)>1 and res[1][0] or False
        return True

    def _default_amount(self, cr, uid, context=None):
        print "file: wiz/pos_payment.py/ funct _default_amount"
        order_obj = self.pool.get('sale.order')
        active_id = context and context.get('active_id', False)
        if active_id:
            order = order_obj.browse(cr, uid, active_id, context=context)
            inv = self.pool.get('account.invoice').browse(cr, uid, active_id, context=context)
            return order.amount_total - inv.residual
        return False

    _columns = {
        'journal': fields.many2one('account.journal', "Payment Mode", required=True),
        'amount': fields.float('Amount', digits=(16,2), required= True),
        'payment_name': fields.char('Payment Reference', size=32),
        'payment_date': fields.date('Payment Date', required=True),
    }
    _defaults = {
        'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
         'amount': _default_amount,
        #~ 'journal': _default_journal
    }

inv_make_payment()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
