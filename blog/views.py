from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Article, Category, About, Contact
from django.views.generic import  ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q


# Create your views here.

class Contact_Us(TemplateView):
    template_name = 'contact.html'
   

class ArticleView(ListView):
    paginate_by = 10
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'items'
  
    
    def get_context_data(self, tag_slug=None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_post'] = self.model.objects.all()[:6]
        
        
        tag = None
        if tag_slug:
            context['items'] = self.model.objects.all()
            tag = get_object_or_404(Tag, slug=tag_slug)
            context["items"] = context['items'].filter(tags__in=[tag])
        
        
        return context

    
class ArticleDetails(DetailView):
    model = Article
    template_name = 'blog/details.html'
    context_object_name =  'item'
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         items = self.model.objects.get(slug=self.slug)
         item_tags = items.tags.all()
         similar_posts = self.model.published.filter(tags__in=item_tags).exclude(slug=self.slug)
         context['similar_posts'] = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:6]
         
        


def article_details(request, slug):
    item = Article.objects.get(slug=slug)
    item_tags = item.tags.all()
    similar_posts = Article.published.filter(tags__in=item_tags).exclude(slug=slug) 
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:6]  
    
    context = {
        "item": item,
        'similar_posts': similar_posts
        
    }
    
    return render(request, 'blog/details.html', context)


# Both functions  and class base cathegories views
def myCategory(request, category):
    category_list = Article.objects.get(category=category)
    context = {'category': category_list}
    return render(request, 'blog/category.html', context=context)

class Category_List(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    
    def get_queryset(self, category):
        category_list = Article.objects.get(category=category)
        return category_list


class Article_Create(CreateView):
    model = Article
    fields = ('title', 'image','body', 'category', 'status', 'tags')
    template_name = 'blog/create.html'
    success_url = reverse_lazy('homepage')
    
    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
    
class Article_Update(UpdateView):
    model = Article
    fields = ('title','image','body', 'category', 'status',)
    template_name = 'blog/update.html'
    success_url = reverse_lazy('homepage')
    
    
    
class Article_Delete(DeleteView):
    model = Article
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('homepage')
    
class Search_Page(ListView):
    template_name = 'blog/index.html'
    model = Article
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q') 
        object_list = Article.objects.filter(Q(title__icontains=query)| Q(body__icontains=query)) 
        return object_list


class About_View(ListView):
    template_name  = 'about.html'
    model = About
    context_object_name = 'about'