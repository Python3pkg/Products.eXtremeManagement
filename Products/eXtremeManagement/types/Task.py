from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseFolderSchema 

class Task(BaseContent):
    """A simple archetype"""
    schema                = schema
    content_icon          = 'document_icon.gif'
    meta_type             = 'Task'
    archetype_name        = 'Task'
    product_meta_type     = 'Task'
    immediate_view        = 'task_view'
    default_view          = 'task_view'
    allowed_content_types = ([])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/task_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Task, PROJECTNAME)


