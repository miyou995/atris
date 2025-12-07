from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks

class ExpertiseIndexPage(Page):
    """Index page for 'Nos expertises' (Our Expertise)"""

    hero_title = models.CharField(
        max_length=255, default="Nos Expertises", verbose_name="Titre principal"
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )
    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("introduction"),
        FieldPanel("hero_image"),

    ]
    subpage_type = ["ExpertisePage"]


    class Meta:
        verbose_name = "Page Index des Expertises"

    def get_context(self, request):
        context = super().get_context(request)
        # Get all child expertise pages
        context["expertises"] = self.get_children().live().specific()
        return context


class ExpertisePage(Page):
    """Individual expertise page"""
    subtitle = models.CharField(max_length=255, blank=True)
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
    body = StreamField([
        ("section", blocks.RichTextBlock()),
        ("image", ImageChooserBlock(required=False)),
        ("list", blocks.ListBlock(blocks.CharBlock(label="Point"))),
    ], use_json_field=True, blank=True)
    body.verbose_name="Le Contenu de la Page"


    content_panels = Page.content_panels + [
        FieldPanel("featured_image"),
        FieldPanel("summary"),
        FieldPanel("description"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Page Expertise"

    parent_page_types = ["expertise.ExpertiseIndexPage"]
