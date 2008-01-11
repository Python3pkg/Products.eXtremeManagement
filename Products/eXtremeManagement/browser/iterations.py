from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import ImplicitAcquisitionWrapper
from Products.PageTemplates.PageTemplate import PageTemplate

from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from xm.booking.timing.interfaces import IActualHours
from xm.booking.timing.interfaces import IEstimate
from Products.eXtremeManagement.content.Iteration import \
    UNACCEPTABLE_STATUSES as UNACCEPTABLE_STORY_STATUSES
from Products.eXtremeManagement.utils import formatTime
from Products.eXtremeManagement.utils import getStateSortedContents


def degrade_headers(html, howmuch=2):
    """
      >>> degrade_headers('<h1>Hello</h1><h2>World</h2>')
      '<h3>Hello</h3><h4>World</h4>'
      >>> degrade_headers('<h0>Funny things</h0><h2>as input</h2>')
      '<h2>Funny things</h2><h4>as input</h4>'
    """
    for number in range(6, -1, -1):
        html = html.replace('<h%s' % number, '<h%s' % (number + howmuch))
        html = html.replace('</h%s>' % number, '</h%s>' % (number + howmuch))
    return html


class IterationView(XMBaseView):
    """Simply return info about a Iteration.
    """

    details_template = PageTemplate()
    details_template.write("""
    <metal:define metal:use-macro='context/global_defines/macros/defines' />
    <h0 tal:content='context/Title'>Story title</h0>
    <metal:use use-macro='context/story_view/macros/details' />
    """)

    def main(self):
        """Get a dict with info from this Context.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')
        anno = IActualHours(context, None)
        if anno is not None:
            actual = anno.actual_time
        else:
            # Should not happen (tm).
            actual = -99.0
        est = IEstimate(context, None)
        if est is not None:
            estimate = est.estimate
        else:
            # Should not happen (tm).
            estimate = -99.0

        # Size estimate.  We may want to do this smarter.
        filter = dict(portal_type='Story')
        items = context.getFolderContents(filter)
        size_estimate = sum([item.size_estimate for item in items
                             if item.size_estimate is not None])

        review_state = workflow.getInfoFor(context, 'review_state')
        if review_state in ['completed', 'invoiced']:
            budget_left = None
        else:
            budget_left = self.actual_budget_left()
        if budget_left is not None:
            budget_left = formatTime(budget_left)
        ploneview = context.restrictedTraverse('@@plone')
        if hasattr(context, 'getManHours'):
            manhours = context.getManHours()
        else:
            manhours = None
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            man_hours = manhours,
            start_date = ploneview.toLocalizedTime(context.getStartDate()),
            end_date = ploneview.toLocalizedTime(context.getEndDate()),
            estimate = formatTime(estimate),
            size_estimate = size_estimate,
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            review_state = review_state,
            budget_left = budget_left
            )
        return returnvalue

    def stories(self):
        context = aq_inner(self.context)
        filter = dict(portal_type='Story',
                      sort_on='getObjPositionInParent')
        items = context.getFolderContents(filter)
        storybrains = getStateSortedContents(items)

        story_list = []

        for storybrain in storybrains:
            info = self.storybrain2dict(storybrain)
            info['details'] = self.render_details(storybrain)
            story_list.append(info)

        return story_list

    def storybrain2dict(self, brain):
        """Get a dict with info from this story brain.
        """
        context = aq_inner(self.context)
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')
        catalog = getToolByName(context, 'portal_catalog')

        # compute progress percentage
        is_completed = (review_state_id == 'completed')
        if is_completed:
            progress = 100
        else:
            estimated = brain.estimate
            actual = brain.actual_time
            progress = self.get_progress_perc(actual, estimated)

        # compute open task count
        searchpath = brain.getPath()
        filter = dict(portal_type=['Task', 'PoiTask'],
                      path=searchpath)
        unfinished_states = ('open', 'to-do', )
        filter['review_state'] = unfinished_states
        open_tasks = len(catalog.searchResults(**filter))

        # compute completed task count
        finished_states = ('completed', )
        filter['review_state'] = finished_states
        completed_tasks = len(catalog.searchResults(**filter))

        estimate = brain.estimate
        actual = brain.actual_time
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            raw_estimate = estimate,
            estimate = formatTime(estimate),
            size_estimate = brain.size_estimate,
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            progress = progress,
            review_state = review_state_id,
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Story'),
            is_completed = is_completed,
            open_tasks = open_tasks,
            completed_tasks = completed_tasks,
        )
        return returnvalue

    def todo_tasks(self):
        return self.state_tasks('to-do')

    def open_tasks(self):
        return self.state_tasks('open')

    def state_tasks(self, state):
        context = aq_inner(self.context)
        context.REQUEST.form['state'] = state
        view = context.restrictedTraverse('@@mytask_details')
        result = view.tasklist()
        return result

    def render_details(self, storybrain):
        story = storybrain.getObject()
        info = story.restrictedTraverse('@@story').main()
        rendered = ImplicitAcquisitionWrapper(self.details_template, story)()
        return degrade_headers(rendered)

    def story_titles_not_startable(self):
        context = aq_inner(self.context)

        filter = dict(portal_type='Story',
                      sort_on='getObjPositionInParent')
        items = context.getFolderContents(filter)

        stories = [x.Title
                   for x in items
                   if x.review_state in UNACCEPTABLE_STORY_STATUSES]
        return ', '.join(stories)

    def get_progress_perc(self, part, total):
        """Get progress percentage of part compared to total.

        Set up some test context.

        >>> from zope.publisher.browser import TestRequest
        >>> class SimpleContext(object):
        ...     portal_properties = None
        >>> context = SimpleContext()
        >>> request = TestRequest()
        >>> view = IterationView(context, request)

        Test a part that is larger than the total:

        >>> view.get_progress_perc(3, 1)
        300

        We do not want to go over 100 percent though, so we have a
        setting in a property sheet that we use.  Set up a test
        environment for that.

        >>> xm_properties = dict(maximum_not_completed_percentage = 90)
        >>> portal_properties = dict()
        >>> portal_properties['xm_properties'] = xm_properties
        >>> view.context.portal_properties = portal_properties

        Now try again.

        >>> view.get_progress_perc(3, 1)
        90

        Code that uses this method can choose to show 100 percent to
        the user, for instance because a Story has the status
        'completed'.  But that is not our responsibility.

        Now for some more tests.

        >>> view.get_progress_perc(0, 1)
        0
        >>> view.get_progress_perc(10, 100)
        10
        >>> view.get_progress_perc(1, 3)
        33
        >>> view.get_progress_perc(1, 3.0)
        33

        """
        context = self.context
        if total > 0:
            try:
                percentage = int(round(part/float(total)*100))
            except TypeError:
                return '??'
            portal_properties = getToolByName(context, 'portal_properties',
                                              None)
            if portal_properties is None:
                return percentage
            xm_props = portal_properties.get('xm_properties', None)
            if xm_props is None:
                return percentage
            max_percentage = xm_props.get('maximum_not_completed_percentage',
                                          90.0)
            if percentage > max_percentage:
                return max_percentage
            return percentage
        return 0

    def actual_budget_left(self):
        context = self.context
        project = aq_parent(aq_inner(self.context))
        hours_left = project.getBudgetHours()
        if not hours_left:
            return None
        contentfilter = dict(portal_type = 'Iteration')
        iteration_brains = project.getFolderContents(contentfilter)
        for brain in iteration_brains:
            iteration = brain.getObject()
            hours_left -= IActualHours(brain.getObject()).actual_time
        return hours_left
