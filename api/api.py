from ninja import NinjaAPI, Schema
from api.collections import collections

api = NinjaAPI()
api.add_router("collections", collections.router)
