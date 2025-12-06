from django.db import models
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    """Enhanced homepage with hero section and features"""

    # Hero Section
    hero_title = models.CharField(
        max_length=255, default="Bienvenue", verbose_name="Titre principal"
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

    hero_cta_text = models.CharField(
        max_length=50, default="En savoir plus", verbose_name="Texte du bouton CTA"
    )

    hero_cta_link = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Lien du bouton CTA",
        help_text="URL relative (ex: /expertise/) ou absolue",
    )

    # Introduction
    introduction = RichTextField(blank=True, verbose_name="Introduction")

    # Services Section
    services_title = models.CharField(
        max_length=255,
        default="Nos Services",
        verbose_name="Titre de la section services",
    )

    services_description = RichTextField(
        blank=True, verbose_name="Description des services"
    )

    # Statistics Section
    stats_title = models.CharField(
        max_length=255,
        default="Nos Chiffres",
        verbose_name="Titre de la section statistiques",
    )

    # Call to Action
    cta_title = models.CharField(
        max_length=255,
        default="Prêt à démarrer votre projet ?",
        verbose_name="Titre CTA final",
    )

    cta_description = models.TextField(blank=True, verbose_name="Description CTA final")

    cta_button_text = models.CharField(
        max_length=50,
        default="Contactez-nous",
        verbose_name="Texte du bouton CTA final",
    )
    # seo_title = models.CharField(max_length=255, blank=True)
    # seo_description = models.TextField(blank=True)
    
    
    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("hero_cta_text"),
        FieldPanel("hero_cta_link"),
        FieldPanel("introduction"),
        FieldPanel("services_title"),
        FieldPanel("services_description"),
        FieldPanel("stats_title"),
        FieldPanel("cta_title"),
        FieldPanel("cta_description"),
        FieldPanel("cta_button_text"),
        # MultiFieldPanel([FieldPanel('seo_title'), FieldPanel('seo_description')], heading="SEO"),
        
    ]

    class Meta:
        verbose_name = "Page d'Accueil"
