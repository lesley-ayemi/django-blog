from django.contrib.auth.views import PasswordChangeView
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from blog.forms import CommentForm, ProfileForm, RegisterForm, UserUpdateForm, addPostForm
from blog.models import Category, Comment, Post, Tag
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from marketing.models import SignUp
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages 
from aboutme.models import Biography
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin

class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    # """Authentications"""
def register(request):
    # form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Successfully Created')
            return redirect('login')
    else:
        form = RegisterForm()
        context = {
            'form':form,
        }
    return render(request, 'auth/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # changed the login default name
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')

    return render(request, 'auth/login.html')
    """END"""


    """Home & Details Page"""
def home(request):
    # //* Newsletter 
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()
        messages.success(request, 'You have successfully subscribed to the newsletter')
        return redirect('home')
    else:
        posts = Post.objects.all()
        featured = Post.objects.filter(featured=True)[0:4]
        lastest = Post.objects.order_by('-published_at')[0:3]
        categories = Category.objects.all()
        about = Biography.objects.get()
        comment = Comment.objects.filter(active=True)
        # Pagination
        paginator = Paginator(posts, 5)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            paginated_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)
        
        context = {
            'posts':paginated_queryset,
            'featured':featured,
            'lastest':lastest,
            'page':page,
            'page_request_var':page_request_var,
            'categories':categories,
            'about':about,
            'comment':comment,
        }

    return render(request, 'blog/main.html', context)

def all_articles(request):

    posts = Post.objects.all().filter(status='published')
    lastest = Post.objects.order_by('-published_at')[0:3]
    categories = Category.objects.all()
    about = Biography.objects.get()
    # Pagination
    paginator = Paginator(posts, 12)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {'posts':paginated_queryset, 'lastest':lastest, 'categories':categories, 'about':about, 'page':page,
            'page_request_var':page_request_var,}
    return render(request, 'blog/all_posts.html', context)


def search_article(request):
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            posts = Post.objects.order_by('-published_at').filter(Q(title__icontains=search)|Q(content__icontains=search))
            posts_count = posts.count()
            lastest = Post.objects.order_by('-published_at')[0:3]
            categories = Category.objects.all()
            about = Biography.objects.get()
            # print(posts)
    context = {
        'posts':posts,
        'posts_count':posts_count,
        'lastest':lastest,
        'categories':categories,
        'about':about,
    }
    return render(request, 'blog/search_result.html', context)

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    categories = Category.objects.all()
    about = Biography.objects.get()
    comments = Comment.objects.filter(post=post)
    tags = Tag.objects.all()
    comment_form = CommentForm()
    new_comment = None
    # posted comment 
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
    context = {
        'post':post,
        'tags':tags,
        'categories':categories,
        'about':about,
        'comments':comments,
        'comment_form':comment_form,
        # 'profile':profile,
    }
    return render(request, 'blog/post_detail.html', context)
    """END"""

    """Users Controllers"""
@login_required(login_url='login')
def dashboard(request):
    post = Post.objects.filter(author=request.user)
    latest = Post.objects.filter(author=request.user)[:3]
    published = post.filter(status='published')
    draft = post.filter(status='draft')
    # post_obj = Post.objects.filter('-published_at')[0:5]
    context = {
        'post':post,
        'published':published,
        'draft':draft,
        'latest':latest,
        # 'post_obj':post_obj,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='login')
def show_post(request):
    user_post = Post.objects.filter(author=request.user).order_by('-updated_at')
    context = {
        'user_post':user_post,
        # 'posts':posts,
    }
    return render(request, 'dashboard/posts/index.html', context)

@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST' and request.FILES['blog_image']:
        form = addPostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # TODO: Integerate django toggit later
            #importabt for tags
            form.save_m2m()
            messages.info(request, 'Successfully added article')
            return redirect('show-post')
    else:
        context = {}
        context['form']= addPostForm()
    return render(request, 'dashboard/posts/add_post.html', context)

@login_required(login_url='login')
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return redirect('show-post')
    form = addPostForm(
        request.POST or None,
        request.FILES or None,
        instance=post
    )
    if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated post')
            return redirect('show-post')
    context = {
        'form':form
    }
    return render(request, 'dashboard/posts/update_post.html', context)

@login_required(login_url='login')
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)

    if post.author == request.user:
        post.delete()
        messages.success(request, 'Article successfully deleted')
        return redirect('show-post')
    else:
        return redirect('show-post')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
        context = {
            'u_form':u_form,
            'p_form':p_form,
        }
    # profile = get_object_or_404(Profile, user=request.user)
    # form = ProfileForm(
    #     request.POST or None,
    #     request.FILES or None,
    #     instance=profile
    # )
    # if form.is_valid():
    #     form.save()
    #     messages.success(request, 'Profile sucessfully updated')
    #     return redirect('profile')
    # context = {'form':form, 'profile':profile}
    return render(request, 'dashboard/profile/index.html', context)

class PasswordsChangeView(SuccessMessageMixin, PasswordChangeView):
    from_class = PasswordChangeForm
    success_url = reverse_lazy('password')
    success_message = "Password Updated"


def logout(request):
    auth_logout(request)
    return redirect('home')