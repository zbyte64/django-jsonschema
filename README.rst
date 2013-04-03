

============
Introduction
============

django-jsonschema converts Django Forms into JSON Schema compatibile representations

------------
Requirements
------------

* Python 2.6 or later
* Django 1.4 or later


=====
Usage
=====

To convert a form to a JSON Schema::

    from djangojsonschema.jsonschema import DjangoFormToJSONSchema
    
    schema_repr = DjangoFormToJSONSchema().convert_form(MyForm)


To embed a JSON Schema as a form field::

    from djangojsonschema.forms import JSONSchemaField
    
    #where schema is a python dictionay like schema_repr in the first exmaple
    
    class MyForm(forms.Form):
        subfield = JSONSchemaField(schema=schema)
    
    form = MyForm(data={'subfield':'<json encoded value>'})
    form.validate() #will validate the subfield entry against schema
    form['subfield'].as_widget() #will render a textarea widget with a data-schemajson attribute
