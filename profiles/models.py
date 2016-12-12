from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

# Create your models here.

class Profile(models.Model):
    _genders=(
        ('M', _('Male'), ),
        ('F', _('Female'), ),
    )
    # _는 관례상 Protect의 표시
    # __는 관례상 Private의 표시
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(max_length=1,
                                null=True, blank=True,
                                choices=_genders)
    #blank는 modelForm에서 required가 False가 됨
