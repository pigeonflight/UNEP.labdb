from operator import itemgetter

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite

from Products.CMFCore.utils import getToolByName


class Countries(object):
    """Vocabulary factory for available countries on the labs.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        portal_catalog = getToolByName(site, 'portal_catalog', None)
        brains = portal_catalog.searchResults(
                   portal_type=["UNEP.labdb.lab",] 
                    )
        #filter out country codes
        countries = [country for country in brains if len(country) > 2]
        terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in countries ]
        return SimpleVocabulary(terms)
          

#AvailableContentLanguageVocabularyFactory = Countries()
