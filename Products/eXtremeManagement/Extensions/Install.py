import transaction
from Products.CMFCore.utils import getToolByName

PRODUCT_DEPENDENCIES = ('Poi',)

EXTENSION_PROFILES = ('Products.eXtremeManagement:default',)

def install(self, reinstall=False):
    """Install a set of products (which themselves may either use Install.py
    or GenericSetup extension profiles for their configuration) and then
    install our extension profile.

    We do this because it is not possible to install other products during
    the execution of an extension profile (i.e. we cannot do this during
    the importVarious step for this profile).
    """

    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')

    for product in PRODUCT_DEPENDENCIES:
        if reinstall and portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.reinstallProducts([product])
            transaction.savepoint()
        elif not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()

    portal_setup.runAllImportStepsFromProfile('profile-Products.eXtremeManagement:default',
                                              purge_old=False)
    product_name = extension_id.split(':')[0]
    portal_quickinstaller.notifyInstalled(product_name)
    transaction.savepoint()