from django.conf import settings
import string, random
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    
    class Meta:
        verbose_name = 'categories'

    def __str__(self):
        return (self.name)

    def get_absolute_url(self):
        return reverse("home")
    
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Article(models.Model):
    
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    
    
     
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=False, blank=True, max_length=255,  unique=True)
    image = models.ImageField(upload_to='images')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  related_name='category')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    created_at = models.DateTimeField(auto_now_add=True)




   
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created_at',)
        
    
    
    def get_absolute_url(self):
        return reverse('blog_details', kwargs={"slug": self.slug})

    def unique_slug_generator(instance, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(instance.title)
        Klass = instance.__class__
        max_length = Klass._meta.get_field('slug').max_length
        slug = slug[:max_length]
        qs_exists = Klass.objects.filter(slug=slug).exists()

        if qs_exists:
            new_slug = "{slug}-{randstr}".format(
                slug = slug[:max_length-5], randstr = random_string_generator(size = 4))

            return instance.unique_slug_generator(new_slug=new_slug)
        return slug


    def save(self, *args, **kwargs): # new
         if not self.slug:
            self.slug = self.unique_slug_generator()
            return super().save(*args, **kwargs)

    tags = TaggableManager()
    objects = models.Manager() # The default manager.
    published = PublishedManager()
    

class Comment(models.Model): # new
    article = models.ForeignKey(Article, on_delete=models.CASCADE,  related_name='comments',)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, default=1)
   
    
    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('article_list')

class About(models.Model):
    description = models.TextField()
    

class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    title = models.CharField(max_length=500)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-date',)
    
    
    