from datetime import datetime
from email import message
import email
import imp
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
from bs4 import BeautifulSoup as bs
import datetime

from .models import Article, Website

# Create your views here.

def index(request):

    if request.method == 'POST':

        ## Scrap Websites
        website_url = request.POST['website_url']
        r = requests.get(website_url)
        soup = bs(r.content, 'html.parser')
        website_name = soup.find('title').get_text()
        website_link = website_url
        created_At = datetime.datetime.now().date()
        last_Scrapped = datetime.datetime.now().time()

        # Save websites to Data Base
        new_website = Website(
            websiteName = website_name,
            websiteLink = website_link,
            createdAt = created_At,
            lastScrappedAt = last_Scrapped
        )
        new_website.save()

        ## Scrap Articles
        
        articles_dict = {"article_title":[], "article_dom":[], "article_desc":[], "article_link":[]}

        ''' Scrapping Articles Data 
        '''
        for item in soup.find_all('article', class_= "item-list"):
            title = item.select_one("h2").get_text()
            articles_dict['article_title'].append(title)
            articles_dict['article_dom'].append(item) 
        
        for x in soup.find_all('div', {"class": "entry"}):
            desc = x.select_one("p").get_text()
            link = x.select_one("a")['href']
            articles_dict['article_desc'].append(desc)
            articles_dict['article_link'].append(link)

        # Save articles to Data Base
        for index in range(len(articles_dict['article_title'])):
            new_article = Article(
                website_ID   = new_website,
                articleTitle = articles_dict["article_title"][index],
                articleDesc  = articles_dict["article_desc"][index],
                articleDOM   = str(articles_dict["article_dom"][index]) ,
                articleLink  = articles_dict["article_link"][index]
                )
            new_article.save()

        messages.info(request, 'Scrapping is completed')
        redirect('/')
        
    return render(request, 'index.html')


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password ==  password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already registered')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Password not Matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'signup.html')


def log_me_in(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def log_me_out(request):

    logout(request)
    return redirect('login')
    

def websites(request):
    my_websites = Website.objects.all()
    return render(request, 'websites.html', {'my_websites':my_websites})

def articles(request):
    my_articles = Article.objects.all()
    return render(request, 'articles.html', {'my_articles':my_articles})

def update_websites(request,id):

    website = Website.objects.get(pk=id)
    website_url = website.websiteLink

    
    ## Scrap Websites
    r = requests.get(website_url)
    soup = bs(r.content, 'html.parser')
    website_name = soup.find('title').get_text()
    website_link = website_url
    created_At = datetime.datetime.now().date()
    last_Scrapped = datetime.datetime.now().time()

    # Update websites in Data Base
    website.websiteName = website_name
    website.websiteLink = website_link
    website.createdAt = created_At
    website.lastScrappedAt = last_Scrapped

    website.save()
    

    ## Scrap Articles

    articles_dict = {"article_title":[], "article_dom":[], "article_desc":[], "article_link":[]}

    ''' Scrapping Articles Data 
    '''
    
    for item in soup.find_all('article', class_= "item-list"):
        title = item.select_one("h2").get_text()
        articles_dict['article_title'].append(title)
        articles_dict['article_dom'].append(item) 
        
    for x in soup.find_all('div', {"class": "entry"}):
        desc = x.select_one("p").get_text()
        link = x.select_one("a")['href']
        articles_dict['article_desc'].append(desc)
        articles_dict['article_link'].append(link)

    # Fetch all articles attached to the primary key
    # Update Data Base
    index = 0
    article = Article.objects.all()
    for e in article:
        if e.website_ID.id == id:
            e.articleTitle = articles_dict["article_title"][index]
            e.articleDesc  = articles_dict["article_desc"][index]
            e.articleDOM   = str(articles_dict["article_dom"][index])
            e.articleLink  = articles_dict["article_link"][index]
            #print(articles_dict["article_link"][index])
            index = index + 1
            e.save()

    messages.info(request, 'Updating is completed')
    return redirect('websites')