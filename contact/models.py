from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class FormField(AbstractFormField):
    """Custom form field for contact form"""

    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactPage(AbstractEmailForm):
    """Page model for 'Contact' with integrated form"""

    hero_title = models.CharField(
        max_length=255, default="Contactez-Nous", verbose_name="Titre principal"
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    # Contact Information
    address = models.TextField(blank=True, verbose_name="Adresse")

    phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")

    email = models.EmailField(blank=True, verbose_name="Email")

    office_hours = models.CharField(
        max_length=255, blank=True, verbose_name="Horaires d'ouverture"
    )

    # Map
    map_embed_code = models.TextField(
        blank=True,
        verbose_name="Code d'intégration de la carte",
        help_text="Code iframe de Google Maps ou autre service de cartographie",
    )

    # Form settings
    thank_you_text = RichTextField(
        blank=True,
        verbose_name="Message de remerciement",
        help_text="Texte affiché après la soumission du formulaire",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("introduction"),
        FieldPanel("address"),
        FieldRowPanel(
            [
                FieldPanel("phone"),
                FieldPanel("email"),
            ]
        ),
        FieldPanel("office_hours"),
        FieldPanel("map_embed_code"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FieldPanel("thank_you_text"),
        FormSubmissionsPanel(),
    ]

    class Meta:
        verbose_name = "Page Contact"
