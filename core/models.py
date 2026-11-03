from django.db import models
import re
from urllib.parse import quote
from datetime import date

class SingletonModel(models.Model):
    """Oru record mattum irukkum (settings maari)"""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSetting(SingletonModel):
    logo_icon_class = models.CharField(max_length=100, default="fa-solid fa-desktop",
                                       help_text="Bootstrap Icons class. Example: bi bi-laptop")
    logo_image = models.ImageField(upload_to="logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="logo/", blank=True, null=True,
                                help_text="Browser tab icon. Square PNG, 512x512 recommended. Empty na logo image use aagum")
    site_title = models.CharField(max_length=100, default="Tech G", help_text="Browser tab title")
    logo_text = models.CharField(max_length=50, default="Tech")
    logo_highlight = models.CharField(max_length=50, default="G", help_text="Purple color la varum")
    contact_btn_text = models.CharField(max_length=50, default="Contact Us")
    contact_btn_url = models.CharField(max_length=200, default="#contact")

    class Meta:
        verbose_name = "Site Setting (Logo & Contact Button)"
        verbose_name_plural = "Site Setting (Logo & Contact Button)"

    def __str__(self):
        return "Site Settings"


class NavLink(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200, help_text="Example: #products or /about/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        
    def save(self, *args, **kwargs):
        if self.url.startswith("#"):
            self.url = self.url.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class HeroSection(SingletonModel):
    tagline = models.CharField(max_length=100, default="Computer Sales & Service")
    heading_line1 = models.CharField(max_length=100, default="One supplier")
    heading_line2 = models.CharField(max_length=100, default="for")
    heading_highlight = models.CharField(max_length=100, default="every piece", help_text="Orange color la varum")
    description = models.TextField(default="We supply the products and accessories needed for a complete computer setup — from the screen you look at to the cable that connects you.")

    primary_btn_text = models.CharField(max_length=50, default="Explore Products")
    primary_btn_url = models.CharField(max_length=200, default="#products")
    secondary_btn_text = models.CharField(max_length=50, default="Request a Quote")
    secondary_btn_url = models.CharField(max_length=200, default="#contact")

    show_warranty = models.BooleanField(default=True)
    warranty_icon_class = models.CharField(max_length=100, default="fa-solid fa-shield-halved")
    warranty_title = models.CharField(max_length=100, default="1-Year Service Warranty")
    warranty_subtitle = models.CharField(max_length=150, default="(Warranty Protection Included)")

    background_image = models.ImageField(upload_to="hero/", blank=True, null=True,
                                         help_text="Bootstrap Icons class. Example: bi bi-laptop")
    is_active = models.BooleanField(default=True, help_text="Untick pannina section hide aagum")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"


class HeroFeature(models.Model):
    COLOR_CHOICES = [("purple", "Purple"), ("orange", "Orange")]

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=150)
    icon_class = models.CharField(max_length=100, default="fa-solid fa-laptop",
                                  help_text="Bootstrap Icons class. Example: bi bi-laptop")
    icon_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="purple")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Hero Bottom Feature"

    def __str__(self):
        return self.title
    
class ServiceSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick pannina section hide aagum")
    badge_text = models.CharField(max_length=100, default="Laptop & Computer Service")
    image = models.ImageField(upload_to="services/", blank=True, null=True,
                              help_text="Big top image. Recommended: 1600x600 px")
    heading_normal = models.CharField(max_length=150, default="When something isn't right,")
    heading_highlight = models.CharField(max_length=100, default="bring it in.",
                                         help_text="Italic purple color la varum")
    description = models.TextField(default="Describe the problem you're facing and we'll get back to you about service for your laptop or desktop.")
    button_text = models.CharField(max_length=50, default="Request a Quote")
    button_url = models.CharField(max_length=200, default="#contact")

    class Meta:
        verbose_name = "Service Section"
        verbose_name_plural = "Service Section"

    def __str__(self):
        return "Service Section"


class ServiceItem(models.Model):
    COLOR_CHOICES = [("orange", "Orange"), ("purple", "Purple")]

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=150)
    icon_class = models.CharField(max_length=100, default="bi bi-tools",
                                  help_text="Bootstrap Icons class. Example: bi bi-tools")
    icon_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="orange")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Service Item"

    def __str__(self):
        return self.title
    
class ProductSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick pannina section hide aagum")
    badge_text = models.CharField(max_length=100, default="Products & Accessories")
    heading_normal = models.CharField(max_length=150, default="Everything for the desk,")
    heading_highlight = models.CharField(max_length=100, default="in one place.",
                                         help_text="Italic violet color la varum")
    button_text = models.CharField(max_length=50, default="Enquire Now")
    whatsapp_number = models.CharField(max_length=20, default="919999999999",
                                       help_text="Country code oda, + illaama. Example: 919876543210")
    whatsapp_message = models.CharField(max_length=250,
                                        default="Hi Tech G, I would like to enquire about {product}.",
                                        help_text="{product} nu irundha product name auto ah maarum")

    class Meta:
        verbose_name = "Product Section"
        verbose_name_plural = "Product Section"

    def __str__(self):
        return "Product Section"


class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=50, default="Computers",
                                help_text="Image mela pill la varum. Example: Computers, Peripherals, Networking")
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/", blank=True, null=True,
                              help_text="Transparent PNG recommended, 800x600 px")
    custom_message = models.CharField(max_length=250, blank=True,
                                      help_text="Optional. Idha fill pannina indha product ku mattum custom WhatsApp message use aagum")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
class AboutSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick pannina section hide aagum")
    badge_text = models.CharField(max_length=50, default="About Us")
    heading_line1 = models.CharField(max_length=100, default="Your Trusted Partner")
    heading_violet = models.CharField(max_length=60, default="for", help_text="Italic violet color")
    heading_orange = models.CharField(max_length=100, default="Computer Solutions", help_text="Italic orange color")
    description = models.TextField(default="We provide a complete range of computer solutions, including laptop and desktop sales, professional computer service, and a wide selection of accessories and peripherals — all designed to meet your personal and business needs.")

    image = models.ImageField(upload_to="about/", blank=True, null=True,
                              help_text="Right side photo. Recommended: 1200x1000 px")
    show_decor = models.BooleanField(default=True,
                                     help_text="Lavender circle, arcs, dots. Image la already irundha untick pannunga")

    show_float1 = models.BooleanField(default=True)
    float1_icon = models.CharField(max_length=100, default="bi bi-shield-check", help_text="Bootstrap Icons class")
    float1_title = models.CharField(max_length=60, default="Reliable Solutions")
    float1_text = models.CharField(max_length=100, default="For home, office and business.")

    show_float2 = models.BooleanField(default=True)
    float2_icon = models.CharField(max_length=100, default="bi bi-display", help_text="Bootstrap Icons class")
    float2_title = models.CharField(max_length=60, default="Quality Products")
    float2_text = models.CharField(max_length=100, default="Trusted brands. Better performance.")

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section"


class AboutCard(models.Model):
    COLOR_CHOICES = [("blue", "Blue"), ("orange", "Orange"), ("purple", "Purple")]

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=100, default="bi bi-display",
                                  help_text="Bootstrap Icons class. Example: bi bi-gear")
    icon_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="blue",
                                  help_text="Icon box color")
    arrow_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="orange",
                                   help_text="Keezha irukkura circle arrow color")
    link_url = models.CharField(max_length=200, blank=True, default="#products",
                                help_text="Arrow click panna pogum idam. Example: #products")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "About Card"

    def __str__(self):
        return self.title
    
class SalesSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick pannina section hide aagum")
    badge_text = models.CharField(max_length=60, default="Laptop & Computer Sales")
    heading_line1 = models.CharField(max_length=100, default="Find the computer", help_text="Purple, 1st line")
    heading_line2 = models.CharField(max_length=100, default="that fits", help_text="Purple, 2nd line")
    heading_highlight = models.CharField(max_length=100, default="how you work.", help_text="Italic orange text")
    description = models.TextField(default="Whether you need a laptop to carry or a desktop to settle into, tell us what you need it for and we'll help you explore the options available.")
    image = models.ImageField(upload_to="sales/", blank=True, null=True,
                              help_text="Left side full visual (photo + frames + stripes). Transparent PNG, approx 1300x1200 px")
    button_text = models.CharField(max_length=50, default="Request a Quote")
    button_url = models.CharField(max_length=200, default="#contact", help_text="Example: #contact")
    button_icon = models.CharField(max_length=100, default="bi bi-arrow-right", blank=True,
                                   help_text="Bootstrap Icons (bi bi-arrow-right) or Box Icons (bx bx-right-arrow-alt)")

    class Meta:
        verbose_name = "Laptop & Computer Sales Section"
        verbose_name_plural = "Laptop & Computer Sales Section"

    def __str__(self):
        return "Laptop & Computer Sales Section"


class SalesCard(models.Model):
    COLOR_CHOICES = [("purple", "Purple"), ("orange", "Orange")]

    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=120)
    icon_class = models.CharField(max_length=100, default="bi bi-laptop",
                                  help_text="Bootstrap Icons (bi bi-laptop) or Box Icons (bx bx-laptop)")
    icon_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="purple", help_text="Icon box + card color")
    link_url = models.CharField(max_length=200, blank=True, default="", help_text="Optional. Example: #products")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Sales Card"

    def __str__(self):
        return self.title
    
class SetupSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick pannina section hide aagum")
    eyebrow_text = models.CharField(max_length=80, default="Complete Computer Setup",
                                    help_text="Mela irukkura chinna orange text (uppercase-la varum)")
    heading = models.CharField(max_length=150, default="“Technology, chosen well.”")
    description = models.TextField(default="Carefully selected components, bringing performance, reliability, and everything you need together.")
    image = models.ImageField(upload_to="setup/", blank=True, null=True,
                              help_text="Big center image. Recommended: 2200 x 1000 px (wide)")

    class Meta:
        verbose_name = "Complete Setup Section"
        verbose_name_plural = "Complete Setup Section"

    def __str__(self):
        return "Complete Setup Section"


class SetupTag(models.Model):
    label = models.CharField(max_length=40, help_text="Example: Monitor")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Setup Pill"

    def __str__(self):
        return self.label
    
class WhySection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick to hide the section")
    badge_text = models.CharField(max_length=60, default="Why Choose Us")
    heading_line1 = models.CharField(max_length=60, default="Built around")
    heading_highlight = models.CharField(max_length=40, default="your", help_text="Italic violet word")
    heading_line2 = models.CharField(max_length=60, default="whole setup")
    heading_dot = models.CharField(max_length=3, default=".", blank=True, help_text="Orange full stop after line 2")
    image = models.ImageField(upload_to="why/", blank=True, null=True,
                              help_text="Left visual (monitor, plant, circles). Transparent PNG, approx 1500 x 1000 px")

    class Meta:
        verbose_name = "Why Choose Us Section"
        verbose_name_plural = "Why Choose Us Section"

    def __str__(self):
        return "Why Choose Us Section"


class WhyCard(models.Model):
    COLOR_CHOICES = [("orange", "Orange"), ("purple", "Purple")]

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=200, help_text="Press Enter for a line break")
    icon_class = models.CharField(max_length=100, default="bi bi-laptop",
                                  help_text="Bootstrap Icons (bi bi-laptop) or Box Icons (bx bx-laptop)")
    icon_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="orange",
                                  help_text="Icon box, arrow and timeline dot color")
    arrow_icon = models.CharField(max_length=100, default="bi bi-arrow-right", blank=True)
    link_url = models.CharField(max_length=200, blank=True, default="#products")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Why Choose Us Card"

    def __str__(self):
        return self.title
    
class CtaSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick to hide the section")
    eyebrow_text = models.CharField(max_length=80, default="Have a question?", help_text="Small uppercase text on top")
    heading_normal = models.CharField(max_length=80, default="Let's talk")
    heading_highlight = models.CharField(max_length=60, default="computers", help_text="Italic lavender word")
    heading_dot = models.CharField(max_length=3, default=".", blank=True, help_text="Orange full stop")
    description = models.TextField(default="Looking for a product, an accessory, or service for your computer? Send us an enquiry.")
    button_text = models.CharField(max_length=40, default="Get in Touch")
    button_url = models.CharField(max_length=200, default="#contact")
    button_icon = models.CharField(max_length=100, default="bi bi-arrow-right", blank=True,
                                   help_text="Bootstrap Icons (bi bi-arrow-right) or Box Icons (bx bx-right-arrow-alt)")
    tagline = models.CharField(max_length=120, default="Products · Accessories · Service", blank=True,
                               help_text="Small text beside the button. Leave empty to hide")
    background_image = models.ImageField(upload_to="cta/", blank=True, null=True,
                                         help_text="Card background photo. Recommended: 2000 x 800 px")

    class Meta:
        verbose_name = "CTA Banner Section"
        verbose_name_plural = "CTA Banner Section"

    def __str__(self):
        return "CTA Banner Section"
    
from django.core.validators import MinValueValidator, MaxValueValidator


class ReviewSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick to hide the section")

    badge_text = models.CharField(max_length=60, default="Customer Reviews")
    heading_normal = models.CharField(max_length=60, default="What our")
    heading_highlight = models.CharField(max_length=60, default="customers", help_text="Violet word")
    heading_end = models.CharField(max_length=60, default="say", blank=True)
    subtitle = models.CharField(max_length=160, default="Real people. Real experiences. Trusted by many.", blank=True)

    reviews_per_page = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(6)],
                                                        help_text="Reviews shown at a time on desktop (1-6). Mobile shows max 2")
    autoplay_seconds = models.PositiveSmallIntegerField(default=6, help_text="Auto slide time in seconds. 0 = off")

    auto_publish = models.BooleanField(default=False,
                                       help_text="Ticked: visitor reviews go live immediately. Unticked: they wait for your approval")
    notify_email = models.EmailField(blank=True,
                                     help_text="New visitor reviews are emailed here. Leave empty to turn off")
    success_message = models.CharField(max_length=200,
                                       default="Thank you! Your review has been submitted and will appear after approval.")

    form_icon = models.CharField(max_length=100, default="bi bi-pencil-fill", help_text="Bootstrap Icons or Box Icons class")
    form_title = models.CharField(max_length=60, default="Write a Review")
    form_subtitle = models.CharField(max_length=200, default="Share your experience with us. Your feedback helps us serve you better.")
    name_label = models.CharField(max_length=40, default="Customer Name")
    name_placeholder = models.CharField(max_length=60, default="Enter your name")
    rating_label = models.CharField(max_length=40, default="Rating")
    review_label = models.CharField(max_length=40, default="Your Review")
    review_placeholder = models.CharField(max_length=80, default="Write your review here...")
    button_text = models.CharField(max_length=40, default="Submit Review")
    button_icon = models.CharField(max_length=100, default="bi bi-send-fill", blank=True)

    class Meta:
        verbose_name = "Customer Reviews Section"
        verbose_name_plural = "Customer Reviews Section"

    def __str__(self):
        return "Customer Reviews Section"


class Review(models.Model):
    COLOR_CHOICES = [("violet", "Violet"), ("orange", "Orange"), ("purple", "Purple")]
    RATING_CHOICES = [(i, f"{i} star{'s' if i > 1 else ''}") for i in range(5, 0, -1)]

    name = models.CharField(max_length=80)
    city = models.CharField(max_length=60, blank=True, help_text="Example: Chennai (optional)")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    text = models.TextField(max_length=400)
    avatar_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="violet",
                                    help_text="Color of the letter circle")
    is_active = models.BooleanField(default=True, help_text="Tick to show on the website. Untick = hidden / pending approval")
    from_website = models.BooleanField(default=False, editable=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Customer Review"

    def __str__(self):
        return f"{self.name} ({self.rating}★)"
    
class PendingReview(Review):
    """Admin menu-la 'waiting for approval' reviews mattum kaattum"""
    
    class Meta:
        proxy = True
        verbose_name = "Pending Review (waiting approval)"
        verbose_name_plural = "Pending Reviews (waiting approval)"
        
class ContactSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick to hide the section")

    badge_text = models.CharField(max_length=40, default="Contact")
    heading_normal = models.CharField(max_length=60, default="Send us an")
    heading_highlight = models.CharField(max_length=60, default="enquiry.", help_text="Italic violet text")
    description = models.TextField(default="Tell us what you're looking for — a product, an accessory or service — and we'll get back to you.")
    image = models.ImageField(upload_to="contact/", blank=True, null=True,
                              help_text="Illustration (girl with laptop). Transparent PNG, approx 900 x 1000 px")

    type_label = models.CharField(max_length=40, default="Enquiry Type")
    name_label = models.CharField(max_length=40, default="Name")
    name_placeholder = models.CharField(max_length=60, default="Enter your name")
    phone_label = models.CharField(max_length=40, default="Phone Number")
    phone_placeholder = models.CharField(max_length=60, default="Enter your phone number")
    product_label = models.CharField(max_length=40, default="Select Product", help_text="Default label. Each enquiry type can override it")
    product_placeholder = models.CharField(max_length=80, default="e.g., Laptop, Monitor, Keyboard")
    quantity_label = models.CharField(max_length=40, default="Quantity")
    quantity_placeholder = models.CharField(max_length=60, default="Select quantity")
    quantity_options = models.TextField(default="1\n2\n3\n4\n5\n6 - 10\nMore than 10", help_text="One option per line")
    specs_label = models.CharField(max_length=60, default="Specifications / Requirements")
    specs_placeholder = models.CharField(max_length=120, default="Tell us about the specifications or any special requirements...")
    message_label = models.CharField(max_length=40, default="Message")
    message_placeholder = models.CharField(max_length=80, default="Additional details (optional)...")
    button_text = models.CharField(max_length=40, default="Submit Enquiry")
    button_icon = models.CharField(max_length=100, default="bi bi-cursor-fill", blank=True,
                                   help_text="Bootstrap Icons or Box Icons class")

    success_message = models.CharField(max_length=200, default="Thank you! We have received your enquiry and will get back to you shortly.")
    again_text = models.CharField(max_length=40, default="Send another enquiry")

    notify_email = models.EmailField(blank=True, help_text="Every enquiry is emailed here. Empty = no email")
    country_code = models.CharField(max_length=5, default="91", help_text="Digits only. Used for customer call / WhatsApp links in admin")
    whatsapp_number = models.CharField(max_length=20, blank=True,
                                       help_text="Shop WhatsApp number WITH country code, digits only. Example: 919876543210")
    send_whatsapp_auto = models.BooleanField(default=False,
                                             help_text="Send each enquiry automatically to the number above (needs CALLMEBOT_API_KEY in .env)")
    show_whatsapp_button = models.BooleanField(default=True,
                                               help_text="After submit, show a 'Send on WhatsApp' button to the customer")
    whatsapp_button_text = models.CharField(max_length=40, default="Send on WhatsApp")
    
    callmebot_api_key = models.CharField(max_length=60, blank=True,
                                         help_text="API key you got from CallMeBot on WhatsApp (needed only for automatic WhatsApp)")

    class Meta:
        verbose_name = "Contact Section"
        verbose_name_plural = "Contact Section"

    def __str__(self):
        return "Contact Section"

    def quantity_list(self):
        return [l.strip() for l in self.quantity_options.splitlines() if l.strip()]


class ContactInfo(models.Model):
    COLOR_CHOICES = [("orange", "Orange"), ("purple", "Purple")]
    KIND_CHOICES = [
        ("auto", "Auto-detect"),
        ("phone", "Phone (click = call)"),
        ("email", "Email (click = compose mail to this address)"),
        ("address", "Address (click = Google Maps)"),
        ("other", "Plain text / custom link"),
    ]

    label = models.CharField(max_length=40, help_text="Example: Phone")
    value = models.CharField(max_length=120, help_text="Example: +91 98765 43210")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default="auto",
                            help_text="Decides what happens on click. Auto-detect works for Phone / Email / Address")
    icon_class = models.CharField(max_length=100, default="bi bi-telephone", help_text="Bootstrap Icons or Box Icons class")
    icon_color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="orange")
    link_url = models.CharField(max_length=300, blank=True,
                                help_text="Optional override. Address: paste Google Maps 'Share' link for exact pin. Empty = auto link")
    mail_subject = models.CharField(max_length=120, blank=True, default="Enquiry from website",
                                    help_text="Email only. Pre-filled subject")
    desktop_gmail = models.BooleanField(default=True,
                                        help_text="Email only. On laptop/desktop open Gmail compose in new tab (mobile uses the mail app)")
    show_in_footer = models.BooleanField(default=True, help_text="Show this row in the footer")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Contact Info Row"

    def __str__(self):
        return self.label

    def resolved_kind(self):
        if self.kind != "auto":
            return self.kind
        v, l, ic = self.value.lower(), self.label.lower(), self.icon_class.lower()
        if "@" in v or "mail" in l or "envelope" in ic:
            return "email"
        if any(k in l for k in ("phone", "mobile", "call", "whatsapp")) or "phone" in ic or "telephone" in ic:
            return "phone"
        if any(k in l for k in ("address", "location", "office", "shop")) or "geo" in ic or "map" in ic or "location" in ic:
            return "address"
        return "other"

    def href(self):
        if self.link_url.strip():
            return self.link_url.strip()
        k, v = self.resolved_kind(), self.value.strip()
        if k == "phone":
            return "tel:" + ("+" if v.startswith("+") else "") + re.sub(r"\D", "", v)
        if k == "email":
            return "mailto:" + v + (("?subject=" + quote(self.mail_subject)) if self.mail_subject else "")
        if k == "address":
            return "https://www.google.com/maps/search/?api=1&query=" + quote(v)
        return ""

    def new_tab(self):
        return self.href().startswith("http")

    def gmail_url(self):
        if self.resolved_kind() == "email" and self.desktop_gmail:
            return "https://mail.google.com/mail/?view=cm&fs=1&to=" + quote(self.value.strip()) + \
                   "&su=" + quote(self.mail_subject or "")
        return ""

class EnquiryType(models.Model):
    title = models.CharField(max_length=40, help_text="Tab name. Example: IT Products")
    icon_class = models.CharField(max_length=100, default="bi bi-box-seam", help_text="Tab icon")
    form_title = models.CharField(max_length=80, help_text="Example: IT Products Quotation")
    form_subtitle = models.CharField(max_length=160, blank=True)
    form_icon = models.CharField(max_length=100, default="bi bi-box-seam", help_text="Small icon beside the form title")
    product_label = models.CharField(max_length=40, blank=True, help_text="Optional. Example: Select Service. Empty = default label")
    product_placeholder = models.CharField(max_length=80, blank=True, help_text="Optional. Empty = default placeholder")
    message_placeholder = models.CharField(max_length=120, blank=True, default="",
                                           help_text="Optional. Placeholder inside the Message box for this tab. Empty = default")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Enquiry Type (tab)"

    def __str__(self):
        return self.title


class EnquiryProduct(models.Model):
    enquiry_type = models.ForeignKey(EnquiryType, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Enquiry(models.Model):
    STATUS_CHOICES = [("new", "New"), ("contacted", "Contacted"), ("closed", "Closed")]
    mail_status = models.CharField(max_length=200, blank=True)
    wa_status = models.CharField(max_length=200, blank=True)
    enquiry_type = models.CharField(max_length=80)
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    products = models.TextField(blank=True)
    quantity = models.CharField(max_length=40, blank=True)
    details = models.TextField(blank=True, default="")
    specs = models.TextField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Enquiry"
        verbose_name_plural = "Customer Enquiries"

    def __str__(self):
        return f"{self.name} - {self.enquiry_type}"
    
class FooterSection(SingletonModel):
    is_active = models.BooleanField(default=True, help_text="Untick to hide the footer")
    logo_image = models.ImageField(upload_to="footer/", blank=True, null=True,
                                   help_text="Optional. Empty = purple circle with the letter below")
    logo_letter = models.CharField(max_length=2, default="C", help_text="Letter inside the purple circle")
    logo_text = models.CharField(max_length=50, default="Tech-G")
    description = models.TextField(default="Computer sales and service — laptops, desktops, peripherals and networking accessories.")
    copyright_text = models.CharField(max_length=150, default="© {year} Tech-G Computers",
                                      help_text="Use {year} to keep the year updating automatically")

    class Meta:
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Section"

    def __str__(self):
        return "Footer Section"

    def copyright(self):
        return self.copyright_text.replace("{year}", str(date.today().year))


class FooterLink(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200, help_text="Example: #products or /about/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Footer Link"

    def save(self, *args, **kwargs):
        u = self.url.strip()
        if u and not u.startswith(("#", "/", "http", "tel:", "mailto:")):
            u = "#" + u          # "Contact" becomes "#contact"
        if u.startswith("#"):
            u = u.lower()
        self.url = u
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class EnquiryField(models.Model):
    TYPE_CHOICES = [
        ("text", "Single-line text box"),
        ("textarea", "Multi-line text box"),
        ("select", "Dropdown (choose one)"),
        ("multiselect", "Dropdown (choose many)"),
        ("products", "Dropdown (choose many) - uses this tab's Enquiry products list"),
        ("date", "Date picker"),
    ]
    enquiry_type = models.ForeignKey(EnquiryType, on_delete=models.CASCADE, related_name="custom_fields")
    label = models.CharField(max_length=60, help_text="Example: Number of Systems")
    field_type = models.CharField(max_length=12, choices=TYPE_CHOICES, default="text")
    placeholder = models.CharField(max_length=120, blank=True, help_text="Example: e.g., 5 computers, 10 systems")
    options = models.TextField(blank=True, help_text="Dropdowns only. One option per line")
    required = models.BooleanField(default=False, help_text="Shows the red * and must be filled")
    show_optional_tag = models.BooleanField(default=False, help_text="Shows a small grey '(Optional)' beside the label")
    full_width = models.BooleanField(default=False, help_text="Untick = half width (2 fields side by side)")
    rows = models.PositiveSmallIntegerField(default=3, help_text="Multi-line box only. Height in lines (1-8)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Form field"

    def __str__(self):
        return self.label

    def option_list(self):
        return [l.strip() for l in self.options.splitlines() if l.strip()]