from django.db import models
from wagtail.admin.panels import FieldPanel,InlinePanel
from wagtail.fields import RichTextField,StreamField
from wagtail.models import Page
from wagtail import blocks
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
# from wagtail.admin.panels import StreamFieldPanel
from wagtail.snippets.models import register_snippet
from django.forms import CheckboxSelectMultiple
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager




class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogIndexPage(Page):
    """Index page for Blog / Insights"""

    hero_title = models.CharField(
        max_length=255, default="Blog & Insights", verbose_name="Titre principal"
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

    intro = RichTextField(blank=True, verbose_name="Introduction")


    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("intro"),
        FieldPanel("hero_image"),

    ]

    class Meta:
        verbose_name = "Page Index du Blog"

    # subpage_types = ["blog.ArticlePage"]

    def get_context(self, request):
        context = super().get_context(request)
        tag = request.GET.get('tag')

        posts = self.get_children().live().specific().order_by("-first_published_at")

        if tag:
            posts = posts.filter(tags__name=tag)

        context["posts"] = posts
        context["selected_tag"] = tag
        return context
    
    subpage_types = ["BlogPage"]
    # parent_page_types = ['wagtailcore.Page']

#addeded vcomment 

class BlogPage(Page):
    tags = ClusterTaggableManager(through="blog.BlogPageTag", blank=True)
    subtitle = models.CharField(max_length=250, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de couverture"
    )
    date = models.DateField('Date')
    author = models.CharField(max_length=255, blank=True,verbose_name="auteur")
    reading_time = models.IntegerField(blank=True, null=True, verbose_name="Temps de lecture")
    content = RichTextField(blank=True, verbose_name="Contenu")
   
    # body = StreamField(
    #     [
    #         ("paragraph", blocks.RichTextBlock()),
    #         ("image", ImageChooserBlock()),
    #         ("quote", blocks.BlockQuoteBlock()),
    #     ],
    #     use_json_field=True,
    #     blank=True,
    # )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("date"),
                FieldPanel("image"),
                FieldPanel("tags"),    
                FieldPanel("content"),
            ],
            heading="Informations",
        ),
        # FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []
