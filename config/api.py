from ninja import NinjaAPI
from .generate_context import ContextSchema, generate_exa, ExampleContext

api = NinjaAPI()

@api.post('/context')
def generate_context(request, payload: ContextSchema):
    response = generate_exa(payload)
    return response