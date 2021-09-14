from django import forms
# from tinymce import TinyMCE
from froala_editor.widgets import FroalaEditor
from django.forms import fields, widgets
from .models import Account, Category, Comment, Post, Profile

class addPostForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'slug', 'comment_count', 'comments']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content', 'active']

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