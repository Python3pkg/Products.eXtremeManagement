# File: testStory.py
#
# Copyright (c) 2006 by Zest software
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>, Maurits van Rees
<m.van.rees@zestsoftware.nl>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) Story
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.Story import Story

##code-section module-beforeclass #fill in your manual code here
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder
##/code-section module-beforeclass


class testStory(eXtremeManagementTestCase):
    """ test-cases for class(es) Story
    """

    ##code-section class-header_testStory #fill in your manual code here
    ##/code-section class-header_testStory

    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow
        self.userfolder = self.portal.acl_users
        self.userfolder._doAddUser('customer', 'secret', ['Customer'], [])
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects
        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project
        self.project.manage_addLocalRoles('customer',['Customer'])
        self.project.invokeFactory('Iteration', id='iteration')
        self.iteration = self.project.iteration
        self.iteration.invokeFactory('Story', id='story')
        self.story = self.iteration.story
        self.assertEqual(self.story.isEstimated(), False)
        self.story.setRoughEstimate(4.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task


    # from class Story:
    def test_CookedBody(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_get_progress_perc(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_generateUniqueId(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_isCompleted(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_getRawEstimate(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_getEstimate(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_getRawActualHours(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_getActualHours(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_getRawDifference(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_getDifference(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_isEstimated(self):
        """
        """
        self.setRoles(['Manager'])
        self.assertEqual(self.story.isEstimated(), True)
        self.story.setRoughEstimate(0)
        self.assertEqual(self.story.isEstimated(), False)
        self.logout()

    # from class Story:
    def test_startable(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # from class Story:
    def test_completable(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Story('temp_Story')
        ##self.folder._setObject('temp_Story', o)
        pass

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testStory))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


