from django.core.serializers.json import DjangoJSONEncoder

# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, YourCustomType):
#             return str(obj)
#         return super().default(obj)
