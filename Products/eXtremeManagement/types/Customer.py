from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseSchema + DescriptionSchema + CustomerSchema 

class Customer(BaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'group_icon.gif'
    meta_type             = 'Customer'
    archetype_name        = 'Customer'
    product_meta_type     = 'Customer'
    immediate_view        = 'customer_view'
    default_view          = 'customer_view'
    allowed_content_types = (['ProjectMember',])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/customer_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'},
              )

registerType(Customer, PROJECTNAME)

