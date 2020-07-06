from django.db.models import Count, Q
from django.shortcuts import render,get_object_or_404,redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post,Category,About,Comment
from .forms import CommentForm
from marketing.models import Signup
from django.views.generic import ListView
from hitcount.views import HitCountDetailView
from django.views.generic import  DetailView
# Create your views here.
class About(ListView):
    template_name ='about.html'
    model = About
def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
        'query':query
    }
    return render(request, 'search_results.html', context)

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    popular_posts = Post.objects.order_by('-hit_count__hits')[:3]
    categories = Category.objects.filter()
    category_count = get_category_count()
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list':featured,
        'latest':latest,
        'popular_posts':popular_posts,
        'categories':categories,
        'category_count':category_count
    }
    return render(request, 'index.html',context)

# def blog(request):
#     return render(request, 'blog.html',{})    
def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset
 
def post_list(request):
    categories = Category.objects.all()
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:8]
    post_list = Post.objects.order_by('-timestamp')
    paginator = Paginator(post_list, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'categories': categories,
        'category_count': category_count, 
        # 'form': form
    }
    return render(request, 'blog.html', context)
  

def Posts_in_CategoryView(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_in_cat = category.post_set.all()

    # pagination
    paginator = Paginator(posts_in_cat, 8) # Show 8 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
            'posts_in_cat':posts_in_cat,
            'cat_name': category,
            'page_obj': page_obj,
    }
   
   
    
    return render(request, 'posts_in_category.html', context)
    
   
      

    # return render(request, 'blog/posts_in_category.html', context)
class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
    count_hit = True
    # post = self.get_object()
    # comments = post.comments.filter(active=True)
    form=CommentForm()
    new_comment = None
    
 
    def get_context_data(self, **kwargs):
        # post = get_object_or_404(Post, slug=slug)
        categories = Category.objects.filter()
        category_count = get_category_count()
        this_post = Post.objects.filter(id=self.object.id)
        most_recent = Post.objects.order_by('-timestamp')[:5]
        popular_posts = Post.objects.order_by('-hit_count__hits')[:3]
        tags = [tag.strip() for tag in this_post[0].tags.split(',')]
        post = self.get_object()
        comments = post.comments.filter(active=True)
        
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = popular_posts
        context['most_recent'] = most_recent
        context["tags"] = tags
        # context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['categories']= categories
        
        context['form'] = self.form
        context['new_comment'] = self.new_comment
        context['comments'] = comments
    
        return context


    def post(self, request, *args, **kwargs):
       
        post = self.get_object()
        if request.method == 'POST':
        # A comment was posted
           form = CommentForm(data=request.POST)
           if form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # Save the comment to the database
                new_comment.save()
                return redirect(reverse("post-detail", kwargs={
                    'slug': post.slug
            }))
        else:
            form = CommentForm()
    



def post_detail(request, slug):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:8]
    post = get_object_or_404(Post, slug=slug)
    # count_hit = True

    comments = post.comments.filter(active=True)
    category_count = get_category_count()

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        # 'form': form,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'category_count':category_count
    }
    return render(request, 'post_detail.html', context)
    count_hit = True