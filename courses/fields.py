from django.db import models


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
        

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) == None:
            # No Current Value
            try:
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    # qs.filter(**query)
                    qs = self.model.objects.filter(**query)
                    # Get the latest instance 
                    last_item = qs.latest(self.attname)
                    value = last_item.order + 1
            except:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

