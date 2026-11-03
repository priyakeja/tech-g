import time
from django.db.models import Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import os
import re
import urllib.request
from urllib.parse import quote, urlencode
import threading
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render
from .models import (HeroSection, HeroFeature,
                     ServiceSection, ServiceItem,
                     ProductSection, Product, 
                     AboutSection, AboutCard, 
                     SalesSection, SalesCard,
                     SetupSection, SetupTag,
                     WhySection, WhyCard,
                     CtaSection,ReviewSection, Review,
                     ContactSection, ContactInfo, EnquiryType, Enquiry,
                     )
from .notify import send_whatsapp
from datetime import date

_REQ_MSG = {"products": "Please select at least one product.", "quantity": "Please select a quantity."}


def _fields_for(t, contact):
    """Fields of one enquiry tab. A tab with no custom fields keeps the old default layout."""
    prods = [p.name for p in t.products.all() if p.is_active]
    custom = [f for f in t.custom_fields.all() if f.is_active]
    if not custom:
        return [
            {"key": "products", "label": t.product_label or contact.product_label, "type": "products",
             "placeholder": t.product_placeholder or contact.product_placeholder, "options": prods,
             "required": True, "optional_tag": False, "full": True, "rows": 3},
            {"key": "quantity", "label": contact.quantity_label, "type": "select",
             "placeholder": contact.quantity_placeholder, "options": contact.quantity_list(),
             "required": True, "optional_tag": False, "full": False, "rows": 3},
            {"key": "specs", "label": contact.specs_label, "type": "textarea",
             "placeholder": contact.specs_placeholder, "options": [],
             "required": False, "optional_tag": False, "full": False, "rows": 3},
        ]
    return [{
        "key": f"f{f.id}", "label": f.label, "type": f.field_type, "placeholder": f.placeholder,
        "options": prods if f.field_type == "products" else f.option_list(),
        "required": f.required, "optional_tag": f.show_optional_tag, "full": f.full_width, "rows": f.rows,
    } for f in custom]


def _clean_answers(post, fields):
    errors, answers = {}, []
    for f in fields:
        k, t = f["key"], f["type"]
        if t in ("multiselect", "products"):
            val = ", ".join(v for v in dict.fromkeys(post.getlist(k)) if v in f["options"])
        elif t == "select":
            v = post.get(k, "").strip()
            val = v if v in f["options"] else ""
        elif t == "date":
            v = post.get(k, "").strip()
            try:
                d = date.fromisoformat(v) if v else None
            except ValueError:
                d = None
            if d and d < date.today():
                errors[k] = "Please choose today or a future date."
                continue
            val = d.strftime("%d %b %Y") if d else ""
        elif t == "textarea":
            val = post.get(k, "").strip()[:500]
        else:
            val = " ".join(post.get(k, "").split())[:200]

        if f["required"] and not val:
            if k in _REQ_MSG:
                errors[k] = _REQ_MSG[k]
            elif t == "date":
                errors[k] = "Please choose a date."
            elif t in ("select", "multiselect", "products"):
                errors[k] = "Please select " + f["label"].lower() + "."
            else:
                errors[k] = "Please enter " + f["label"].lower() + "."
        if val:
            answers.append((f, val))
    return errors, answers

def index(request):
    prod_section = ProductSection.load()
    number = re.sub(r"\D", "", prod_section.whatsapp_number)

    products = list(Product.objects.filter(is_active=True))
    for p in products:
        template = p.custom_message or prod_section.whatsapp_message
        msg = template.replace("{product}", p.name)
        p.wa_url = f"https://wa.me/{number}?text={quote(msg)}" if number else "#"

       
    contact = ContactSection.load()
    enquiry_types = list(EnquiryType.objects.filter(is_active=True).prefetch_related("products", "custom_fields"))
    enquiry_data = [{
        "id": t.id,
        "form_title": t.form_title,
        "form_subtitle": t.form_subtitle,
        "form_icon": t.form_icon,
        "message_placeholder": t.message_placeholder or contact.message_placeholder,
        "fields": _fields_for(t, contact),
    } for t in enquiry_types]
    
    context = {
        "hero": HeroSection.load(),
        "hero_features": HeroFeature.objects.filter(is_active=True),
        "service": ServiceSection.load(),
        "service_items": ServiceItem.objects.filter(is_active=True),
        "prod_section": prod_section,
        "products": products,
        "about": AboutSection.load(),
        "about_cards": AboutCard.objects.filter(is_active=True),
        "sales": SalesSection.load(),
        "sales_cards": SalesCard.objects.filter(is_active=True),
        "setup": SetupSection.load(),
        "setup_tags": SetupTag.objects.filter(is_active=True),
        "why": WhySection.load(),
        "why_cards": WhyCard.objects.filter(is_active=True),
        "cta": CtaSection.load(),
        "rv": ReviewSection.load(),
        "reviews": Review.objects.filter(is_active=True),
        "contact": contact,
        "contact_info": ContactInfo.objects.filter(is_active=True),
        "enquiry_types": enquiry_types,
        "enquiry_data": enquiry_data,
    }
    return render(request, "core/index.html", context)

@require_POST
def _send_review_mail(subject, body, to):
    try:
        send_mail(subject, body, None, [to], fail_silently=False)
        print("✅ Review email sent to", to)
    except Exception as e:
        print("❌ Review email FAILED:", repr(e))

def _send_review_mail(subject, body, to):
    try:
        send_mail(subject, body, None, [to], fail_silently=False)
        print("✅ Review email sent to", to)
    except Exception as e:
        print("❌ Review email FAILED:", repr(e))


@require_POST
def submit_review(request):
    rv = ReviewSection.load()

    if request.POST.get("website"):                      # honeypot
        return JsonResponse({"ok": True, "message": rv.success_message})

    if time.time() - request.session.get("last_review_ts", 0) < 30:
        return JsonResponse({"ok": False, "error": "Please wait a little before sending another review."}, status=429)

    name = request.POST.get("name", "").strip()[:80]
    text = request.POST.get("text", "").strip()[:400]
    try:
        rating = int(request.POST.get("rating", 0))
    except ValueError:
        rating = 0

    errors = {}
    if len(name) < 2:
        errors["name"] = "Please enter your name."
    if not 1 <= rating <= 5:
        errors["rating"] = "Please choose a rating."
    if len(text) < 10:
        errors["text"] = "Please write at least 10 characters."
    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    colors = ["violet", "orange", "purple"]
    Review.objects.create(
        name=name, rating=rating, text=text,
        avatar_color=colors[Review.objects.count() % 3],
        order=(Review.objects.aggregate(m=Max("order"))["m"] or 0) + 1,
        is_active=rv.auto_publish, from_website=True,
    )
    request.session["last_review_ts"] = time.time()

    # email notification to admin
    if rv.notify_email:
        link = request.build_absolute_uri(reverse("admin:core_pendingreview_changelist"))
        body = (
            f"New customer review on the Tech G website\n\n"
            f"Name: {name}\nRating: {rating}/5\nReview: {text}\n"
            f"Status: {'Published' if rv.auto_publish else 'Waiting for your approval'}\n\n"
            f"Review it here: {link}"
        )
        threading.Thread(
            target=_send_review_mail,
            args=(f"New review from {name} ({rating} stars)", body, rv.notify_email),
            daemon=True,
        ).start()
    else:
        print("ℹ️ Notify email is empty in admin, so no email was sent")

    return JsonResponse({"ok": True, "message": rv.success_message})

def _send_enquiry_mail(subject, body, to, enquiry_id):
    try:
        send_mail(subject, body, None, [to], fail_silently=False)
        status = f"Email sent to {to}"
    except Exception as e:
        status = "Email FAILED: " + repr(e)[:170]
    print(status)
    Enquiry.objects.filter(pk=enquiry_id).update(mail_status=status[:200])


def _send_whatsapp_auto(number, text, key, enquiry_id):
    ok, info = send_whatsapp(number, text, key)
    status = ("WhatsApp OK - " if ok else "WhatsApp FAILED - ") + info
    print(status)
    Enquiry.objects.filter(pk=enquiry_id).update(wa_status=status[:200])

@require_POST
def submit_enquiry(request):
    c = ContactSection.load()

    if request.POST.get("website"):                      # honeypot
        return JsonResponse({"ok": True, "message": c.success_message})

    if time.time() - request.session.get("last_enquiry_ts", 0) < 20:
        return JsonResponse({"ok": False, "error": "Please wait a few seconds before sending another enquiry."}, status=429)

    name = " ".join(request.POST.get("name", "").split())[:60]
    phone = re.sub(r"[\s\-]", "", request.POST.get("phone", ""))
    message = request.POST.get("message", "").strip()[:800]

    try:
        etype = (EnquiryType.objects.filter(pk=int(request.POST.get("enquiry_type", 0)), is_active=True)
                 .prefetch_related("products", "custom_fields").first())
    except (TypeError, ValueError):
        etype = None
    if not etype:
        return JsonResponse({"ok": False, "error": "Please choose an enquiry type."}, status=400)

    errors, answers = _clean_answers(request.POST, _fields_for(etype, c))
    if len(name) < 3:
        errors["name"] = "Name must be at least 3 characters."
    if not re.fullmatch(r"\d{10}", phone):
        errors["phone"] = "Enter a valid 10-digit phone number (without country code)."
    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    by_key = {f["key"]: val for f, val in answers}
    enq = Enquiry.objects.create(
        enquiry_type=etype.title, name=name, phone=phone,
        products=by_key.get("products", ""), quantity=by_key.get("quantity", ""), specs=by_key.get("specs", ""),
        details="\n".join(f"{f['label']}: {val}" for f, val in answers), message=message,
    )
    request.session["last_enquiry_ts"] = time.time()

    lines = [f"*New enquiry - {etype.title}*", f"Name: {name}", f"Phone: +{c.country_code} {phone}"]
    lines += [f"{f['label']}: {val}" for f, val in answers]
    if message:
        lines.append(f"Message: {message}")
    text = "\n".join(lines)

    # 1) email to admin (SMTP)
    if c.notify_email:
        link = request.build_absolute_uri(reverse("admin:core_enquiry_changelist"))
        threading.Thread(
            target=_send_enquiry_mail,
            args=(f"New enquiry: {etype.title} - {name}",
                  text.replace("*", "") + f"\n\nOpen in admin: {link}", c.notify_email, enq.pk),
            daemon=True,
        ).start()
    else:
        Enquiry.objects.filter(pk=enq.pk).update(mail_status="Skipped: Notify email is empty in admin")

    # 2) automatic WhatsApp to shop number
    wa_number = re.sub(r"\D", "", c.whatsapp_number)
    if c.send_whatsapp_auto and wa_number:
        threading.Thread(
            target=_send_whatsapp_auto,
            args=(wa_number, text, c.callmebot_api_key, enq.pk),
            daemon=True,
        ).start()
    else:
        Enquiry.objects.filter(pk=enq.pk).update(
            wa_status="Skipped: 'Send whatsapp auto' is OFF or WhatsApp number is empty")

    data = {"ok": True, "message": c.success_message}
    # 3) click-to-chat button for the customer
    if c.show_whatsapp_button and wa_number:
        data["whatsapp_url"] = f"https://wa.me/{wa_number}?text={quote(text)}"
    return JsonResponse(data)