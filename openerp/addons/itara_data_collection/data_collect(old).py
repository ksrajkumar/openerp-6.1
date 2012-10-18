from osv import fields, osv
import time
from datetime import datetime
import pooler
import netsvc
import sys
import os
from osv import osv,fields
from mx.DateTime import *
from tools.translate import _
import logging
import netsvc
logger = logging.getLogger('server')

class crm_lead(osv.osv):    
    _inherit = "crm.lead"
    _columns = {
    'collect_line':fields.one2many('data.collect', 'lead_id', 'Data Collection' ),
    }    
crm_lead()

class data_collect(osv.osv):
    _name = "data.collect"  


                 
    _columns = {
    'name':fields.char('Name', size=68),
    'lead_id': fields.many2one('crm.lead', 'Leads'),
    'data_line':fields.one2many('data.collect.line', 'dc_id', 'Data Collect Line'),
    'desp':fields.char('Description', size=68),	 
    'req_id': fields.many2one('category.req', 'Requirements'),
    'data_ids': fields.one2many('data.collect.line', 'data_id', 'Questionnaire Lines'),
####### NATURE OF DUST ###############################################
    'dust1': fields.char('Dust Material', size=100),
    'dust2': fields.char('Bulk Density(kg/m3)', size=100),
    'dust3': fields.char('Particle Size(microns)', size=100),

######### DUST ######################################################
    'dusts1': fields.boolean('Hygroscopic(moisture)'),
    'dusts2': fields.boolean('Abrasive'),
    'dusts3': fields.boolean('Corrosive'),
    'dusts4': fields.boolean('Explosive'),
    'dusts5': fields.boolean('Sticky'),
    'dusts6': fields.boolean('toxic'),

######### UTILITY ######################################################	
    'utility': fields.text('Application Remarks'),

######### ELECTRICITY ######################################################	
    'voltage': fields.char('Voltage', size=64),
    'volts': fields.char('Volts', size=64),
    'frequency': fields.char('Frequency', size=64),
    'hz': fields.char('Hertz', size=64),

######### PHASE ######################################################	
    'phase1': fields.boolean('Three Phase'),
    'phase2': fields.boolean('Double Phase'),
    'phase3': fields.boolean('Single Phase'),	                      
    } 
    
   # def onchange_req_id(self, cr, uid, ids, req_id):
    #    inst = self.pool.get('data.collect').browse(cr, uid, 1)
	#req = self.pool.get('question.req').browse(cr, uid, ids)
       # service_obj = self.pool.get('data.collect.line')
       # print inst
       # temp = ''
       # temp=str(ids)

       # print temp[1:len(temp)-2]

        #for i in inst.data_line:

	#		service_obj.create(cr, uid,{
	#			'quest_id': i.req.name,
	#			'dc_id':int(temp[1:len(temp)-2]),
	#				})
        
        #return True
##########################################itaracode##############################################
    def onchange_req_id(self, cr, uid, ids, req_id):

	print '-------------------------------------------------------------------------------------------------',ids
        req_obj=self.pool.get('category.req').browse(cr, uid, ids, context=None)
        data_ids=self.pool.get('data.collect.line').search(cr, uid, [('requirement_id', '=', ids)])
        spec_obj2=self.pool.get('data.collect.line')
        for spec_id in data_ids:
            spec_obj=self.pool.get('data.collect.line').browse(cr, uid, spec_id, context=None)
            #print spec_obj.notes
            spec_obj2.create(cr, uid,{
                'quest_id': spec_obj.quest_id.id,
                'dc_id': ids[0],
                'yesno': spec_obj.yesno,
                
                'remark': spec_obj.remark,
            })
            #print spec_obj.id
        return False
        
###################################################################################################
data_collect()

class data_collect_line(osv.osv):
    
    _name = "data.collect.line"

  
    _columns = {
    'name':fields.char('Name', size=64 ),
    'dc_id':fields.many2one('data.collect', 'Data Collection Line'),  
    'quest_id': fields.many2one('question.req', 'Questionnaire'),
    'remark':fields.char('Remarks', size=68),
    'yesno': fields.selection([('Yes','Yes '),('No', 'No')], 'Status'),
    'requirement_id' : fields.many2one('category.req','Questionnaire'),
    'data_id' : fields.many2one('category.req','Questionnaire'),
	    
    }       
data_collect_line()

class category_req(osv.osv):
    _name="category.req"
    _description = ""    
    _columns = {
            'name': fields.char('Requirements', size=64),
            'code': fields.char('Code', size=6),  
            'req_ids': fields.one2many('data.collect.line', 'requirement_id', 'Questionnaire Lines'),
           
	    
             
      }
category_req()

class question_req(osv.osv):
    _name="question.req"
    _description = ""    
    _columns = {
            'name': fields.char('Questionnaire', size=250),
            'code': fields.char('Code', size=6), 
	   # 'select_req': fields.many2many('data.collect', 'data_collect_rel', 'categ_id', 'req_id', 'Select Multi Requirements') 
      }
question_req()


