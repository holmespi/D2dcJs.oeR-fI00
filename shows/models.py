from datetime import date
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.management import call_command
from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
InlinePanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from south.signals import post_migrate

class ShowIndexPage(Page):
    intro = RichTextField(blank=True)

    @property
    def shows(self):
        shows = ShowPage.objects.live().descendant_of(self)

        shows = shows.filter(date_from__gte=date.today())

        shows = shows.order_by('date')

        return shows

ShowIndexPage.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('intro', classname='full'),

]

IndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),

]

class ShowPage:
    date = models.DateField('date')
    venue = models.CharField(max_length=255)
    tickets = models.URLField(blank=True,Null=True)


    @property
    def show_index(self):
        return self.get_ancestors().type(ShowIndexPage).last()

ShowPage.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('date'),
    FieldPanel('tickets'),
]


ShowPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),
]










