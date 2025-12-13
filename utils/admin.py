class AutoFieldsAdminMixin:
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    def get_search_fields(self, request):
        return [
            field.name for field in self.model._meta.fields if field.get_internal_type() in ["CharField", "TextField"]
        ]

    def get_list_filter(self, request):
        return [
            field.name
            for field in self.model._meta.fields
            if field.get_internal_type() in ["BooleanField", "DateField", "DateTimeField"]
        ]
