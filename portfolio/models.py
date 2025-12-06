from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index


class PortfolioIndexPage(Page):
    """Index page for 'Réalisations / Clients' (Portfolio/Clients)"""

    hero_title = models.CharField(
        max_length=255, default="Nos Réalisations", verbose_name="Titre principal"
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    clients_title = models.CharField(
        max_length=255,
        default="Nos Clients",
        verbose_name="Titre de la section clients",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("introduction"),
        FieldPanel("clients_title"),
        InlinePanel("client_logos", label="Logos des clients"),
    ]

    class Meta:
        verbose_name = "Page Index du Portfolio"

    def get_context(self, request):
        context = super().get_context(request)
        # Get all child portfolio pages
        context["projects"] = self.get_children().live().specific()
        return context


class ClientLogo(Orderable):
    """Client logo for the portfolio index page"""

    page = ParentalKey(
        PortfolioIndexPage, on_delete=models.CASCADE, related_name="client_logos"
    )

    client_name = models.CharField(max_length=255, verbose_name="Nom du client")

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo",
    )

    panels = [
        FieldPanel("client_name"),
        FieldPanel("logo"),
    ]


class PortfolioPage(Page):
    """Individual portfolio/project page"""

    client_name = models.CharField(
        max_length=255, blank=True, verbose_name="Nom du client"
    )

    project_date = models.DateField(
        null=True, blank=True, verbose_name="Date du projet"
    )

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )

    summary = models.TextField(max_length=500, blank=True, verbose_name="Résumé")

    challenge = RichTextField(blank=True, verbose_name="Défi / Problématique")

    solution = RichTextField(blank=True, verbose_name="Solution apportée")

    results = RichTextField(blank=True, verbose_name="Résultats")

    technologies = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Technologies utilisées",
        help_text="Séparées par des virgules",
    )

    project_url = models.URLField(blank=True, verbose_name="URL du projet")

    search_fields = Page.search_fields + [
        index.SearchField("client_name"),
        index.SearchField("summary"),
        index.SearchField("challenge"),
    ]
    gallery_images = InlinePanel('gallery', label="Galerie")

    content_panels = Page.content_panels + [
        FieldPanel("client_name"),
        FieldPanel("project_date"),
        FieldPanel("featured_image"),
        FieldPanel("summary"),
        FieldPanel("challenge"),
        FieldPanel("solution"),
        FieldPanel("results"),
        FieldPanel("technologies"),
        FieldPanel("project_url"),
        InlinePanel("gallery_images", label="Galerie d'images"),
    ]

    class Meta:
        verbose_name = "Page Projet"

    parent_page_types = ["portfolio.PortfolioIndexPage"]


class PortfolioGalleryImage(Orderable):
    """Gallery images for portfolio pages"""

    page = ParentalKey(
        PortfolioPage, on_delete=models.CASCADE, related_name="gallery_images"
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Image",
    )

    caption = models.CharField(max_length=255, blank=True, verbose_name="Légende")

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]
