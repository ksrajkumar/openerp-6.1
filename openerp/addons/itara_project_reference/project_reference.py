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
from osv import osv, fields
import pooler
import re
from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
import netsvc
from datetime import date


def _links_get(self, cr, uid, context=None):
    obj = self.pool.get('res.request.link')
    ids = obj.search(cr, uid, [], context=context)
    res = obj.read(cr, uid, ids, ['object', 'name'], context)
    return [(r['object'], r['name']) for r in res]
    
class project_reference(osv.osv):
    _inherit = "project.task"

    _columns={
    'ref_partner_id':fields.many2one('res.partner', 'Partner Ref.'),
    'ref_doc1':fields.reference('Document Ref 1', selection=_links_get, size=128 ),
    'ref_doc2':fields.reference('Document Ref 2', selection=_links_get, size=128 ),
    }

project_reference()




class res_request_link(osv.osv):
    _name = 'res.request.link'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'object': fields.char('Object', size=64, required=True),
        'priority': fields.integer('Priority'),
    }
    _defaults = {
        'priority': lambda *a: 5,
    }
    _order = 'priority'
res_request_link()
