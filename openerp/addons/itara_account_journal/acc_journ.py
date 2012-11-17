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

class acc_journ(osv.osv):
    _inherit = "account.journal"
    _columns={
      'cheque':fields.boolean("Cheque"),
    }
    
acc_journ()


class acct_voucher(osv.osv):
    _inherit = "account.voucher"
    _columns={
    'cheque':fields.boolean("Cheque"),
    'credit_card':fields.boolean("Credit Card"),
    'cheque_clear':fields.boolean("Cheque Cleared"),
    'cheque_no':fields.char("Cheque Number", size=248),
    'cheque_date':fields.date("Cheque Date"),
    'bank_name':fields.char('Bank Name',size=256),
    
    'cc_name':fields.char('Cardholders Name', size=32,),
    'cc_b_addr_1':fields.char('Billing Address1', size=32,),
    'cc_b_addr_2':fields.char('Billing Address2', size=32,),
    'cc_city': fields.char('City', size=32,),
    'cc_state':fields.char('State', size=32,),
    'cc_zip':fields.char('Postal/Zip', size=32,),
    'cc_country':fields.char('Country', size=32,),
    'cc_number':fields.char('Credit Card Number', size=256),
    'cc_v':fields.char('Card Code Verification', size=32,),
    'cc_e_d_month':fields.char('Expiration Date MM', size=32),
    'cc_e_d_year':fields.char('Expiration Date YY', size=32),
    'cc_comment':fields.char('Comment', size=128,),
    'cc_auth_code':fields.char('Authorization Code', size=32),
    }
    
    
    
acct_voucher()
