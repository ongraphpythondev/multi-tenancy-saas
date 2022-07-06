from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Profile, Tag, Article
from tenant.models import Domain
# Django Q objects use to create complex queries
# https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
from django.db.models import Q
from django_tenants.utils import remove_www
from django.views.decorators.csrf import csrf_exempt 
def home(request):

    # # feature articles on the home page
    featured = Article.articlemanager.filter(featured=True)[0:3]
    print("feature",featured)
    # context = {
    #     'articles': featured
    # }

    # return render(request, 'index.html', context)
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    name = domain.tenant.blog_name
    print(name)
    #.
    #.
    context = {
        'name': name,
        'articles': featured
        
    }
    return render(request, 'index.html', context)

@csrf_exempt
def articles(request):
    # print(2)
    # get query from request
    query = request.POST.get('query')
    # print(query)
    # Set query to '' if None
    if query == None:
        query = ''

    # articles = Article.articlemanager.all()
    # search for query in headline, sub headline, body
    articles = Article.articlemanager.filter(
        Q(headline__icontains=query) |
        Q(sub_headline__icontains=query) |
        Q(body__icontains=query)
    )

    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'tags': tags,
    }

    return render(request, 'articles.html', context)


def article(request, article):

    article = get_object_or_404(Article, slug=article, status='published')
    print(1)
    context = {
        'article': article
    }

    return render(request, 'article.html', context)
