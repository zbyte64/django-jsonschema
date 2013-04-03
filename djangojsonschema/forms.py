
class JSONSchemaField:
    '''
    A django form field that takes in a schema definition and serializes the result in JSON.
    Renders to a textarea with a data-schema-json attribute containing the initial json .
    Javascript is loaded to convert the field into an Alpacajs powered form: http://www.alpacajs.org/
    
    Upon return validate the submission using python-jsonschema
    
    '''
    def __init__(self, schema):
        pass
