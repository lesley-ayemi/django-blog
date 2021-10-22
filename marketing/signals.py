from django.db.models.signals import post_save
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django_pandas.io import read_frame
from blog.models import Post
from blog.forms import addPostForm
from marketing.models import SignUp

# def create_user(sender, instance, created, **kwargs):
#     if created:
#         def mail_letter(request):
#             emails = SignUp.objects.all()
#             df = read_frame(emails, fieldnames=['email'])
#             mail_list = df['email'].values.tolist()
#             print(mail_list)
#             if request.method == 'POST':
#                 form = addPostForm(request.POST)
#                 if form.is_valid():
#                     form.save()
#                     title = form.cleaned_data.get('title')
#                     message = form.cleaned_data.get('content')
#                     send_mail(
#                         title,
#                         message,
#                         '',
#                         mail_list,
#                         fail_silently=False,
#                         )
#                 # messages.success(request, 'Message has been sent to the Mail List')
#                 # return redirect('mail-letter')
       
# post_save.connect(create_user, sender=Post)