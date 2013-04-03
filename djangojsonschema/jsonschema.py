#TODO find a better submodule name
from django.forms import widgets


class DjangoFormToJSONSchema(object):
    def convert_form(self, form, json_schema=None):
        if json_schema is None:
            json_schema = {
                #'title':dockit_schema._meta
                #'description'
                'type':'object',
                'properties':{}, #TODO SortedDict
            }
        #CONSIDER: base_fields when given a class, fields for when given an instance
        for name, field in form.base_fields.iteritems():
            json_schema['properties'][name] = self.convert_formfield(field, json_schema)
        return json_schema
    
    def convert_formfield(self, field, json_schema):
        target_def = {
            'title': field.label,
            'description': field.help_text,
            'required': field.required,
        }
        widget = field.field.widget
        if isinstance(widget, widgets.Input):
            target_def['type'] = widget.input_type
        elif isinstance(widget, widgets.CheckboxInput):
            target_def['type'] = 'boolean'
        elif isinstance(widget, widgets.Select):
            if widget.allow_multiple_selected:
                target_def['type'] = 'string'
            else:
                target_def['type'] = 'array'
            target_def['enum'] = [choice[0] for choice in field.choices]
        else:
            target_def['type'] = 'string'
        return target_def
        
class DjangoModelToJSONSchema(DjangoFormToJSONSchema):
    def convert_model(self, model, json_schema=None):
        model_form = None #TODO convert to model form
        #TODO handle many2many and inlines
        return self.convert_form(model_form, json_schema)

#TODO move to django-dockit
class DocKitSchemaToJSONSchema(DjangoFormToJSONSchema):
    def convert_dockitschema(self, dockit_schema, json_schema=None):
        if json_schema is None:
            json_schema = {
                #'title':dockit_schema._meta
                #'description'
                'type':'object',
                'properties':{}, #TODO SortedDict
            }
        for key, field in dockit_schema._meta.fields.iteritems():
            self.convert_dockitfield(field, json_schema)
        return json_schema
    
    def convert_dockitfield(self, field, json_schema):
        #if simple field, get the form field
        if True: #TODO is simple
            formfield = field.formfield()
            return self.convert_formfield(formfield, json_schema)
        #else: #complex stuff
        target_def = {}
        json_schema['properties'][field.name] = target_def

