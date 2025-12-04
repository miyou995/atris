from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class RecruitmentPage(Page):
    """Page model for 'Recrutement' (Recruitment)"""

    hero_title = models.CharField(
        max_length=255, default="Rejoignez Notre Équipe", verbose_name="Titre principal"
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    why_join_title = models.CharField(
        max_length=255,
        default="Pourquoi nous rejoindre ?",
        verbose_name="Titre 'Pourquoi nous rejoindre'",
    )

    why_join_content = RichTextField(
        blank=True, verbose_name="Contenu 'Pourquoi nous rejoindre'"
    )

    culture_title = models.CharField(
        max_length=255, default="Notre Culture", verbose_name="Titre de la culture"
    )

    culture_content = RichTextField(blank=True, verbose_name="Contenu de la culture")

    benefits_title = models.CharField(
        max_length=255, default="Avantages", verbose_name="Titre des avantages"
    )

    benefits_content = RichTextField(blank=True, verbose_name="Contenu des avantages")

    open_positions_title = models.CharField(
        max_length=255,
        default="Postes Ouverts",
        verbose_name="Titre des postes ouverts",
    )

    open_positions_content = RichTextField(
        blank=True,
        verbose_name="Contenu des postes ouverts",
        help_text="Listez les postes actuellement ouverts",
    )

    application_email = models.EmailField(
        blank=True,
        verbose_name="Email de candidature",
        help_text="Email pour recevoir les candidatures",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        FieldPanel("why_join_title"),
        FieldPanel("why_join_content"),
        FieldPanel("culture_title"),
        FieldPanel("culture_content"),
        FieldPanel("benefits_title"),
        FieldPanel("benefits_content"),
        FieldPanel("open_positions_title"),
        FieldPanel("open_positions_content"),
        FieldPanel("application_email"),
    ]

    class Meta:
        verbose_name = "Page Recrutement"
