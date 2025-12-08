from django.db import models
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
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
    legal_notice = RichTextField(
        blank=True,
        verbose_name="Mentions légales"
    )

    privacy_policy = RichTextField(
        blank=True,
        verbose_name="Politique de confidentialité"
    )

    cookies_policy = RichTextField(
        blank=True,
        verbose_name="Politique de cookies"
    )

    rgpd_rights = RichTextField(
        blank=True,
        verbose_name="Droits RGPD"
    )


    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("legal_notice"),
            ],
            heading="Mentions légales",
        ),

        MultiFieldPanel(
            [
                FieldPanel("privacy_policy"),
            ],
            heading="Politique de confidentialité",
        ),

        MultiFieldPanel(
            [
                FieldPanel("cookies_policy"),
            ],
            heading="Politique de cookies",
        ),

        MultiFieldPanel(
            [
                FieldPanel("rgpd_rights"),
            ],
            heading="Droits RGPD",
        ),
    ]

    class Meta:
        verbose_name = "Page Légale"

    subpage_types = []
