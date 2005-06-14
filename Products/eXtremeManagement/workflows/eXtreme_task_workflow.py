# Generated by dumpDCWorkflow.py written by Sebastien Bigaret
# Original workflow id/title: eXtreme_task_workflow/eXtreme Task Workflow
# Date: 2005/06/14 10:47:09.049 GMT+2
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

def setupExtreme_task_workflow(wf):
    "..."
    wf.setProperties(title='eXtreme Task Workflow')

    for s in ['in-progress', 'completed', 'open']:
        wf.states.addState(s)
    for t in ['retract', 'activate', 'complete']:
        wf.transitions.addTransition(t)
    for v in ['action', 'time', 'comments', 'actor', 'review_history']:
        wf.variables.addVariable(v)
    for l in ['reviewer_queue']:
        wf.worklists.addWorklist(l)
    for p in ('Access contents information', 'Modify portal content', 'View', 'Change portal events'):
        wf.addManagedPermission(p)
        

    ## Initial State
    wf.states.setInitialState('open')

    ## States initialization
    sdef = wf.states['in-progress']
    sdef.setProperties(title="""Task is accepted by a user""",
                       transitions=('complete', 'retract'))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Employee', 'Manager', 'Owner'])

    sdef = wf.states['completed']
    sdef.setProperties(title="""Task is completed""",
                       transitions=())
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Employee', 'Manager', 'Owner'])

    sdef = wf.states['open']
    sdef.setProperties(title="""News task""",
                       transitions=('activate',))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Change portal events', 0, ['Employee', 'Manager', 'Owner'])


    ## Transitions initialization
    tdef = wf.transitions['retract']
    tdef.setProperties(title="""User retracts a task""",
                       new_state_id="""open""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Retract""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    tdef = wf.transitions['activate']
    tdef.setProperties(title="""Task is activated""",
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
    tdef.setProperties(title="""Task is completed""",
                       new_state_id="""completed""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Completed""",
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

    vdef = wf.variables['time']
    vdef.setProperties(description="""Time of the last transition""",
                       default_value="""""",
                       default_expr="""state_change/getDateTime""",
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

    vdef = wf.variables['actor']
    vdef.setProperties(description="""The ID of the user who performed the last transition""",
                       default_value="""""",
                       default_expr="""user/getId""",
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

    ## Worklists Initialization
    ldef = wf.worklists['reviewer_queue']
    ldef.setProperties(description="""Reviewer tasks""",
                       actbox_name="""Pending (%(count)d)""",
                       actbox_url="""%(portal_url)s/search?review_state=pending""",
                       actbox_category="""global""",
                       props={'guard_permissions': 'Review portal content', 'var_match_review_state': 'pending'})


def createExtreme_task_workflow(id):
    "..."
    ob = DCWorkflowDefinition(id)
    setupExtreme_task_workflow(ob)
    return ob

addWorkflowFactory(createExtreme_task_workflow,
                   id='eXtreme_task_workflow',
                   title='eXtreme Task Workflow')


