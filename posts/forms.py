from django import forms

from posts.models import Offer, Post
from users.models import User
from . import models

class ItemForm(forms.ModelForm):
    FORM_TITLE = 'Item Description'
    CHOICE = ((0, 'Office Use'), (1, 'Academic Use'), (2, 'Other Uses'))

    use = forms.ChoiceField(choices=CHOICE, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), initial=1)

    help = {
        'name': 'Required',
        'quantity': 'Required. Must be a positive number.',
        'price': 'Required. Must be a positive number.',
        'use': 'Required. Choose how the item will be used.',
        'course': 'Type the course code if the item is for academic use only.'
    }
    class Meta:

        model = models.Item
        fields = ['name', 'quantity', 'price', 'use', 'course', 'picture']

        labels = {
            'name': 'Item Name',
            'quantity': 'Item Quantity',
            'price': 'Item Price',
            'course': 'Item Course',
            'picture': 'Item Picture',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name...'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': 0}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': 0}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name...'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

class PostForm(forms.ModelForm):
    FORM_TITLE = 'Post Description'
    help = {
        'description': 'Required.',
        'tags': 'Required. Tags are separated by blank spaces.'
    }

    class Meta:
        model=models.Post
        fields = ['description', 'tags']

        labels = {
            'description': 'Item Description',
            'tags': 'Post Tags'
        }

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(Second Hand, Barely Used...)'}),
            'tags': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'books science math...'})
        }

class OfferForm(forms.ModelForm):
    FORM_TITLE = 'Offer/Trade'

    class Meta:
        model = Offer

        fields = ['post', 'offerPost', 'offerCash', 'message']

        labels = {
            'offerCash': 'Cash To Offer (in Php.)',
        }

        widgets = {
            'offerCash': forms.NumberInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Message Here...', 'style':'resize: none'}),
        }
    def __init__(self, sender, receiver, hidden=None, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)

        s = sender
        r = receiver

        self.fields['post'] = forms.ModelChoiceField(queryset=Post.objects.filter(user=r), label='Item To Buy', required=True,
                                                     widget= forms.Select(attrs={'class': 'form-control'}))
        self.fields['post'].label_from_instance = lambda obj: "%s" % obj.item.name

        self.fields['offerPost'] = forms.ModelChoiceField(queryset=Post.objects.filter(user=s), label='Item To Offer', required=False,
                                                          widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['offerPost'].label_from_instance = lambda obj: "%s" % obj.item.name

        if hidden == 'receiver':
            del self.fields['post']
