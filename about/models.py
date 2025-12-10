from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page


class AboutPage(Page):
    """Page model for 'Qui sommes-nous ?' (About Us)"""

    hero_title = models.CharField(
        max_length=255, default="Qui sommes-nous ?", verbose_name="Titre principal"
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

    mission_title = models.CharField(
        max_length=255, default="Notre Mission", verbose_name="Titre de la mission"
    )

    mission_content = RichTextField(blank=True, verbose_name="Contenu de la mission")

    vision_title = models.CharField(
        max_length=255, default="Notre Vision", verbose_name="Titre de la vision"
    )

    vision_content = RichTextField(blank=True, verbose_name="Contenu de la vision")

    values_title = models.CharField(
        max_length=255, default="Nos Valeurs", verbose_name="Titre des valeurs"
    )

    values_content = RichTextField(blank=True, verbose_name="Contenu des valeurs")

    timeline = StreamField([
        ("items",blocks.ListBlock(
            blocks.StructBlock([
                ('year', blocks.CharBlock(required=True,label="année")),
                ('event', blocks.TextBlock(required=True,label='événement')),
                ('description', blocks.TextBlock(required=True,label='description')),
            ])
        ))
        ], blank=True, use_json_field=True)
    timeline.verbose_name = "histoire"
    
    key_numbers = StreamField([
        ("numbers", blocks.ListBlock(
            blocks.StructBlock([
                ('number', blocks.CharBlock(required=True,label="chiffre")),
                ('label', blocks.CharBlock(required=True,label="label")),
            ])
        ))
        ], blank=True, use_json_field=True)
    key_numbers.verbose_name = "chiffres clés"
    
    leadership = StreamField([
            ("members", blocks.ListBlock(
                blocks.StructBlock([
                    ('photo', ImageChooserBlock(required=False,label="photo")),
                    ('name', blocks.CharBlock(required=True,label="nom")),
                    ('position', blocks.CharBlock(required=True,label="position")),
                    ('bio', blocks.TextBlock(required=True,label="bio")),
                ])
            ))
            ], blank=True, use_json_field=True)
    leadership.verbose_name = "équipe dirigeante"



    # team_title = models.CharField(
    #     max_length=255, default="Notre Équipe", verbose_name="Titre de l'équipe"
    # )

    # team_description = RichTextField(blank=True, verbose_name="Description de l'équipe")
    # seo_title = models.CharField(max_length=255, blank=True)
    # seo_description = models.TextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        # FieldPanel("mission_title"),
        # FieldPanel("mission_content"),
        FieldPanel("vision_title"),
        FieldPanel("vision_content"),
        FieldPanel("values_title"),
        FieldPanel("values_content"),
        FieldPanel("timeline"),
        FieldPanel("key_numbers"),
        FieldPanel("leadership"),
        # MultiFieldPanel([FieldPanel('seo_title'), FieldPanel('seo_description')], heading="SEO"),
    ]
    
    class Meta:
        verbose_name = "Page À Propos"

    # parent_page_types = ['myapp.HomePage'] 
    subpage_types = []
