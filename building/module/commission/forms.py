from django import forms

class PutForm(forms.Form):
    price = forms.FloatField(label='Price')
    
    def clean_price(self):
        price = self.cleaned_data['price']

        if price > 0:
            return price
#
        raise forms.ValidationError('Price must be positive')
        
        