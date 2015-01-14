from five import grok
from zope.interface import alsoProvides
from zope.interface import implements
from zope import schema
from zope.component import getMultiAdapter
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder

from cpma.dexteritycontent import MessageFactory as _


@grok.provider(IContextSourceBinder)
def sponsor_types(context):
    """ populate a vocabulary with all the public page sponsors """

    terms = [
        SimpleTerm(value=u'section_sponsor', title=_(u'Section Sponsor')),
        SimpleTerm(value=u'no_sponsor', title=_(u'None')),
        ]
    portal_state = getMultiAdapter((context, context.REQUEST), name=u'plone_portal_state')
    path = "%s/sponsors" % portal_state.navigation_root_path()
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog(
        portal_type='page_sponsor',
        sort_on='sortable_title',
        review_state=('published', 'visible'),
        path=path,
        )

    for b in results:
        terms.append(SimpleTerm(value=b.getId, title=b.Title or b.getId))

    return SimpleVocabulary(terms)


class IPageSponsorship(form.Schema):
    """
       Marker/Form interface for Page Sponsorship
    """

    form.fieldset(
            'sponsorship',
            label=_(u'Page Sponsors'),
            fields=('major_sponsor', 'minor_sponsor', 'minor_sponsor2',),
        )

    major_sponsor = schema.Choice(
                title=_(u"Major Sponsor"),
                description=_(u'Choose a major sponsor.'),
                source=sponsor_types,
                required=True,
                default=u'section_sponsor',
            )

    minor_sponsor = schema.Choice(
                title=_(u"Minor Sponsor"),
                description=_(u'Choose a minor sponsor.'),
                source=sponsor_types,
                required=True,
                default=u'section_sponsor',
            )

    minor_sponsor2 = schema.Choice(
                title=_(u"Minor Sponsor 2"),
                description=_(u'Choose a second minor sponsor.'),
                source=sponsor_types,
                required=True,
                default=u'section_sponsor',
            )

alsoProvides(IPageSponsorship, IFormFieldProvider)

# def context_property(name):
#     def getter(self):
#         return getattr(self.context, name)
#     def setter(self, value):
#         setattr(self.context, name, value)
#     def deleter(self):
#         delattr(self.context, name)
#     return property(getter, setter, deleter)

# class PageSponsorship(object):
#     """
#        Adapter for Page Sponsorship
#     """
#     implements(IPageSponsorship)
#     adapts(IDexterityContent)

#     def __init__(self,context):
#         self.context = context

#     # -*- Your behavior property setters & getters here ... -*-
