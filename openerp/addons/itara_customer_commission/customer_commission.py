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


class cus_commission_master(osv.osv):
    _name="cus.commission.master"
    _description="Customer commission Master"
    
    
    def _after_cal_inv(self, cr, uid, ids,name,args, context=None):
        res={}
        print 'called'
        his_c = self.browse(cr, uid, ids)
        for m in his_c:
            sub_id = self.pool.get('com.point.history').search(cr,uid,[('may2on','=',m.id)])
            sub_br = self.pool.get('com.point.history').browse(cr,uid,sub_id)
            for his_class in sub_br:
                invoice_id = his_class.in_id
                inv_class = self.pool.get('account.invoice').search(cr, uid, [('id','=',invoice_id)])
                inv_br = self.pool.get('account.invoice').browse(cr, uid, inv_class)
                for i in inv_br:
                    print i.number,'------',i.date_invoice,'--------',his_class.id
                    self.pool.get('com.point.history').write(cr,uid, his_class.id, {
                    'date':str(i.date_invoice),
                    'name':str(i.number)
                    })
                    res[m.id]= 87
        return res
    
    
    _columns={
        'name':fields.many2one('res.partner','Customer Name'),
        'com_points':fields.integer('Points'),
        'commission_amt':fields.integer("Commission Amount"),
        'on2may':fields.one2many('com.point.history','may2on', "Points History", readonly=True),
        'aft_inv_gen':fields.function(_after_cal_inv, string=' ', method=True, type="integer"),
    }
    
cus_commission_master()

class com_point_history(osv.osv):
    _name="com.point.history"
    _description="Commission Points History"
    
        
    _columns={
          'name':fields.char('Invoice No.', size=128),
          'date':fields.char("Invoice Date", size=256),
          'in_id':fields.integer("Invoice ID"),
          'c_point':fields.integer("Points"),
          'c_amount':fields.integer("Commission Amount"),
          'i_amount':fields.integer("Invoice Amount"),
          'may2on':fields.many2one("cus.commission.master",'Poinnt link history'),

        }
        

        
com_point_history()

class commission_points_master(osv.osv):
    _name="commission.points.master"
    _description="Commission points value master"
    

    
    _columns={
        'name':fields.char("Name",size=128),
        'amt_starts':fields.integer("Amounts Starts", required=True),
        'amt_ends':fields.integer("Amounts Ends",required=True),
        'points':fields.integer("Points",required=True),
        'point_amt':fields.integer("Amount",required=True),
        }
commission_points_master()


class invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns={
        'amt_bool':fields.boolean('Amt Boolean'),
        'amt_bool1':fields.boolean('Amt Boolean1'),
        'less_amt':fields.integer("Less Amt"),
        'point_p':fields.integer("Commission Points"),
        'amount_a':fields.integer("Commission Amount(-)"),
    }
    _defaults={
            'amt_bool':False,
            'amt_bool1':False,
    }
    
    def get_commission_point(self, cr, uid, ids, context=None):
        inv = self.browse(cr, uid, ids[0], context=context)
        commission_points=self.pool.get('commission.points.master')
        com_point_list=commission_points.search(cr, uid, [('amt_starts','<=',inv.amount_total),('amt_ends','>=',inv.amount_total)])
        if not com_point_list:
            raise osv.except_osv(_('WARNING !'),
                    _('This Invoice Amount has No Points !'))
        else:
            comm_point_br=commission_points.browse(cr, uid, com_point_list, context=None)
            for i in comm_point_br:
                com_points = i.points
                com_point_amt = i.point_amt
            part_id = self.pool.get('cus.commission.master').search(cr, uid, [('name','=',inv.partner_id.id)])
            if len(part_id) > 0:
                com=self.pool.get('cus.commission.master').browse(cr,uid,part_id[0])
                self.pool.get('cus.commission.master').write(cr, uid,part_id[0],{'name':inv.partner_id.id, 'com_points': com_points, 'commission_amt':com_point_amt })  
                self.write(cr, uid, ids,{'amt_bool': True, 'point_p':com_points , 'amount_a':com_point_amt } )
            else:
                self.pool.get('cus.commission.master').create(cr, uid,{'name':inv.partner_id.id, 'com_points': com_points, 'commission_amt': com_point_amt }) 
                self.write(cr, uid, ids,{'amt_bool': True, 'point_p':com_points, 'amount_a':com_point_amt } )

        return True
    
    def use_comm_points(self, cr, uid, ids, context=None):
        inv = self.browse(cr, uid, ids[0], context=context)
        commission_points=self.pool.get('cus.commission.master')
        com_point_list=commission_points.search(cr, uid, [('name','=',inv.partner_id.id)])
        if not com_point_list:
            print "Empty"
            raise osv.except_osv(_('WARNING !'),
                    _('This Customer has No Points !'))
        else:
            part_id = self.pool.get('cus.commission.master').search(cr, uid, [('name','=',inv.partner_id.id)])
            com_br=self.pool.get('cus.commission.master').browse(cr,uid,part_id[0])
            less_amt = inv.amount_total-com_br.commission_amt
            self.pool.get('account.invoice').write(cr, uid, ids[0],{'amount_total': less_amt, 'check_total': less_amt, 'amt_bool1':1})
            ss = self.pool.get('account.invoice').browse(cr, uid, ids[0], context=context)
            x = cr.execute(""" update account_invoice  set amount_total= %s where id=%s """,(less_amt,ids[0]))
            self.pool.get('cus.commission.master').write(cr, uid, part_id[0], {'com_points':0, 'commission_amt':0})
            self.pool.get('com.point.history').create(cr, uid,{
                                                                'may2on':com_br.id,
                                                                'date': inv.date_invoice or ' ',
                                                                'in_id':inv.id,
                                                                'name':inv.number,
                                                                'c_point': inv.point_p,
                                                                'c_amount':inv.amount_a,
                                                                'i_amount':inv.amount_total,
                                                                })
        return True
        
        
        
        def _amount_all(self, cr, uid, ids, name, args, context=None):
            res = {}
            for invoice in self.browse(cr, uid, ids, context=context):
                res[invoice.id] = {
                    'amount_untaxed': 0.0,
                    'amount_tax': 0.0,
                    'amount_total': 0.0
                }
                print res[invoice.id]['less_amt'], "_amount_all _amount_all"
                for line in invoice.invoice_line:
                    res[invoice.id]['amount_untaxed'] += line.price_subtotal
                for line in invoice.tax_line:
                    res[invoice.id]['amount_tax'] += line.amount
                print res[invoice.id]['less_amt'], "_amount_all _amount_all"
                res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
                if invoice.less_amt > 0:
                    res.update({'less_amt':invoice.less_amt})
                    print res[invoice.id]['less_amt'], "_amount_all _amount_all"
                    res[invoice.id]['amount_total'] = res[invoice.id]['amount_total'] - res[invoice.id]['less_amt']
            return res
        
invoice()
