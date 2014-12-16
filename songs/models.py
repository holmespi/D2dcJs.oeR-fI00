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

class SongIndexPage(Page):
    intro = RichTextField(blank=True)

    @property
    def songs(self):
        songs = SongPage.objects.live().descendant_of(self)

        return songs

SongIndexPage.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('intro', classname='full'),

]

SongIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),
]

class SongPage:
    about = RichTextField(blank=True)
    song = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )



SongPage.content_panels = [
    FieldPanel('title', classname='title'),
    FieldPanel('date'),
    FieldPanel('body', classname='full'),
    DocumentChooserPanel('song'),
]


SongPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),
    ImageChooserPanel('feed_image'),
]


