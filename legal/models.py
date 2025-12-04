from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class LegalPage(Page):
    """Page model for 'Mentions légales & RGPD' (Legal Notices & GDPR)"""

    hero_title = models.CharField(
        max_length=255,
        default="Mentions Légales & RGPD",
        verbose_name="Titre principal",
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    # Legal Information
    legal_title = models.CharField(
        max_length=255,
        default="Mentions Légales",
        verbose_name="Titre des mentions légales",
    )

    legal_content = RichTextField(
        blank=True,
        verbose_name="Contenu des mentions légales",
        help_text="Informations légales sur l'entreprise, l'éditeur du site, etc.",
    )

    # Privacy Policy
    privacy_title = models.CharField(
        max_length=255,
        default="Politique de Confidentialité",
        verbose_name="Titre de la politique de confidentialité",
    )

    privacy_content = RichTextField(
        blank=True, verbose_name="Contenu de la politique de confidentialité"
    )

    # GDPR
    gdpr_title = models.CharField(
        max_length=255,
        default="Protection des Données (RGPD)",
        verbose_name="Titre RGPD",
    )

    gdpr_content = RichTextField(
        blank=True,
        verbose_name="Contenu RGPD",
        help_text="Informations sur la protection des données personnelles",
    )

    # Cookies
    cookies_title = models.CharField(
        max_length=255,
        default="Politique des Cookies",
        verbose_name="Titre de la politique des cookies",
    )

    cookies_content = RichTextField(
        blank=True, verbose_name="Contenu de la politique des cookies"
    )

    # Terms of Use
    terms_title = models.CharField(
        max_length=255,
        default="Conditions d'Utilisation",
        verbose_name="Titre des conditions d'utilisation",
    )

    terms_content = RichTextField(
        blank=True, verbose_name="Contenu des conditions d'utilisation"
    )

    last_updated = models.DateField(
        null=True, blank=True, verbose_name="Dernière mise à jour"
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("introduction"),
        FieldPanel("legal_title"),
        FieldPanel("legal_content"),
        FieldPanel("privacy_title"),
        FieldPanel("privacy_content"),
        FieldPanel("gdpr_title"),
        FieldPanel("gdpr_content"),
        FieldPanel("cookies_title"),
        FieldPanel("cookies_content"),
        FieldPanel("terms_title"),
        FieldPanel("terms_content"),
        FieldPanel("last_updated"),
    ]

    class Meta:
        verbose_name = "Page Légale"
