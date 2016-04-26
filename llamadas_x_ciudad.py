# -*- coding: utf-8 -*-
import datetime
import math
import time
from operator import attrgetter

from openerp.exceptions import Warning
from openerp import tools
from openerp.osv import fields, osv 
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)


class llamadas_x_ciudad(osv.osv_memory):

    _name = 'llamadas.x.ciudad'
    _columns = {

        'name': fields.char( 'Nombre'),
        'section_id': fields.many2one('crm.case.section', 'Section'),
        'city': fields.char( 'Ciudad'),
        'user_id': fields.many2one('res.users', 'user'),
        
        'city_id': fields.many2one('res.country.state.city', 'City'),
        }
    _defaults= {
    }
   

    def set_phonecalls(self, cr, uid,ids,context=None):
        data=self.read(cr, uid, ids[0], ['section_id','city','user_id','name'])
        partner_ob=self.pool.get('res.partner')
        section_ob=self.pool.get('crm.case.section')
        phonecall_ob=self.pool.get('crm.phonecall')

        
        partners_ids=partner_ob.search(cr,uid, [('city', 'ilike', data['city']),'|',('mobile','!=',None),('phone','!=',None)],offset=0,limit=2000)
        days=1
        count=0
        for partner in partner_ob.browse(cr,uid,partners_ids):
            _logger.info('city %r ' ,partner['city'])
            count +=1 
            phonecall={}
            phonecall['name']=data['name'] 
            phonecall['partner_id']=partner['id']
            phonecall['partner_mobile']=partner['mobile']
            phonecall['partner_phone']=partner['phone']
            phonecall['date']=datetime.datetime.today() +datetime.timedelta(days=days)
            phonecall['section_id']=data['section_id'][0]
            phonecall['user_id']=data['user_id'][0]
            res_id=phonecall_ob.create(cr,uid,phonecall,context=None)
            if count > 40 :
                days +=1
                count =0 





