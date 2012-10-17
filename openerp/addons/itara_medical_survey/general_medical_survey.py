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

general_medical_survey()
