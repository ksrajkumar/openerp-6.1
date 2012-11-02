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

class entity_data(osv.osv):
    _name="entity.data"
    _description="Entity Datas"
    _columns={
        'name':fields.char('Entity Name',size=256),
        'ent_dept':fields.many2one('entity.dep.master','Department'),
        'ent_date':fields.date('Date'),
        'ent_num':fields.char('Entity No.',size=256),
      }
entity_data()

#~ class entity_master(osv.osv):
    #~ _name="entity.master"
    #~ _description="Entity Master"
    #~ _columns={
        #~ 'name':fields.char('Entity Name',size=256),
        #~ 'ent_dep_mast_id':fields.many2one('entity.dep.master','Department'),
    #~ }
#~ entity_master()

class entity_dep_master(osv.osv):
    _name="entity.dep.master"
    _description="Entity Dept Master"
    _columns={
        'name':fields.char('Department Name',size=256),
    }
entity_dep_master()

class ticket_allocation(osv.osv):
    _name = "ticket.allocation"
    _description = "ticket allocation form"
    _columns={
    'name':fields.char('Name', size=256),
    'sales_person_id':fields.many2one('res.users','Sales Person'),
    'alloc_date':fields.datetime('Allocation Date'),
    'tick_num':fields.one2many('ticket.list','add_tick_id','Ticket Numbers'),
    'remarks':fields.char('Remarks',size=256),
    'entity_data_id':fields.many2one('entity.data','Entity'),
    'enty_no':fields.char('Entity No',size=256),
    }
    _defaults = {
         'alloc_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
     }

    def onchange_entity_data_id(self, cr, uid, ids, entity_data_id):
        val={}
        if entity_data_id:
            x=self.pool.get('entity.data').browse(cr, uid, entity_data_id)
            val['enty_no']= x.ent_num #  { 'value' : {'enty_no':x.ent_num} } 
        return {'value':val}

####3#Seq Id Generation#########
    def tick_generation(self, cr, uid, ids,*args):
        for o in self.browse(cr, uid, ids, context={}):
            seq_no = self.pool.get('ir.sequence').get(cr, uid, 'ticket.number.seq')
            print o, "===", o.id, o.sales_person_id, o.alloc_date, o.entity_data_id.id, o.entity_data_id.ent_num
            jx=self.pool.get('ticket.list').create(cr, uid, 
                        {'name': o.sales_person_id.name[0:4]+str(time.strftime("%d%m%Y"))+seq_no, 
                        'add_tick_id':o.id, 
                        'sal_per_id':o.sales_person_id.id, 
                        'allocation_date':o.alloc_date,
                        'remarks':o.remarks or ' ',
                        'entity_data_id':o.entity_data_id.id,
                        'enty_no':o.entity_data_id.ent_num or 'o',
                        })
        return True
#####END seqId##########

#    def tick_generation(self, cr, uid, ids,*args):
#        x=0
#        def static_num():
#            global x
#            x=x+1
#            return x
##        for x in range(i+1,i+6):
##            print x
#        for i in range(0,5):
#            print static_num()
#        return True


ticket_allocation()

class ticket_list(osv.osv):
    _name="ticket.list"
    _description="Ticket list"
    _columns = {
    'name':fields.char('Ticket number', size=256),
    'add_tick_id':fields.many2one('ticket.allocation', 'Tick',ondelete='cascade'),
    'sal_per_id':fields.many2one('res.users','Sales Person'),
    'allocation_date':fields.datetime('Allocation Date'),
    'remarks':fields.char('Remark',size=256),
    'entity_data_id':fields.many2one('entity.data','Entity'),
    'enty_no':fields.char('Entity No',size=256),
    'state':fields.selection([('new','New'),('assigned','Assigned')],'state'),
    #  in complete
    }
    _defaults={
      'state': 'new',
   }
ticket_list()
