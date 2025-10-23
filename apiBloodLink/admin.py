from django.contrib import admin

# Register your models here.
from .models.doctor_models import *
from .models.blood_bank_models import *
from .models.provider_models import Provider
from .models.alert_models import Alert
from .models.blood_bag_models import BloodBag
from .models.alertReceive_models import AlerteReceive

admin.site.register(Doctor)
admin.site.register(BloodBank)
admin.site.register(Provider)
admin.site.register(Alert)

admin.site.register(BloodBag)
admin.site.register(BloodTransaction)
admin.site.register(BloodRequest)
admin.site.register(AlerteReceive)