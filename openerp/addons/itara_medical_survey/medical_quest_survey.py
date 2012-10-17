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

class medical_quest_survey(osv.osv):
    _name="medical.quest.survey"
    _description="Medical Survey for Customer"
    _columns={
     'cli_name':fields.many2one('res.users', 'Name'),
     'date':fields.date('Date'),
     'letter_text':fields.char('Letter Text',size=248),
     'quest_sur_id':fields.char('ID',size=24),
     'private_coach_name':fields.char('Private Coacher Name',size=264),
     'sal_per_name':fields.many2one('res.users', 'Sales Person Name'),
     'age':fields.char('Age',size=24),
     'weight':fields.char('Weight',size=64),
     'sex':fields.selection([('male','Male'),('female','Female')], 'Sex'),
     'tel_home':fields.char('Tel Home',size=64),
     'mobile':fields.char('Mobile',size=48),
     'fax':fields.char('Fax',size=128),
     'email':fields.char('Email',size=128),
     'health_fund':fields.char('Health Fund',size=128),
     'name_doctor':fields.char('Name of Doctor', size=168),
     'height':fields.char('Height',size=124),
     'reg_medication':fields.char('Regular Medication',size=168),
     
#     'approve_diet':fields.selection([('yes','Yes'),('no','No')],'Approve for diet?'),
#     'health_ques':fields.selection([('yes','Yes'),('no','No'),], 'Are you generally healty person?'),
#     'wealth_ques':fields.selection([('yes','Yes'),('no','No'),], 'Do you take medication regularly'),
#     'medicine_name':fields.char('Medicine Name',size=128),
#     'medicine_what':fields.char('Medicine for what',size=128),
#     'med_for_depression':fields.selection([('yes','Yes'),('no','No'),],'Medicine for Depression?'),
#     'med_for_dep_name':fields.char('Medicine for Depression name',size=128),
#     'med_for_dep_amt':fields.char('Medicine for Depression amount', size=128),
    
    }

medical_quest_survey()
