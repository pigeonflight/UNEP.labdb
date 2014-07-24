# -*- coding: utf-8 -*-
import json
from plone import api
from Products.CMFPlone.interfaces import constrains
from UNEP.labdb.importer import LabImporter
from UNEP.labdb.lab import ILab
from zope.schema import getFieldsInOrder


def setupVarious(context):

    if context.readDataFile('UNEP.labdb.marker.txt') is None:
        return

    portal = api.portal.get()
    #request = getattr(portal, 'REQUEST', None)
    
    #check for the existence of meetings and documents
    #
    if not api.content.get('/labs'):
        labs = api.content.create(
            portal,
            'Folder',
            id='labs',
            title='Labs'
        )
        api.content.transition(labs, transition='publish')
        behavior = constrains.ISelectableConstrainTypes(labs)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(['UNEP.labdb.lab', 'Folder'])
        behavior.setImmediatelyAddableTypes(['UNEP.labdb.lab', 'Folder'])

        _fields = getFieldsInOrder(ILab)
        fields = [(item[0],item[0].title().replace('_',' '))
                        for item in _fields]
        data_map = dict(fields)
        data_map['title']=u'Lab Name' 
        data_map['cep_involvement_details']=u'CEP Involvement'
        data_map['telephone & email']=u'Telephone & Email' 

        inv_data_map = {v:k for k, v in data_map.items()}
        skip = ['Address','Established']
        li = LabImporter(portal)
        li.create_lab_folder()

        # create all the labs
        _lab_data = context.readDataFile('labdata.json')
        lab_data = json.loads(_lab_data)
        for source_lab in lab_data:
            lab_ = li.create_lab(source_lab['Lab Name'])
            # iterate over each attribute an set it
            for key in source_lab.keys():
                if key not in skip: 
                    value = source_lab[key] 
                    if key == 'Lab Type':
                        value = value.split('\n')
                    if key == 'Country':
                        value = value.title().replace('And','&')
                    inv_key = inv_data_map[key] 
                    setattr(lab_,inv_key,value)
