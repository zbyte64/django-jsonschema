from jsonschema import Draft4Validator

from django.utils import unittest
from django import forms

from djangojsonschema.jsonschema import DjangoFormToJSONSchema


check_schema = Draft4Validator.check_schema

CHOICES = [('first', 'first'), ('second', 'second')]

class TestForm(forms.Form):
    a_charfield = forms.CharField(help_text='Any string')
    a_textarea = forms.CharField(widget=forms.Textarea, help_text='Any paragraph')
    url = forms.URLField()
    a_boolean = forms.BooleanField()
    select_option = forms.ChoiceField(choices=CHOICES)
    a_date = forms.DateField()
    a_datetime = forms.DateTimeField()
    a_decimal = forms.DecimalField()
    an_email = forms.EmailField()
    a_file = forms.FileField()
    #a_filepath = forms.FilePathField()
    a_float = forms.FloatField()
    an_image = forms.ImageField()
    an_integer = forms.IntegerField()
    an_ipaddress = forms.IPAddressField()
    #a_generic_ipaddress = forms.GenericIPAddressField()
    a_multiple_choice = forms.MultipleChoiceField(choices=CHOICES)
    a_typed_multiple_choice = forms.TypedMultipleChoiceField(choices=CHOICES)
    a_null_boolean = forms.NullBooleanField() #not sure what this should be
    a_regex = forms.RegexField(regex=r'<([A-Z][A-Z0-9]*)\b[^>]*>(.*?)</\1>') #matches tags
    a_slug = forms.SlugField()
    a_time = forms.TimeField()

class FormToJsonSchemaTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = DjangoFormToJSONSchema()

    def test_convert_form(self):
        form_repr = self.encoder.convert_form(TestForm)
        print form_repr
        try:
            check_schema(form_repr)
        except Exception as error:
            print error.message
            print error.path
            print error.validator
            print error.cause
            raise
        instance_form_repr = self.encoder.convert_form(TestForm())
        check_schema(instance_form_repr)

    def test_convert_charfield(self):
        name = 'a_charfield'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'description': u'Any string',
            'title': 'A charfield',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_charfield(self):
        #CONSIDER: the json spec doesn't define a textarea, this is an option of alpacajs
        name = 'a_textarea'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'description': u'Any paragraph',
            'title': 'A textarea',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_urlfield(self):
        name = 'url'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'format': 'url',
            'description': u'',
            'title': 'Url',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_booleanfield(self):
        name = 'a_boolean'
        ideal_repr = {
            'required': [name],
            'type': 'boolean',
            'description': u'',
            'title': 'A boolean',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_select_option(self):
        name = 'select_option'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'description': u'',
            'title': 'Select option',
            'enum': ['first', 'second'],
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_date(self):
        name = 'a_date'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'format': 'date',
            'description': u'',
            'title': 'A date',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_datetime(self):
        name = 'a_datetime'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'format': 'datetime',
            'description': u'',
            'title': 'A datetime',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_decimal(self):
        name = 'a_decimal'
        ideal_repr = {
            'required': [name],
            'type': 'number',
            'description': u'',
            'title': 'A decimal',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_email(self):
        name = 'an_email'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'format': 'email',
            'description': u'',
            'title': 'An email',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_file(self):
        name = 'a_file'
        ideal_repr = {
            'required': [name],
            'type': 'string',
            'format': 'uri',
            'description': u'',
            'title': 'A file',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_float(self):
        name = 'a_float'
        ideal_repr = {
            'required': [name],
            'type': 'number',
            'description': u'',
            'title': 'A float',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

    def test_convert_integer(self):
        name = 'an_integer'
        ideal_repr = {
            'required': [name],
            'type': 'integer',
            'description': u'',
            'title': 'An integer',
        }
        field = TestForm.base_fields[name]
        json_schema = {'properties':{}}
        schema_repr = self.encoder.convert_formfield(name, field, json_schema)
        self.assertEqual(schema_repr, ideal_repr)

