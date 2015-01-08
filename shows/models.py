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
    subpage_types = ['shows.ShowPage',]
    @property
    def shows(self):
        shows = ShowPage.objects.live().descendant_of(self)

        shows = shows.order_by('date')

        return shows

    def get_context(self, request):
        shows = self.shows

        tag = request.GET.get('tag')
        if tag:
            shows = shows.filter(tags__name=tag)

        page = request.GET.get('page')

        paginator = Paginator(shows, 5)
        try:
            shows = paginator.page(page)
        except PageNotAnInteger:
            shows = paginator.page(1)
        except EmptyPage:
            shows = paginator.page(paginator.num_pages)

        context = super(ShowIndexPage, self).get_context(request)
        context['shows'] = shows
        return context


ShowIndexPage.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('intro', classname='full'),

]

ShowIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),

]

class ShowPage(Page):
    date = models.DateField('date')
    venue = models.CharField(max_length=255)
    tickets = models.URLField(blank=True,)


    @property
    def show_index(self):
        return self.get_ancestors().type(ShowIndexPage).last()

ShowPage.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('date'),
    FieldPanel('tickets'),
    FieldPanel('venue'),
]


ShowPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),
]










