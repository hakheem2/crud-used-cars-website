from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from cars.models import Car

# Static pages sitemap
class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['pages:home', 'pages:about', 'cars:car_list', 'pages:contact', 'articles:article_list']  # URL names

    def location(self, item):
        return reverse(item)


# Dynamic car pages sitemap
class CarSitemap(Sitemap):
    protocol = "https"
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Car.objects.all()

    def location(self, obj):
        # Reverse URL using slug
        return reverse('cars:car_detail', kwargs={'slug': obj.slug})