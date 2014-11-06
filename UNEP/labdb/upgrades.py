from Products.CMFCore.utils import getToolByName

default_profile = 'profile-UNEP.labdb:default'

def upgrade_to_1_0_1(context):
    print "Upgrading to 1.0.1"
    context.runImportStepFromProfile(default_profile, 'jsregistry')
