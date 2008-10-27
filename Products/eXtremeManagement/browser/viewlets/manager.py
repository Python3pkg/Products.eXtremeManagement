from Acquisition import Explicit
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from interfaces import ISimpleTaskList
from interfaces import ISimpleStoryList
from interfaces import IStoryDetails


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

    def iteration_icon(self):
        # the (1) is needed otherwise getIcon() will return
        # 'plone/iteration_icon.gif', which is wrong. The template
        # will add the $portal_url prefix
        return self.iteration_object.getIcon(1)

    def update(self):
        pass


class StoryDetailsProvider(Explicit):
    implements(IStoryDetails)
    template = ViewPageTemplateFile('templates/manage_story_details.pt')
    render = template
    story_object = None
    number_of_comments = 0

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        uid = request.get('uid')
        if uid is not None:
            brains = getToolByName(context, 'uid_catalog')(UID=uid)
            self.story_object = brains[0].getObject()
            pd = getToolByName(context, 'portal_discussion')
            replies = pd.getDiscussionFor(self.story_object).getReplies()
            self.number_of_comments = len(replies)
        self.__parent__ = view

    def update(self):
        pass
