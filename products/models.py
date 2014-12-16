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

class ProductIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ['products.ProductPage',]

    @property
    def products(self):
        products = ProductPage.objects.live().descendant_of(self)
    
        return products

    def get_context(self, request):
        products = self.products



        tag = request.GET.get('tag')
        if tag:
            products = products.filter(tags__name=tag)



        page = request.GET.get('page')

        paginator = Paginator(products, 15)

        try:
            products = paginator.page(page)

        except PageNotAnInteger:
            products = paginator.page(1)

        except EmptyPage:
            products = paginator.page(paginator.num_pages)


        context = super(ProductIndexPage, self).get_context(request)
        context['products'] = products


        return context

ProductIndexPage.content_panels = [
    FieldPanel('title', classname='title'),
    FieldPanel('intro', classname='full'),
]


ProductIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),
]

class ProductPageTag(TaggedItemBase):
   content_object = ParentalKey('products.ProductPage', related_name='tagged_items') 

class ProductPage(Page, Orderable):
    body = RichTextField()
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True)
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
    def product_index(self):
        return self.get_ancestors().type(ProductIndexPage).last()


ProductPage.content_panels = [
    FieldPanel('title', classname='title'),
    FieldPanel('date'),
    FieldPanel('body', classname='full'),
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]


ProductPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page Configurations"),
]


