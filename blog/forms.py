from django import forms
# from tinymce import TinyMCE
# from froala_editor.widgets import FroalaEditor
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.forms import fields, widgets
from .models import Account, Category, Comment, Post, Profile

class addPostForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'slug', 'post_views']


class CommentForm(forms.ModelForm):

    class Meta:
        # class CheckboxInput(forms.CheckboxInput):
        #     def __init__(self, default=False, *args, **kwargs):
        #         super(CheckboxInput, self).__init__(*args, **kwargs)
        #         self.default = default

        # def value_from_datadict(self, data, files, name):
        #     if name not in data:
        #         return self.default
        #     return super(CheckboxInput, self).value_from_datadict(data, files, name)

        model = Comment
        fields = ['name', 'email', 'content', 'active']
        def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)

            self.fields['active'].widget.attrs['checked'] = True
        # active = forms.BooleanField(widget=CheckboxInput(default=True), required=False)
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
        
class RegisterForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email']
#     password = forms.CharField(
#     widget=forms.TextInput(attrs={'readonly':'readonly'})
# )

class ContactForm(forms.Form):
    # name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=200)
    email_address = forms.EmailField(max_length=200)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)