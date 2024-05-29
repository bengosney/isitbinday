class SetOwnerMixin:
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        model_form = super().get_form(request, obj, **kwargs)

        class ModelFormWithOwner(model_form):
            def save(self, commit=True):
                if not self.instance.pk:
                    self.instance.owner = request.user
                return super().save(commit)

        return ModelFormWithOwner
