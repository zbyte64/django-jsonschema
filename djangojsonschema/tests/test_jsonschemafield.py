import json

from django.utils import unittest
from django import forms

from djangojsonschema.jsonschema import DjangoFormToJSONSchema
from djangojsonschema.forms import JSONSchemaField


class SurveyForm(forms.Form):
    name = forms.CharField()
    ranking = forms.ChoiceField(choices=[('1', 'excellent'), ('2', 'average'), ('3', 'poor')])

class JSONSchemaFieldTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = DjangoFormToJSONSchema()
        self.schema = self.encoder.convert_form(SurveyForm)
        
        class TargetForm(forms.Form):
            ticket = forms.CharField()
            
            #presumable a very configurable survey can be plugged in here
            survey_entry = JSONSchemaField(schema=self.schema)
        
        self.targetform = TargetForm
    
    def test_field_presentation(self):
        field = self.targetform()['survey_entry']
        html = field.as_widget()
        self.assertTrue('data-schemajson' in html)
    
    def test_field_validation(self):
        survey_response = {
            'name': 'John Smith',
            'ranking': '1',
        }
        post = {
            'survey_entry': json.dumps(survey_response),
            'ticket':'text'
        }
        form = self.targetform(data=post)
        self.assertTrue(form.is_valid(), str(form.errors))
        
        survey_response = {
            'name': 'John Smith',
            'ranking': '5',
        }
        post = {
            'survey_entry': json.dumps(survey_response),
            'ticket':'text'
        }
        form = self.targetform(data=post)
        self.assertFalse(form.is_valid())
        print form.errors
