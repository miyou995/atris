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

    cta_linked_page = models.ForeignKey(
            'wagtailcore.Page',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name="Lien du bouton CTA",
            related_name='+', # Use '+' to avoid reverse accessor clashes
        )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    cta_button_text = models.CharField(
        max_length=50,
        default="Contactez-nous",
        verbose_name="Texte du bouton CTA final",
    )
    button_linked_page = models.ForeignKey(
            'wagtailcore.Page',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name="Lien du bouton CTA final",
            related_name='+', # Use '+' to avoid reverse accessor clashes
        )
    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        FieldPanel("hero_cta_text"),
        FieldPanel("cta_linked_page"),
        FieldPanel("cta_button_text"),
        FieldPanel("button_linked_page"),
        
    ]
    
    @classmethod
    def can_create_at(cls, parent):
        # Only one HomePage allowed, under the root page (wagtailcore.Page)
        return super().can_create_at(parent) and not cls.objects.exists()

    class Meta:
        verbose_name = "Page d'Accueil"

    
