from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class ExpertiseIndexPage(Page):
    """Index page for 'Nos expertises' (Our Expertise)"""

    hero_title = models.CharField(
        max_length=255, default="Nos Expertises", verbose_name="Titre principal"
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("introduction"),
    ]

    class Meta:
        verbose_name = "Page Index des Expertises"

    def get_context(self, request):
        context = super().get_context(request)
        # Get all child expertise pages
        context["expertises"] = self.get_children().live().specific()
        return context


class ExpertisePage(Page):
    """Individual expertise page"""

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Nom de l'icône (ex: 'code', 'design', 'analytics')",
        verbose_name="Icône",
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

    description = RichTextField(blank=True, verbose_name="Description détaillée")

    key_points = RichTextField(
        blank=True,
        verbose_name="Points clés",
        help_text="Liste des points clés de cette expertise",
    )

    technologies = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Technologies utilisées",
        help_text="Séparées par des virgules",
    )

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("description"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("icon"),
        FieldPanel("featured_image"),
        FieldPanel("summary"),
        FieldPanel("description"),
        FieldPanel("key_points"),
        FieldPanel("technologies"),
    ]

    class Meta:
        verbose_name = "Page Expertise"

    parent_page_types = ["expertise.ExpertiseIndexPage"]
