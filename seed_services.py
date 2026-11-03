from core.models import *

ServiceSection.load()

items = [
    ("Laptop service", "Help when your laptop isn't working as it should.", "bi bi-tools", "orange"),
    ("Desktop service", "Support for desktop computers at home or work.", "bi bi-display", "purple"),
    ("Slow performance", "Look into sluggish startup and everyday slowness.", "bi bi-speedometer2", "purple"),
    ("Hardware issues", "Check components that may need attention.", "bi bi-hdd", "orange"),
]
for i, (t, d, ic, c) in enumerate(items):
    ServiceItem.objects.get_or_create(
        title=t,
        defaults={"description": d, "icon_class": ic, "icon_color": c, "order": i},
    )
print("Service data created")