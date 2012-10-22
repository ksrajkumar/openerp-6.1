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

class general_medical_survey(osv.osv):
    _name="general.medical.survey"
    _description="Medical Survey for Customer"
    _columns={
     'name':fields.many2one('res.users', 'Name'),
     'quest_pack_id':fields.many2one('med.question.pack','Questions'),
     #'every_quest_id':fields.many2many('med.question','med_quest_rel','quest_code','q_id','Questions'),
     'med_line':fields.one2many('general.medical.survey.line', 'med_line_id', 'Every Question'),
     'age':fields.char('Age',size=24),
     'telephone':fields.char('Telephone',size=64),
     'weight':fields.char('Weight',size=24),
     'height':fields.char('Height',size=64),
     'approve_diet':fields.selection([('yes','Yes'),('no','No')],'Approve for diet?'),
     'health_ques':fields.selection([('yes','Yes'),('no','No'),], 'Are you generally healty person?'),
     'wealth_ques':fields.selection([('yes','Yes'),('no','No'),], 'Do you take medication regularly'),
     'medicine_name':fields.char('Medicine Name',size=128),
     'medicine_what':fields.char('Medicine for what',size=128),
     'med_for_depression':fields.selection([('yes','Yes'),('no','No'),],'Medicine for Depression?'),
     'med_for_dep_name':fields.char('Medicine for Depression name',size=128),
     'med_for_dep_amt':fields.char('Medicine for Depression amount', size=128),
    
    }
    
    _defaults={
        'age':lambda *a:'0',
        'telephone':lambda *a:'+91-'
    } 

    def onchange_question_pack(self,cr, uid, ids, quest_pack_id):
        dc = self.browse(cr, uid, ids)
        print dc, "############################################3", len(dc),
        if dc[0].quest_pack_id:
            if dc[0].quest_pack_id:
                print dc[0].quest_pack_id,"%%%%%%%%%%%%%%%%%%%%%%%"
                brow_quest_pack=self.pool.get('med.question.pack').browse(cr, uid, dc[0].quest_pack_id.id)
                print brow_quest_pack,"LOVLOV", "______", brow_quest_pack.pack_line
                for i in brow_quest_pack.pack_line:
                    print i.question_id,"&&&&&&&&&&&&&&&&&&&&&&",i.yesno, i.remark
                    self.pool.get('general.medical.survey.line').create(cr, uid,
                       {'questions_id':i.question_id.id,
                        'yesno':i.yesno,
                        'remark':i.remark,
                        'med_line_id':dc[0].id
                        }
                    )
        else:
            raise osv.except_osv(_('Warning'), _("Please Save the record !"))
            
        return True
        #print name,"oopopooooooooooooooo"
        #self.write(cr, uid, ids, {})
        #x=self.browse(cr, uid, ids, context={})
        #print x, "XXXXXXXXXXXXXXXXXXXXXXXXXXx"
        #for o in self.browse(cr, uid, ids, context={}):
         #   print o,"**********************"
            #dc = self.browse(cr, uid, ids, context={})
        #return super(general_medical_survey, self).create(cr, user, vals, context)#self.write(cr, uid, ids, {})

general_medical_survey()


class general_medical_survey_line(osv.osv):
    _name="general.medical.survey.line"
    _description=" "
    _columns= {
        'med_line_id':fields.many2one('general.medical.survey','General medical'),
        'questions_id':fields.many2one('med.question','Qussss'),
        'yesno':fields.selection([('Yes','Yes '),('No', 'No')], 'Status'),
        'remark':fields.char("Remarks",size=256)
    
    }
    
general_medical_survey_line()
