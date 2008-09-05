from Products.Five.browser import BrowserView
from zope import component
from datetime import date
from xm.charting import gantt
from xm.charting import model as chmodel


def pydate(dt):
    if dt is not None:
        return date(dt.year(), dt.month(), dt.day())
    return None


class GanttView(BrowserView):

    project_crit = dict(portal_type='Project',
                        sort_on='getObjPositionInParent')
    iteration_crit = dict(portal_type='Iteration',
                          review_state=('in-progress', 'new'),
                          sort_on='getObjPositionInParent')
    task_crit = dict(portal_type='Task')

    def __init__(self, context, request):
        self.context = context
        self.request = request

        portal_state = component.getMultiAdapter((context, request),
                                                 name=u'plone_portal_state')
        portal = portal_state.portal()
        self._search = portal.portal_catalog

    def _get_work_hours(self, itbrain):
        hours = {}
        for taskbrain in self._search(path=itbrain.getPath(),
                                      **self.task_crit):
            h = float(taskbrain.estimate) / float(len(taskbrain.getAssignees))
            for x in taskbrain.getAssignees:
                cur = hours.get(x, 0.0) + h
                hours[x] = cur
        return hours

    def _get_durations(self, prjbrain):
        durations = []
        for itbrain in self._search(path=prjbrain.getPath(),
                                    **self.iteration_crit):

            # getting object here due to end/start not being in indexes
            it = itbrain.getObject()
            d = chmodel.Duration(itbrain.Title,
                                 pydate(it.getStartDate()),
                                 pydate(it.getEndDate()))

            # finish getting the work hours bottom half of the chart
            # working
            d.work_hours = self._get_work_hours(itbrain)
            durations.append(d)

        return durations

    def _get_projects(self):
        projects = []
        # TODO: investigate *just* using indexes
        for prjbrain in self._search(**self.project_crit):
            durations = self._get_durations(prjbrain)
            if len(durations) == 0:
                continue

            # getting object here due to having to get list of project
            # members
            project = prjbrain.getObject()

            dg = chmodel.DurationGroup(prjbrain.Title)
            dg._iterations += durations
            projects.append(dg)

        return projects

    def __call__(self):
        return gantt.generate_chart(self._get_projects())
