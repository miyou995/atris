from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField,StreamField
from wagtail.models import Page
from wagtail import blocks
from modelcluster.fields import ParentalKey
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.forms.models import AbstractFormField,AbstractEmailForm
from wagtail.contrib.forms.models import AbstractFormSubmission
from django.shortcuts import redirect, render

# from wagtail.admin.panels import StreamFieldPanel


class ContractType(models.Model):
    page = ParentalKey(
        "recruitment.RecruitmentIndexPage",
        related_name="contract_types",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, verbose_name="Type de contrat")
    panels = [
        FieldPanel("name"),
    ]
    def __str__(self):
        return self.name


class TestimonialCollaboratorBlock(blocks.StructBlock):
    name = blocks.CharBlock(label="Nom")
    role = blocks.CharBlock(label="Poste")
    quote = blocks.TextBlock(label="Citation")
    photo = ImageChooserBlock(label="Photo", required=False)

    class Meta:
        icon = "user"
        label = "Témoignage Collaborateur"


# Contenu ambiance interne
class CultureBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(label="Texte")
    image = ImageChooserBlock(label="Image",required=False)
    video = blocks.URLBlock(label="Vidéo (YouTube/Vimeo)", required=False)

    class Meta:
        icon = "pick"
        label = "Ambiance / Culture interne"


class JobApplicationFormField(AbstractFormField):
    page = ParentalKey(
        'recruitment.RecruitmentIndexPage',
        related_name='form_fields',
        on_delete=models.CASCADE
    )

class JobApplicationSubmission(AbstractFormSubmission):
    page = models.ForeignKey(
        'recruitment.RecruitmentIndexPage',
        on_delete=models.CASCADE,
        related_name='submissions'
    )


class RecruitmentIndexPage(AbstractEmailForm):
    submission_class = JobApplicationSubmission


    hero_title = models.CharField(
        max_length=255, default="Rejoignez Notre Équipe", verbose_name="Titre principal"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )
    introduction = RichTextField(blank=True)

    culture = StreamField(
        [("element", CultureBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Ambiance / Culture interne"
    )
    testimonials = StreamField(
        [("testimonial", TestimonialCollaboratorBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Témoignages collaborateurs"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        InlinePanel("contract_types", label="Types de contrat"),
        InlinePanel("form_fields", label="Application Fields"),  
        FieldPanel("culture"),
        FieldPanel("testimonials"),
        # InlinePanel("contract_type", label="Types de contrat"),
    ]
    subpage_types = ["RecruitmentPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        jobs = self.get_children().live().specific()

        contract_type_id = request.GET.get("type")
        if contract_type_id:
            jobs = [
                job for job in jobs
                if job.contract_type and str(job.contract_type.id) == contract_type_id
            ]
        context["jobs"] = jobs
        context["selected_contract_type"] = contract_type_id

    
        return context
    def serve(self, request):
        if request.method == 'POST':
            form = self.get_form(request.POST, request.FILES)
            if form.is_valid():
                self.process_form_submission(form)
                return redirect(self.url)  


        return super().serve(request)



class RecruitmentPage(Page):
    contract_type = models.ForeignKey(
        ContractType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recruitment_pages",
        verbose_name="Type de contrat",
    )
    job_title = models.CharField(max_length=255,verbose_name="Poste")
    location = models.CharField(max_length=255, blank=True,verbose_name="Localisation")
    body = RichTextField(blank=True, verbose_name="Description")
    salary = models.CharField(max_length=255, blank=True,verbose_name="Salaire")


    # description = StreamField([
    #     ('content', blocks.StreamBlock([
    #         ("text", blocks.RichTextBlock()),
    #         ("list", blocks.ListBlock(blocks.CharBlock(), label="Liste")),
    #     ])),
       
    # ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("contract_type"),
        FieldPanel("job_title"),
        # FieldPanel("introduction"),
        FieldPanel("location"),
        FieldPanel("body"),
        FieldPanel("salary"),
        ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        parent = self.get_parent().specific
        form = parent.get_form(request.POST or None, request.FILES or None)

        context["form"] = form

        if request.method == "POST" and form.is_valid():
            context["success"] = True

        return context
    
    class Meta:
        verbose_name = "Page Recrutement"


    parent_page_types = ["recruitment.RecruitmentIndexPage"]
    subpage_types = []
