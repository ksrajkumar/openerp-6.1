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

class med_question_pack(osv.osv):
    _name="med.question.pack"
    _description = ""    
    _columns = {
            'name': fields.char('Requirements', size=64),
            'code': fields.char('Code', size=6),  
            #'question_ids': fields.one2many('med.question', 'q_id', 'Questionnaire Lines'),
            'pack_line': fields.one2many('med.question.pack.line', 'pack_id', 'Question pack Lines'),
            'physical_activity_id': fields.one2many('physical.activity', 'name_id', 'Physical Activity'),
             
      }
med_question_pack()

class med_question_pack_line(osv.osv):
    _name="med.question.pack.line"
    _desctiption=""
    _columns={
        'pack_id': fields.many2one('med.question.pack', 'Pack_line'),
        'question_id': fields.many2one('med.question', 'questions'),
        'remark':fields.char('Remarks', size=68),
        'yesno': fields.selection([('Yes','Yes '),('No', 'No'),('Dont Know', 'Dont Know')], 'Status'),
    }
med_question_pack_line()
    
class med_question(osv.osv):
    _name="med.question"
    _description = ""    
    _columns = {
            'name': fields.char('Questionnaire', size=250),
            'code': fields.char('Code', size=6), 
            'yesno': fields.selection([('Yes','Yes '),('No', 'No'),('Dont Know', 'Dont Know')], 'Status'),
            'remark':fields.char('Remarks', size=68),
            'q_id': fields.many2one('med.question.pack','Question_link'),
            #'quest_sur_id':fields.many2one('general.medical.survey', 'qes')
            # 'select_req': fields.many2many('data.collect', 'data_collect_rel', 'categ_id', 'req_id', 'Select Multi Requirements') 
      }
med_question()


class physical_activity_many(osv.osv):
    _name='physical.activity.many'
    _description='Creating master for Physical Activity'
    _columns={
    'name':fields.char('Physical Activity',size=256),
    }
physical_activity_many()



class physical_activity(osv.osv):
    _name='physical.activity'
    _description='Creating master for Physical Activity'
    _columns={
    'name': fields.many2one('physical.activity.many',''),
    'name_id':fields.many2one('med.question.pack','Physical Activity'),
    }
physical_activity()
