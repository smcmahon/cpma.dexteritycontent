from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.dexterity.interfaces import IDexterityContainer

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from cpma.dexteritycontent import MessageFactory as _


# Interface class; used to define content-type schema.

class Istandarddoc(form.Schema, IImageScaleTraversable):
    """
    Standard Doc
    """

    body = RichText(title=_(u"Body Text"))


class DocSupport(grok.View):
    # A support view to allow us to cook body content
    # with proper relative URL translation

    grok.context(IDexterityContainer)
    grok.require('zope2.View')

    def cooked_body(self):
        body = getattr(self.context, 'body')
        if body:
            return body.output_relative_to(self.context)
        return u''

    def render(self):
        return u""

