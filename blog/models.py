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


#### this is the blog
# @register_snippet
class BlogCategory(models.Model):
    page = ParentalKey(
        "blog.BlogIndexPage",
        related_name="categories",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, verbose_name="Catégorie")
    slug = models.SlugField(unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class ArticleType(models.TextChoices):
    TECH = "tech", "Tech"
    ACTUALITES = "actualites", "Actualités"
    INTERNES = "internes", "Interne"
    CULTURE = "culture", "Culture d’entreprise"



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
        InlinePanel("categories", label="Catégories"),
        

    ]

    class Meta:
        verbose_name = "Page Index du Blog"

    # subpage_types = ["blog.ArticlePage"]

    def get_context(self, request):
        context = super().get_context(request)
        # Get all child blog pages
        context["posts"] = self.get_children().live().order_by("-first_published_at")
        return context
    
    subpage_types = ["BlogPage"]
    # parent_page_types = ['wagtailcore.Page']



class BlogPage(Page):
    subtitle = models.CharField(max_length=250, blank=True)
    type = models.CharField(
        max_length=50,
        choices=ArticleType.choices,
        default=ArticleType.TECH,
        verbose_name="Type d’article",
    )
    categories = models.ManyToManyField(
        "blog.BlogCategory",
        related_name="articles",
        blank=True,
        verbose_name="Catégories"
    )
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
   
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("quote", blocks.BlockQuoteBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("type"),
                FieldPanel("categories", widget=CheckboxSelectMultiple),
                FieldPanel("date"),
                FieldPanel("image"),
            ],
            heading="Informations",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []
