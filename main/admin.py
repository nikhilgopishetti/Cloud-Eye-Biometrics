from django.contrib import admin
from .models import ImageModel, UserActivityLog, AbnormalBehavior

admin.site.register(ImageModel)
admin.site.register(UserActivityLog)
admin.site.register(AbnormalBehavior)