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
             
      }
med_question_pack()

class med_question_pack_line(osv.osv):
    _name="med.question.pack.line"
    _desctiption=""
    _columns={
        'pack_id': fields.many2one('med.question.pack', 'Pack_line'),
        'question_id': fields.many2one('med.question', 'questions'),
        'remark':fields.char('Remarks', size=68),
        'yesno': fields.selection([('Yes','Yes '),('No', 'No')], 'Status'),
    }
med_question_pack_line()
    
class med_question(osv.osv):
    _name="med.question"
    _description = ""    
    _columns = {
            'name': fields.char('Questionnaire', size=250),
            'code': fields.char('Code', size=6), 
            'yesno': fields.selection([('Yes','Yes '),('No', 'No')], 'Status'),
            'remark':fields.char('Remarks', size=68),
            'q_id': fields.many2one('med.question.pack','Question_link'),
            #'quest_sur_id':fields.many2one('general.medical.survey', 'qes')
            # 'select_req': fields.many2many('data.collect', 'data_collect_rel', 'categ_id', 'req_id', 'Select Multi Requirements') 
      }
med_question()
