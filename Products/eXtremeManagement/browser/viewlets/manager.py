from Acquisition import Explicit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from interfaces import ISimpleTaskList
from interfaces import ISimpleStoryList
from zope.interface import implements


class SimpleTaskListManager(Explicit):
    implements(ISimpleTaskList)
    template = ViewPageTemplateFile('templates/manage_simple_tasklist.pt')
    render = template
    realtasks = None
    show_story = False

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

        try:
            self.tasks = view.tasklist()
        except AttributeError:
            self.tasks = None

    def update(self):
        pass


class SimpleStoryListManager(Explicit):
    implements(ISimpleStoryList)
    template = ViewPageTemplateFile('templates/manage_simple_storylist.pt')
    render = template
    realstories = None
    iteration_object = None
    iteration_dict = None
    show_iteration = False
    show_task_count = False
    show_progress = False
    show_totals = False
    iteration_number = '1'

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        pass
