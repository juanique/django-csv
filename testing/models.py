from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return "<Country: %s>" % self.name



class City(models.Model):

    country = models.ForeignKey(Country, related_name='cities')
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return "<City: %s>" % self.name
