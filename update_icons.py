from core.models import *

s = SiteSetting.load()
s.logo_icon_class = "bi bi-display"
s.save()

h = HeroSection.load()
h.warranty_icon_class = "bi bi-shield-check"
h.save()

icons = {
    "Laptop Services": "bi bi-laptop",
    "Network Solutions": "bi bi-wifi",
    "Maintenance Plans": "bi bi-wrench-adjustable",
}
for title, icon in icons.items():
    HeroFeature.objects.filter(title=title).update(icon_class=icon)

print("Icons updated")