from .models import SiteSetting, NavLink, FooterSection, FooterLink, ContactInfo


def site_data(request):
    return {
        "site": SiteSetting.load(),
        "nav_links": NavLink.objects.filter(is_active=True),
        "footer": FooterSection.load(),
        "footer_links": FooterLink.objects.filter(is_active=True),
        "footer_contacts": ContactInfo.objects.filter(is_active=True, show_in_footer=True),
    }