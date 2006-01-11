# File: testProjectFolder.py
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
# Test-cases for class(es) ProjectFolder
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testProjectFolder(eXtremeManagementTestCase):
    """ test-cases for class(es) ProjectFolder
    """

    ##code-section class-header_testProjectFolder #fill in your manual code here
    ##/code-section class-header_testProjectFolder

    def afterSetUp(self):
        """
        """
        pass

    # Manually created methods
    def test_projectFolder(self):
        """Test adding a ProjectFolder in the portal root
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects')
        self.portal._setObject('projects',p)
        self.failUnless( self.portal.projects.portal_type == 'ProjectFolder')



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProjectFolder))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()

