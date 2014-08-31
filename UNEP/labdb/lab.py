from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from five import grok

from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid, Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from UNEP.labdb import MessageFactory as _

# Interface class; used to define content-type schema.

class ITelephoneRow(Interface):
    phone_number = schema.TextLine(
                              title=_(u'Number'), 
                              required=False
                              )

 
class _ILab(form.Schema, IImageScaleTraversable):
    """
    Lab Profile
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/lab.xml to define the content type.

    form.model("models/lab.xml")

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ILab(_ILab,model.Schema):
    """
    Lab Schema to include data grid fields
    """

    form.widget(telephone=DataGridFieldFactory)
    telephone= schema.List(
                title=_(u"Telephone Number(s)"),
                value_type=DictRow(
                    title=_(u"Number"), 
                    schema=ITelephoneRow,
                    required=False,                      
                    )
                )

class Lab(Container):
    grok.implements(ILab)

    # Add your class methods and properties here

#
# View class
# The view will automatically use a similarly named template in
# lab_templates.

class View(dexterity.DisplayForm):
    """ default view located at lab_view """
    grok.context(ILab)
    grok.require('zope2.View')
    grok.name('view')
