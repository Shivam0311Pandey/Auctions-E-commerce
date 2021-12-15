from django import forms

from .models import Auction, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'image', 'starting_bid', 'category')
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'formInput'}),
            'description' : forms.Textarea(attrs={'class' : 'formInput', 'cols': 80, 'rows': 4}),
            'starting_bid' : forms.NumberInput(attrs={'class' : 'formInput'}),
            'category' : forms.Select(choices=Category.objects.all(), attrs={'class' : 'formInput'})
        }