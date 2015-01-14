from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
# from z3c.relationfield.schema import RelationChoice, RelationList
# from plone.formwidget.contenttree import ObjPathSourceBinder

from cpma.dexteritycontent import MessageFactory as _


alignments = SimpleVocabulary(
    [SimpleTerm(value=u'left', title=_(u'Left')),
     SimpleTerm(value=u'right', title=_(u'Right')),
    ])


class IEasyImages(form.Schema):
    """
       Marker/Form interface for Easy Images
    """

    form.fieldset(
                'decoration',
                label=_(u'Decoration'),
                fields=('imageone', 'imagetwo', 'image_align', 'text_wrap'),
            )

    imageone = namedfile.NamedBlobImage(
            title=_(u'Image One'),
            description=_(u'Optional. Upload a GIF, JPG or PNG image to illustrate or decorate the page.'),
            required=False,
        )

    imagetwo = namedfile.NamedBlobImage(
            title=_(u'Image Two'),
            description=_(u'Optional. Upload a GIF, JPG or PNG image to illustrate or decorate the page.'),
            required=False,
        )

    form.widget(image_align="z3c.form.browser.radio.RadioFieldWidget")
    image_align = schema.Choice(
                title=_(u"Image Alignment"),
                description=_(u'On which side of the content area should these images be placed?'),
                vocabulary=alignments,
                required=False,
                default=u'left',
            )

    text_wrap = schema.Bool(
            title=_(u'Text Wrap'),
            description=_(u'Should text wrap around the images? If not, it will be placed below the images. (Note: if wrap is off and alignment is "Right", the image will be centered.)'),
            default=False,
        )


alsoProvides(IEasyImages, IFormFieldProvider)

# def context_property(name):
#     def getter(self):
#         return getattr(self.context, name)
#     def setter(self, value):
#         setattr(self.context, name, value)
#     def deleter(self):
#         delattr(self.context, name)
#     return property(getter, setter, deleter)

# class EasyImages(object):
#     """
#        Adapter for Easy Images
#     """
#     implements(IEasyImages)
#     adapts(IDexterityContent)

#     def __init__(self,context):
#         self.context = context

#     # -*- Your behavior property setters & getters here ... -*-
