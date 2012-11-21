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

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
import netsvc

class current_weight(osv.osv):
    _name='current.weight'
    _description='Creating master for Current Weight of the Customer'
    _columns={
    'name':fields.char('Current Weight', size=64),
    }
current_weight()



class customer_support_survey(osv.osv):
    _name="customer.support.survey"
    _description="Medical Survey for Support to the Customer"
    _columns={
     'tick_link_id':fields.many2one('ticket.list','Tickets', domain="['&',('sal_per_id','=',uid), ('allocation_date','<', time.strftime('%Y-%m-%d 23:59:59')), ('allocation_date','>=', time.strftime('%Y-%m-%d 00:00:00'))]"),
     'name':fields.many2one('res.partner', 'Name'),
     'email':fields.char('Email', size=128),
     'phone_number':fields.char('Phone Number', size=24),
     'current_status_id': fields.one2many('current.status', 'name_id', 'Current Status'),     
     'notes':fields.text('Notes'),
     'current_weight':fields.many2one('current.weight', 'Current Weight'),
     'custo_hist': fields.many2many('account.invoice','account_invoice_relation','account_id','invoice_id','History'),
    }


    def onchange_customer_invoice(self, cr, uid, ids, name, context=None):
        res= {}
        if name:
            cust = self.pool.get('account.invoice').search(cr, uid, [('partner_id', '=',name)], context=context)
            x=[]
            for i in self.pool.get('account.invoice').browse(cr, uid, cust, context=context):
                if i.type == "out_invoice":
                    x.append(i.id)
            res = {'value':{'custo_hist' : x}}
        return res

customer_support_survey()



class current_status_many(osv.osv):
    _name='current.status.many'
    _description='Creating master for Current Status of the Customer'
    _columns={
    'name':fields.char('Status',size=256),
    }
current_status_many()



class current_status(osv.osv):
    _name='current.status'
    _description='Creating master for Current Status of the Customer'
    _columns={
    'name': fields.many2one('current.status.many','Name'),
    'weight_gain':fields.float('How much weight u gain in the force feeding state'),
    'name_id':fields.many2one('customer.support.survey','Current Status'),
    }
current_status()



