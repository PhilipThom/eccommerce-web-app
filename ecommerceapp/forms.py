from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES=(
    ('S','Stripe'),
    # ('P','PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address=forms.CharField(required=False)
    shipping_address2=forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,

        widget=CountrySelectWidget(
         attrs={
            'class': 'custom-select d-block w-100'
        }

    )
       

    )
    
    shipping_zip=forms.CharField(required=False)
    

    billing_address=forms.CharField(required=False)
    billing_address2=forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,

        widget=CountrySelectWidget(
         attrs={
            'class': 'custom-select d-block w-100'
        }

    )
       

    )
    billing_zip=forms.CharField(required=False)
    same_billing_address=forms.BooleanField(required=False)
    #save_info=forms.BooleanField(required=False)
    set_default_shipping=forms.BooleanField(required=False)
    use_default_shipping=forms.BooleanField(required=False)
    set_default_billing=forms.BooleanField(required=False)
    use_default_billing=forms.BooleanField(required=False)



    payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)

#request refund form
class RefundForm(forms.Form):
    ref_code=forms.CharField(widget=forms.TextInput(attrs={
        
        'placeholder':'Order reference code'
        # rows:3


    }))

    
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        
        'placeholder':'Your Email-address'
        # rows:3


    }))
    message=forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder':'Write your complain'
        # rows:3


    }))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)    