#TODO find a better submodule name
from django.forms import widgets, fields


def pretty_name(name):
    """Converts 'first_name' to 'First name'"""
    if not name:
        return u''
    return name.replace('_', ' ').capitalize()

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
            json_schema['properties'][name] = self.convert_formfield(name, field, json_schema)
        return json_schema
    
    input_type_map = {
        'text': 'string',
    }
    
    def convert_formfield(self, name, field, json_schema):
        #TODO detect bound field
        widget = field.widget
        target_def = {
            'title': field.label or pretty_name(name),
            'description': field.help_text,
        }
        if field.required:
            target_def['required'] = [name] #TODO this likely is not correct
        #TODO JSONSchemaField; include subschema and ref the type
        if isinstance(field, fields.URLField):
            target_def['type'] = 'string'
            target_def['format'] = 'url'
        elif isinstance(field, fields.FileField):
            target_def['type'] = 'string'
            target_def['format'] = 'uri'
        elif isinstance(field, fields.DateField):
            target_def['type'] = 'string'
            target_def['format'] = 'date'
        elif isinstance(field, fields.DateTimeField):
            target_def['type'] = 'string'
            target_def['format'] = 'datetime'
        elif isinstance(field, (fields.DecimalField, fields.FloatField)):
            target_def['type'] = 'number'
        elif isinstance(field, fields.IntegerField):
            target_def['type'] = 'integer'
        elif isinstance(field, fields.EmailField):
            target_def['type'] = 'string'
            target_def['format'] = 'email'
        elif isinstance(field, fields.NullBooleanField):
            target_def['type'] = 'boolean'
        elif isinstance(widget, widgets.CheckboxInput):
            target_def['type'] = 'boolean'
        elif isinstance(widget, widgets.Select):
            if widget.allow_multiple_selected:
                target_def['type'] = 'array'
            else:
                target_def['type'] = 'string'
            target_def['enum'] = [choice[0] for choice in field.choices]
        elif isinstance(widget, widgets.Input):
            translated_type = self.input_type_map.get(widget.input_type, 'string')
            target_def['type'] = translated_type
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
            json_schema['properties'][key] = self.convert_dockitfield(key, field, json_schema)
        return json_schema
    
    def convert_dockitfield(self, name, field, json_schema):
        #if simple field, get the form field
        if True: #TODO is simple
            formfield = field.formfield()
            return self.convert_formfield(formfield, json_schema)
        #else: #complex stuff
        target_def = {}

