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

class PostIndexPage(Page):
    intro = RichTextField(blank=True)
    
    @property
    def posts(self):
        #get list of live blog pages that are descendant of this
        posts = PostPage.objects.live().descendant_of(self)

        posts = posts.order_by('-date')

        return posts

    def get_context(self, request):
        posts = self.posts

        tag = request.GET.get('tag')
        if tag:
            posts = posts.filter(tags__name=tag)

        page = request.GET.get('page')

        paginator = Paginator(posts, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = super(PostIndexPage, self).get_context(request)
        context['posts'] = posts
        return context

PostIndexPage.content_panels = [
    FieldPanel('title', classname='title')
    FieldPanel('intro', classname='full')
]


PostIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations")
]

class PostPageTag(TaggedItemBase):
    content_object = ParentalKey('posts.PostPage', related_name='tagged_items')

class PostPage(Page):
    body = RichTextField()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField('Post Date')
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    @property
    def post_index(self):
        return self.get_ancestors().type(PostIndexPage).last()


PostIndexPage.content_panels = [
    FieldPanel('title', classname='title')
    FieldPanel('date'),
    FieldPanel('body', classname='full')
]


PostIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations")
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]



