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

class lead_contact_address(osv.osv):
    _name="lead.contact.address"
    _description="Address fields"
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
lead_contact_address()

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
#####END seqId##########

    _columns = {
        'id_number':fields.char('ID Number',size=64, readonly=True),
	'birth_date' : fields.date('Birth date'),
	'age':fields.char('Age',size=68),
	'addition_contact':fields.one2many("lead.contact.address",'add_cont_id','Additional Contacts'),
	'heard_about':fields.selection([('friend','Friend'),('internet','Internet'),('others','Others')],'How U heard abt us'),
	'others_heard':fields.char(" ",size=128),
	'tick_link_id':fields.many2one('ticket.list','Tickets', domain="['&',('sal_per_id','=',uid), ('allocation_date','<', time.strftime('%Y-%m-%d 23:59:59').encode('utf8')), ('allocation_date','>=', time.strftime('%Y-%m-%d 00:00:00').encode('utf8'))]"),
	
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
    		val = {'value':
    			{
    			'age' : str(age_cal),
    			}}
    	return val

crm()
