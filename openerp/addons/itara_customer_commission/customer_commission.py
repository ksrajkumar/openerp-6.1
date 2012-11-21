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
    _columns={
        'name':fields.many2one('res.partner','Customer Name'),
        'com_points':fields.integer('Points'),
    }
cus_commission_master()


class commission_points_master(osv.osv):
    _name="commission.points.master"
    _description="Commission points value master"
    _columns={
        'name':fields.char("Name",size=128),
        'amt_starts':fields.integer("Amounts Starts"),
        'amt_ends':fields.integer("Amounts Ends"),
        'points':fields.integer("Points"),
        'point_amt':fields.integer("Amount"),
        }
commission_points_master()


class invoice(osv.osv):
    _inherit = 'account.invoice'

    def get_commission_point(self, cr, uid, ids, context=None):
        print ids,"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
        inv = self.browse(cr, uid, ids[0], context=context)
        print inv.amount_total, inv.partner_id,"tot tot toto tot tot tot"
        point_dict={3000:10, 5000:15, 8000:20, 10000:25, 15000:30, 20000:50,}
        part_id = self.pool.get('cus.commission.master').search(cr, uid, [('name','=',inv.partner_id.id)])
        if len(part_id) > 0:
            com=self.pool.get('cus.commission.master').browse(cr,uid,part_id[0])
            print com,"LLLLLLLLLLLLLLLLLLLLLLL",com.id
        print part_id,"partner partner partner partner"
        
        if inv.amount_total >= 3000 and inv.amount_total <5000:
            if len(part_id) > 0:
                self.pool.get('cus.commission.master').write(cr, uid,part_id[0],{'name':inv.partner_id.id, 'com_points':point_dict[3000]+com.com_points})
            else:
                self.pool.get('cus.commission.master').create(cr, uid,{'name':inv.partner_id.id, 'com_points':point_dict[3000]})

        return True
        
        
invoice()


    #~ _defaults = {
         #~ 'alloc_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
     #~ }
#~ 
    #~ def onchange_entity_data_id(self, cr, uid, ids, entity_data_id):
        #~ val={}
        #~ if entity_data_id:
            #~ x=self.pool.get('entity.data').browse(cr, uid, entity_data_id)
            #~ val['enty_no']= x.ent_num #  { 'value' : {'enty_no':x.ent_num} } 
        #~ return {'value':val}
#~ 
#~ ####3#Seq Id Generation#########
    #~ def tick_generation(self, cr, uid, ids,*args):
        #~ for o in self.browse(cr, uid, ids, context={}):
            #~ seq_no = self.pool.get('ir.sequence').get(cr, uid, 'ticket.number.seq')
            #~ print o, "===", o.id, o.sales_person_id, o.alloc_date, o.entity_data_id.id, o.entity_data_id.ent_num,'=====',o.sales_person_id.context_section_id.code
            #~ jx=self.pool.get('ticket.list').create(cr, uid, 
                        #~ {'name': o.sales_person_id.context_section_id.code+o.sales_person_id.code+str(time.strftime("%d%m%Y"))+seq_no, 
                        #~ 'add_tick_id':o.id, 
                        #~ 'sal_per_id':o.sales_person_id.id, 
                        #~ 'allocation_date':o.alloc_date,
                        #~ 'remarks':o.remarks,
                        #~ 'entity_data_id':o.entity_data_id.id,
                        #~ 'enty_no':o.entity_data_id.ent_num or 'o',
                        #~ })
        #~ return True
#~ 
#~ ticket_allocation()

#~ class ticket_list(osv.osv):
    #~ _name="ticket.list"
    #~ _description="Ticket list"
    #~ _order = "priority"
    #~ _columns = {
    #~ 'name':fields.char('Ticket number', size=256),
    #~ 'add_tick_id':fields.many2one('ticket.allocation', 'Tick',ondelete='cascade'),
    #~ 'sal_per_id':fields.many2one('res.users','Sales Person'),
    #~ 'allocation_date':fields.datetime('Allocation Date'),
    #~ 'remarks':fields.char('Remark',size=256),
    #~ 'entity_data_id':fields.many2one('entity.data','Entity'),
    #~ 'enty_no':fields.char('Entity No',size=256),
    #~ 'state':fields.selection([('new','New'),('assigned','Assigned')],'state'),
#~ ################################################################################################################    
    #~ 'color': fields.integer('Color Index'),
    #~ 'kanban_state': fields.selection([('normal', 'Normal'),('blocked', 'Blocked'),('done', 'Ready To Pull')], 'Kanban State',
                                         #~ readonly=True, required=False),
        #~ 'priority': fields.selection([('4','Very Low'), ('3','Low'), ('2','Medium'), ('1','Important'), ('0','Very important')], 'Priority', select=True),
											#~ 
    #~ #  in complete
    #~ }
    #~ 
    #~ _defaults={
          #~ 'state': 'new',
          #~ 'kanban_state': 'normal',
          #~ 'priority': '2',
          #~ 'color': 5}
          #~ 
#~ 
#~ 
    #~ def set_priority(self, cr, uid, ids, priority):
        #~ """Set task priority
        #~ """
        #~ return self.write(cr, uid, ids, {'priority' : priority})
#~ 
    #~ def set_high_priority(self, cr, uid, ids, *args):
        #~ """Set task priority to high
        #~ """
        #~ print ids,"))))))))))))))))))))))))))))))))"
        #~ return self.set_priority(cr, uid, ids, '1')
#~ 
    #~ def set_normal_priority(self, cr, uid, ids, *args):
        #~ """Set task priority to normal
        #~ """
        #~ return self.set_priority(cr, uid, ids, '2')
        #~ 
    #~ def set_kanban_state_blocked1(self, cr, uid, ids, context=None): 
        #~ self.write(cr, uid, ids, {'kanban_state': 'blocked'}, context=context)
#~ 
    #~ def set_kanban_state_normal1(self, cr, uid, ids, context=None):
        #~ self.write(cr, uid, ids, {'kanban_state': 'normal'}, context=context)
#~ 
    #~ def set_kanban_state_done1(self, cr, uid, ids, context=None):
        #~ self.write(cr, uid, ids, {'kanban_state': 'done'}, context=context)
        #~ 
#~ ################################################################################################################        
#~ 
#~ ticket_list()
