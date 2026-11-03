from django.db import models
from django.forms import Textarea
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path,reverse
from django.utils.html import format_html
from .notify import send_whatsapp
from .models import (SiteSetting, NavLink, HeroSection,
                     HeroFeature, ServiceSection,
                     ServiceItem, ProductSection, Product, 
                     AboutSection, AboutCard,
                     SalesSection, SalesCard,
                     SetupSection, SetupTag, 
                     WhySection, WhyCard,
                     CtaSection,
                     ReviewSection, Review,PendingReview,
                     ContactSection, ContactInfo, EnquiryType, 
                     EnquiryProduct, Enquiry,
                     FooterSection, FooterLink,
                     EnquiryField
                     )

admin.site.site_header = "Tech G Admin"
admin.site.site_title = "Tech G Admin"
admin.site.index_title = "Website Content Management"


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        
        
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        meta = self.model._meta
        url = reverse(f"admin:{meta.app_label}_{meta.model_name}_change", args=[obj.pk])
        return redirect(url)


@admin.register(SiteSetting)
class SiteSettingAdmin(SingletonAdmin):
    readonly_fields = ("logo_preview",)
    fieldsets = (
        ("Logo & Favicon", {"fields": (
            "logo_image", "logo_preview", "favicon",
            "logo_icon_class", "logo_text", "logo_highlight", "site_title",
        )}),
        ("Contact Button", {"fields": ("contact_btn_text", "contact_btn_url")}),
    )

    def logo_preview(self, obj):
        if obj.logo_image:
            return format_html('<img src="{}" style="height:50px">', obj.logo_image.url)
        return "No logo uploaded"



@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Text", {"fields": ("tagline", "heading_line1", "heading_line2", "heading_highlight", "description")}),
        ("Buttons", {"fields": (("primary_btn_text", "primary_btn_url"), ("secondary_btn_text", "secondary_btn_url"))}),
        ("Warranty Badge", {"fields": ("show_warranty", "warranty_icon_class", "warranty_title", "warranty_subtitle")}),
        ("Background", {"fields": ("background_image", "image_preview")}),
    )

    def image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.background_image.url)
        return "No image uploaded"


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(HeroFeature)
class HeroFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "icon_color", "order", "is_active")
    list_editable = ("order", "is_active")
    
@admin.register(ServiceSection)
class ServiceSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Image & Badge", {"fields": ("image", "image_preview", "badge_text")}),
        ("Card Content", {"fields": ("heading_normal", "heading_highlight", "description")}),
        ("Button", {"fields": (("button_text", "button_url"),)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.image.url)
        return "No image uploaded"


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "icon_color", "order", "is_active")
    list_editable = ("order", "is_active")
    
@admin.register(ProductSection)
class ProductSectionAdmin(SingletonAdmin):
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("badge_text", "heading_normal", "heading_highlight")}),
        ("Enquire Button & WhatsApp", {"fields": ("button_text", "whatsapp_number", "whatsapp_message")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "order", "is_active")
    list_display_links = ("thumb", "name")
    list_editable = ("order", "is_active")
    search_fields = ("name", "category")

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px;border-radius:6px">', obj.image.url)
        return "-"
    
@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("badge_text", "heading_line1", "heading_violet", "heading_orange", "description")}),
        ("Right Side Image", {"fields": ("image", "image_preview", "show_decor")}),
        ("Floating Card 1 (top)", {"fields": ("show_float1", "float1_icon", "float1_title", "float1_text")}),
        ("Floating Card 2 (bottom)", {"fields": ("show_float2", "float2_icon", "float2_title", "float2_text")}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.image.url)
        return "No image uploaded"


@admin.register(AboutCard)
class AboutCardAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "icon_color", "arrow_color", "order", "is_active")
    list_editable = ("order", "is_active")
    
@admin.register(SalesSection)
class SalesSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("badge_text", "heading_line1", "heading_line2", "heading_highlight", "description")}),
        ("Left Side Image", {"fields": ("image", "image_preview")}),
        ("Button", {"fields": (("button_text", "button_url"), "button_icon")}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.image.url)
        return "No image uploaded"


@admin.register(SalesCard)
class SalesCardAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "icon_class", "icon_color", "order", "is_active")
    list_editable = ("order", "is_active")
    
@admin.register(SetupSection)
class SetupSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Text", {"fields": ("eyebrow_text", "heading", "description")}),
        ("Image", {"fields": ("image", "image_preview")}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.image.url)
        return "No image uploaded"


@admin.register(SetupTag)
class SetupTagAdmin(admin.ModelAdmin):
    list_display = ("label", "order", "is_active")
    list_editable = ("order", "is_active")
    
@admin.register(WhySection)
class WhySectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("badge_text", "heading_line1", "heading_highlight", "heading_line2", "heading_dot")}),
        ("Left Image", {"fields": ("image", "image_preview")}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.image.url)
        return "No image uploaded"


@admin.register(WhyCard)
class WhyCardAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "icon_color", "order", "is_active")
    list_editable = ("order", "is_active")
    formfield_overrides = {models.TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 50})}}
    
@admin.register(CtaSection)
class CtaSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("eyebrow_text", "heading_normal", "heading_highlight", "heading_dot", "description")}),
        ("Button", {"fields": (("button_text", "button_url"), "button_icon", "tagline")}),
        ("Background", {"fields": ("background_image", "image_preview")}),
    )

    def image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.background_image.url)
        return "No image uploaded"
    
@admin.register(ReviewSection)
class ReviewSectionAdmin(SingletonAdmin):
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("badge_text", "heading_normal", "heading_highlight", "heading_end", "subtitle")}),
        ("Slider", {"fields": ("reviews_per_page", "autoplay_seconds")}),
        ("Visitor Reviews", {"fields": ("auto_publish", "notify_email", "success_message")}),
        ("Write a Review Form", {"fields": (
            "form_icon", "form_title", "form_subtitle",
            ("name_label", "name_placeholder"), "rating_label",
            ("review_label", "review_placeholder"), ("button_text", "button_icon"),
        )}),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "stars", "short_text", "from_website", "is_active", "order", "created_at")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "from_website", "rating")
    search_fields = ("name", "city", "text")
    actions = ["approve_selected", "hide_selected"]
    def changelist_view(self, request, extra_context=None):
        n = Review.objects.filter(is_active=False, from_website=True).count()
        if n:
            messages.warning(request, f"{n} new review(s) waiting for approval. Open 'Pending Reviews' to approve.")
        return super().changelist_view(request, extra_context)

    @admin.display(description="Rating")
    def stars(self, obj):
        return "★" * obj.rating

    @admin.display(description="Review")
    def short_text(self, obj):
        return obj.text[:60] + ("…" if len(obj.text) > 60 else "")

    @admin.action(description="Approve selected reviews (show on website)")
    def approve_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Hide selected reviews")
    def hide_selected(self, request, queryset):
        queryset.update(is_active=False)
@admin.register(PendingReview)
class PendingReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "stars", "short_text", "created_at", "is_active")
    list_editable = ("is_active",)
    ordering = ("-created_at",)
    actions = ["approve_selected"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active=False, from_website=True)

    def has_add_permission(self, request):
        return False

    @admin.display(description="Rating")
    def stars(self, obj):
        return "★" * obj.rating

    @admin.display(description="Review")
    def short_text(self, obj):
        return obj.text[:80] + ("…" if len(obj.text) > 80 else "")

    @admin.action(description="Approve selected reviews (show on website)")
    def approve_selected(self, request, queryset):
        queryset.update(is_active=True)


# 🔔 notice on the admin home page
_original_index = admin.site.index

def index_with_notice(request, extra_context=None):
    e = Enquiry.objects.filter(status="new").count()
    r = Review.objects.filter(is_active=False, from_website=True).count()
    if e:
        messages.warning(request, f"🔔 {e} new customer enquiry(s). Open 'Customer Enquiries'.")
    if r:
        messages.warning(request, f"🔔 {r} new customer review(s) waiting for approval. Open 'Pending Reviews'.")
    return _original_index(request, extra_context)

admin.site.index = index_with_notice

@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    readonly_fields = ("image_preview", "wa_test_link")
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Heading", {"fields": ("badge_text", "heading_normal", "heading_highlight", "description")}),
        ("Illustration", {"fields": ("image", "image_preview")}),
        ("Form labels", {"fields": (
            "type_label", ("name_label", "name_placeholder"), ("phone_label", "phone_placeholder"),
            ("product_label", "product_placeholder"), ("quantity_label", "quantity_placeholder"), "quantity_options",
            ("specs_label", "specs_placeholder"), ("message_label", "message_placeholder"),
            ("button_text", "button_icon"),
        )}),
        ("After submit", {"fields": ("success_message", "again_text")}),
        ("Email", {"fields": ("notify_email",)}),
        ("WhatsApp", {
            "description": "Automatic WhatsApp uses the free CallMeBot service. Save this page first, then click 'Send test message'.",
            "fields": (
                "country_code", "whatsapp_number",
                "send_whatsapp_auto", "callmebot_api_key", "wa_test_link",
                "show_whatsapp_button", "whatsapp_button_text",
            )}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:8px">', obj.image.url)
        return "No image uploaded"

    @admin.display(description="Test")
    def wa_test_link(self, obj):
        return format_html(
            '<a class="button" href="{}" style="padding:8px 14px">Send test message</a> '
            '<span style="color:#888">Sends "Test from Tech G" to the WhatsApp number above</span>',
            reverse("admin:core_contactsection_test_wa"))

    def get_urls(self):
        return [path("test-whatsapp/", self.admin_site.admin_view(self.test_whatsapp),
                     name="core_contactsection_test_wa")] + super().get_urls()

    def test_whatsapp(self, request):
        c = ContactSection.load()
        ok, info = send_whatsapp(c.whatsapp_number, "Test from Tech G website. WhatsApp alerts are working.", c.callmebot_api_key)
        (messages.success if ok else messages.error)(request, ("WhatsApp test OK. " if ok else "WhatsApp test FAILED. ") + info)
        return redirect("admin:core_contactsection_changelist")

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "icon_class", "icon_color", "show_in_footer", "order", "is_active")
    list_editable = ("show_in_footer", "order", "is_active")


class EnquiryProductInline(admin.TabularInline):
    model = EnquiryProduct
    extra = 3


class EnquiryFieldInline(admin.StackedInline):
    model = EnquiryField
    extra = 1
    fieldsets = ((None, {"fields": (
        ("label", "field_type"), "placeholder", "options",
        ("required", "show_optional_tag", "full_width"),
        ("rows", "order", "is_active"),
    )}),)


@admin.register(EnquiryType)
class EnquiryTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "form_title", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    inlines = [EnquiryFieldInline, EnquiryProductInline]



@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "contact_links", "enquiry_type", "short_products", "quantity", "mail_status", "wa_status", "status")
    readonly_fields = ("enquiry_type", "name", "phone", "products", "quantity", "details", "specs", "message", "created_at", "mail_status", "wa_status")
    list_editable = ("status",)
    list_filter = ("status", "enquiry_type", "created_at")
    search_fields = ("name", "phone", "products", "message")
   

    def has_add_permission(self, request):
        return False

    @admin.display(description="Phone")
    def contact_links(self, obj):
        cc = ContactSection.load().country_code
        return format_html(
            '<a href="tel:+{cc}{p}">{p}</a> · <a href="https://wa.me/{cc}{p}" target="_blank" rel="noopener">WhatsApp</a>',
            cc=cc, p=obj.phone)

    @admin.display(description="Products / Details")
    def short_products(self, obj):
        txt = obj.products or obj.details.replace("\n", " | ")
        return txt[:50] + ("…" if len(txt) > 50 else "")
    
@admin.register(FooterSection)
class FooterSectionAdmin(SingletonAdmin):
    readonly_fields = ("logo_preview",)
    fieldsets = (
        ("Visibility", {"fields": ("is_active",)}),
        ("Logo", {"fields": ("logo_image", "logo_preview", "logo_letter", "logo_text")}),
        ("Text", {"fields": ("description", "copyright_text")}),
    )

    def logo_preview(self, obj):
        if obj.logo_image:
            return format_html('<img src="{}" style="height:50px">', obj.logo_image.url)
        return "No logo uploaded"


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order", "is_active")
    list_editable = ("order", "is_active")