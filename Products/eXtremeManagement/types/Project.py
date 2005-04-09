from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseFolderSchema

class Project(BaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'folder_icon.gif'
    meta_type             = 'Project'
    archetype_name        = 'Project'
    product_meta_type     = 'Project'
    immediate_view        = 'folder_listing'
    default_view          = 'folder_listing'
    allowed_content_types = (['Iteration',])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/folder_listing',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Project, PROJECTNAME)


