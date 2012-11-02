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
from datetime import date

class opp_contact_address(osv.osv):
    _name="opp.contact.address"
    _description="Oppur cont add fields"
    _columns={
    'add_cont_id':fields.many2one("crm.lead", 'Addional contact'),
    'name':fields.char("Contact Name",size=68),
    'street':fields.char("Street", size=128),
    'street2':fields.char("Street2", size=128),
    'zip':fields.char("Zip",size=24),
    'city':fields.char("City",size=64),
    'state_id': fields.many2one("res.country.state", 'Fed. State', domain="[('country_id','=',country_id)]"),
    'country_id': fields.many2one('res.country', 'Country'),
    'phone':fields.char("Phone",size=24),
    'fax':fields.char("Fax",size=24),
    'mobile':fields.char("Mobile",size=24),
    }
opp_contact_address()

class product_lead(osv.osv):
    _name = "product.lead"
    _columns = {
    	'product_id' : fields.many2one('product.product','Product Name',domain=[('sale_ok', '=', True)], change_default=True),
    	'product_uom_qty' : fields.float('Product Qty', digits=(16, 2)),
    	'product_uom' : fields.many2one('product.uom','Product UOM'),
    	'partner_id' : fields.many2one('res.partner','Partner'),
    	'item_model' : fields.char('Item Model', size=128),
    	'lead_id' : fields.many2one('crm.lead','Lead'),
    }
    
    def onchange_product_id(self,cr, uid, ids, product_id):
    	#if product_id:
    	val = {}
    	print product_id
    	if product_id:
    		product = self.pool.get('product.product').browse(cr, uid, product_id)
    		#if product_id :
    		val = {'value':
    			{

    			'product_uom' : product.uom_id.id,
    			#'item_model' : product.item_model,
    					
    			}}	
    	return val	       
        
product_lead()


class partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
	'product_line' : fields.one2many('product.lead','partner_id','Product'),
        
     }

partner()



class crm(osv.osv):
    _inherit = "crm.lead"

####3#Seq Id Generation#########
    def id_generation(self, cr, uid, ids,*args):
        for o in self.browse(cr, uid, ids, context={}):
            if o.id_number == '/':
                seq_no = self.pool.get('ir.sequence').get(cr, uid, 'crm.lead.form.seq')
                self.write(cr, uid, o.id, {'id_number': seq_no,})
            else:
                raise osv.except_osv(_('ID No Alredy Generated !'),
                    _('ID No Alredy Generated!'))
        return True
    
    def create(self, cr, user, vals, context=None):
       # if ('name' not in vals) or (vals.get('name')=='/'):
       #     vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'quality.accept')
       # return super(quality_accept,self).create(cr, user, vals, context)
    
        #loc_id=self.browse(cr, uid, context={})
        #print loc_id,":::::::::::::::::::::::::::::"
        ser=self.pool.get('ticket.list').search(cr, user,[('id','=',vals['tick_link_id'])])
        self.pool.get('ticket.list').write(cr, user, ser[0], {'state': 'assigned'})
        return super(crm,self).create(cr, user, vals, context)
	
#####END seqId##########

    _columns = {
        'id_number':fields.char('ID Number',size=64, readonly=True),
	'birth_date' : fields.date('Birth date'),
	'age':fields.char('Age',size=68),
	'addition_contact':fields.one2many("opp.contact.address",'add_cont_id','Additional Contacts'),
	'heard_about':fields.selection([('friend','Friend'),('internet','Internet'),('others','Others')],'How U heard abt us'),
	'others_heard':fields.char(" ",size=128),
#	'tick_link_id':fields.many2one('ticket.list','Tickets', domain="['&',('sal_per_id','=',uid), ('allocation_date','<', time.strftime('%Y-%m-%d 23:59:59').encode('utf8')), ('allocation_date','>=', time.strftime('%Y-%m-%d 00:00:00').encode('utf8'))]"),
	'tick_link_id':fields.many2one('ticket.list','Tickets', domain="['&',('sal_per_id','=',uid), ('allocation_date','<', time.strftime('%Y-%m-%d 23:59:59')), ('allocation_date','>=', time.strftime('%Y-%m-%d 00:00:00'))]"),
   	'product_line' : fields.one2many('product.lead','lead_id','Product'),

     }
    _defaults = {
         'id_number': lambda obj, cr, uid, context: '/',
     }

    def onchange_birth_date(self,cr, uid, ids, birth_date):
        val = {}
        days_in_year = 365.25
        if birth_date:
            sp_date = birth_date.split("-")
            b_date = date(int(sp_date[0]),int(sp_date[1]),int(sp_date[2]))
            age_cal = int((date.today() - b_date).days/days_in_year)
            val['age']= str(age_cal) # = {'value': {'age' : str(age_cal),} }
        return {'value':val}
        
    def action_makesurvey(self, cr, uid, ids, context=None):
       # sur_obj = self.pool.get('general.medical.survey')
       # print sur_obj,"MEDICAL SURVEy"
       # opp = self.browse(cr, uid, ids, context=context)
       # print opp[0].id,"LOCALJI   ID IIDD  "
       # sur_obj = self.pool.get('general.medical.survey').create(cr, uid,
       #        {'oppor_link_id':opp[0].id})
       # return True
        if context is None:
            context = {}
        value = {}
        data_obj = self.pool.get('ir.model.data')
        for opp in self.browse(cr, uid, ids, context=context):
            # Get meeting views
            #tree_view = data_obj.get_object_reference(cr, uid, 'crm', 'action_crm_survey_tree_id_act')
            #form_view = data_obj.get_object_reference(cr, uid, 'crm', 'action_crm_survey_form_id_act')
            #calander_view = data_obj.get_object_reference(cr, uid, 'crm', 'crm_case_calendar_view_meet')
            #search_view = data_obj.get_object_reference(cr, uid, 'crm', 'view_crm_case_meetings_filter')
            context.update({
                'default_oppor_link_id': opp.id,
                'default_name': opp.partner_id and opp.partner_id.id or False,
                #'default_user_id': uid,
                'default_age': opp.age,
               
            })
            value = {
                'name': _('Survey'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'general.medical.survey',
                'view_id': False,
             #   'views': [(form_view and form_view[1] or False, 'form'), (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
              #  'search_view_id': search_view and search_view[1] or False,
                'nodestroy': True
                }
        return value
        
        
        
 #   def action_makeinvoice(self, cr, uid, ids, context=None):
 #       if context is None:
 #           context = {}
 #       value = {}
 #       data_obj = self.pool.get('ir.model.data')
 #       for opp in self.browse(cr, uid, ids, context=context):
 #           context.update({
 #               #'default_oppor_link_id': opp.id,
 #               'default_partner_id': opp.partner_id and opp.partner_id.id or False,
 #               'default_address_invoice_id': opp.partner_address_id and opp.partner_id.id or False,
                #'default_user_id': uid,
 #               'default_age': opp.age,
               
  #          })
   #         value = {
  #              'name': _('Pay'),
  #              'context': context,
  #              'view_type': 'form',
  #              'view_mode': 'form,tree',
  #              'res_model': 'account.invoice',
  #              'view_id': False,
             #   'views': [(form_view and form_view[1] or False, 'form'), (tree_view and tree_view[1] or False, 'tree')],
  #              'type': 'ir.actions.act_window',
              #  'search_view_id': search_view and search_view[1] or False,
  #              'nodestroy': True
  #              }
  #      return value

crm()
