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


{
    'name': ' Adding DOb and age in CRM-Lead Form',
    'version': '1.0',
    'category': 'Generic Modules',
    'author': 'Rajkumar',
    'website': 'http://www.openerp.com',
    'depends': ['product','base','crm','sale_crm'],
    'init_xml': [ ],
    'update_xml': ['dms_crm_lead.xml'],
    'demo_xml': [ ],
    'test': [ ],
    'installable': True,
    'active': False,
    'description': """ Adding fields in CRM lead form """
  }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
