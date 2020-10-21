from django.contrib import admin

from tracker import models

# side effects
from . import (  # noqa: F401
    bid,
    country,
    donation,
    event,
    log,
    paypal,
    prize,
    interstitial,
)

# plain admin
admin.site.register(models.Country)
admin.site.register(models.WordFilter)
admin.site.register(models.AmountFilter)
admin.site.register(models.Submission)
admin.site.register(models.UserProfile)
admin.site.register(models.PrizeCategory)
admin.site.index_template = 'admin/tracker/menu.html'
admin.site.site_header = 'Donation Tracker'
