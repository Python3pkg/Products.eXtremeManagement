# Original workflow id/title: eXtreme_story_workflow/eXtreme Story Workflow
# Date: 2005/04/15 10:54:53.690 GMT+2
#
# WARNING: this dumps does NOT contain any scripts you might have added to
# the workflow, IT IS YOUR RESPONSABILITY TO MAKE BACKUPS FOR THESE SCRIPTS.
#
# No script detected in this workflow
# 
"""
Programmatically creates a workflow type
"""
__version__ = "$Revision: 1.1.1.1 $"[11:-2]

from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

def setupExtreme_story_workflow(wf):
    "..."
    wf.setProperties(title='eXtreme Story Workflow')

    for s in ['in-progress', 'completed', 'assigned', 'estimated', 'open', 'pending']:
        wf.states.addState(s)
    for t in ['activate', 'complete', 'submit', 'unassign', 'retract', 'estimate', 'assign', 'improve']:
        wf.transitions.addTransition(t)
    for v in ['action', 'review_history', 'actor', 'comments', 'time']:
        wf.variables.addVariable(v)
    for l in ['reviewer_queue']:
        wf.worklists.addWorklist(l)
    for p in ('Access contents information', 'Modify portal content', 'View'):
        wf.addManagedPermission(p)
        

    ## Initial State
    wf.states.setInitialState('open')

    ## States initialization
    sdef = wf.states['in-progress']
    sdef.setProperties(title="""Content is in-progress""",
                       transitions=('complete',))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager'])

    sdef = wf.states['completed']
    sdef.setProperties(title="""Content is completed""",
                       transitions=('improve',))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager'])

    sdef = wf.states['assigned']
    sdef.setProperties(title="""Content is assigned""",
                       transitions=('activate', 'unassign'))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager', 'Owner'])

    sdef = wf.states['estimated']
    sdef.setProperties(title="""Content is estimated""",
                       transitions=('assign', 'retract'))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager', 'Owner'])

    sdef = wf.states['open']
    sdef.setProperties(title="""Visible for customers and employees and editable by owner and employees""",
                       transitions=('submit',))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Customer', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Manager', 'Owner'])

    sdef = wf.states['pending']
    sdef.setProperties(title="""Content is waiting for estimation""",
                       transitions=('estimate', 'retract'))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Customer', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Manager', 'Owner'])


    ## Transitions initialization
    tdef = wf.transitions['activate']
    tdef.setProperties(title="""Activate content - content is in-progress""",
                       new_state_id="""in-progress""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Activate""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    tdef = wf.transitions['complete']
    tdef.setProperties(title="""Employee member(s) completes content""",
                       new_state_id="""completed""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Complete""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    tdef = wf.transitions['submit']
    tdef.setProperties(title="""Member requests publishing""",
                       new_state_id="""pending""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Submit""",
                       actbox_url="""%(content_url)s/content_submit_form""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Request review'},
                       )

    tdef = wf.transitions['unassign']
    tdef.setProperties(title="""Content is unassigned""",
                       new_state_id="""estimated""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Unassign""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    tdef = wf.transitions['retract']
    tdef.setProperties(title="""Customer retracts content""",
                       new_state_id="""open""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Retract""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    tdef = wf.transitions['estimate']
    tdef.setProperties(title="""Employee member estimates content""",
                       new_state_id="""estimated""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Estimate""",
                       actbox_url="""%(content_url)s/content_publish_form""",
                       actbox_category="""workflow""",
                       props={'guard_permissions': 'Review portal content'},
                       )

    tdef = wf.transitions['assign']
    tdef.setProperties(title="""Content is assigned""",
                       new_state_id="""assigned""",
                       trigger_type=0,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Assign""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    tdef = wf.transitions['improve']
    tdef.setProperties(title="""Retract content to improve""",
                       new_state_id="""in-progress""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Improve""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    ## State Variable
    wf.variables.setStateVar('review_state')

    ## Variables initialization
    vdef = wf.variables['action']
    vdef.setProperties(description="""The last transition""",
                       default_value="""""",
                       default_expr="""transition/getId|nothing""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['review_history']
    vdef.setProperties(description="""Provides access to workflow history""",
                       default_value="""""",
                       default_expr="""state_change/getHistory""",
                       for_catalog=0,
                       for_status=0,
                       update_always=0,
                       props={'guard_permissions': 'Request review; Review portal content'})

    vdef = wf.variables['actor']
    vdef.setProperties(description="""The ID of the user who performed the last transition""",
                       default_value="""""",
                       default_expr="""user/getId""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['comments']
    vdef.setProperties(description="""Comments about the last transition""",
                       default_value="""""",
                       default_expr="""python:state_change.kwargs.get('comment', '')""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['time']
    vdef.setProperties(description="""Time of the last transition""",
                       default_value="""""",
                       default_expr="""state_change/getDateTime""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    ## Worklists Initialization
    ldef = wf.worklists['reviewer_queue']
    ldef.setProperties(description="""Reviewer tasks""",
                       actbox_name="""Pending (%(count)d)""",
                       actbox_url="""%(portal_url)s/search?review_state=pending""",
                       actbox_category="""global""",
                       props={'guard_permissions': 'Review portal content', 'var_match_review_state': 'pending'})


def createExtreme_story_workflow(id):
    "..."
    ob = DCWorkflowDefinition(id)
    setupExtreme_story_workflow(ob)
    return ob

addWorkflowFactory(createExtreme_story_workflow,
                   id='eXtreme_story_workflow',
                   title='eXtreme Story Workflow')


