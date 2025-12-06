from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField,StreamField
from wagtail.models import Page
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
# from wagtail.admin.panels import StreamFieldPanel

class BlogIndexPage(Page):
    """Index page for Blog / Insights"""

    hero_title = models.CharField(
        max_length=255, default="Blog & Insights", verbose_name="Titre principal"
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    intro = RichTextField(blank=True, verbose_name="Introduction")

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("intro"),
    ]

    class Meta:
        verbose_name = "Page Index du Blog"

    def get_context(self, request):
        context = super().get_context(request)
        # Get all child blog pages
        context["posts"] = self.get_children().live().order_by("-first_published_at")
        return context



class BlogPage(Page):
    date = models.DateField('Date')
    author = models.CharField(max_length=255, blank=True,verbose_name="auteur")
    categories = models.CharField(max_length=255, blank=True, help_text='Comma separated categories')
    excerpt = models.TextField(blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('content', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    
    # def get_context(self,request):
    #     context = super().get_context(request)
    #     # Get all child blog pages
    #     context["blogs"] = self.get_children().live()
    #     return context

    content_panels = Page.content_panels + [
    FieldPanel('date'),
    FieldPanel('author'),
    FieldPanel('categories'),
    FieldPanel('excerpt'),
    FieldPanel('body'),
    ]