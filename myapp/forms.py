

# from django import forms
# from .models import Order, OrderLog
# from urllib.parse import urlparse, parse_qs

# class OrderForm(forms.ModelForm):
#     CANCEL_CHOICES = [
#         ('non-cancel', 'Non-Cancel'),
#         ('cancel', 'Cancel'),
#     ]

#     cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())

#     class Meta:
#         model = Order
#         exclude = ['user', 'timing', 'date']
#         widgets = {
#             'id_name': forms.TextInput(attrs={'placeholder': 'Enter ID Name'}),
#             'order_id': forms.TextInput(attrs={'placeholder': 'Enter Order ID or URL'}),
#             'amount': forms.TextInput(attrs={'placeholder': 'Enter the amount'}),
#             'address_code': forms.TextInput(attrs={'placeholder': 'Enter Address Code'}),
#             'refresh_link': forms.TextInput(attrs={'placeholder': 'Enter Refresh Link'}),
#         }

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['cancel_status'].empty_label = None
#         field_order = ['id_name', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
#         self.order_fields(field_order)

#     def clean_order_id(self):
#         order_id = self.cleaned_data['order_id']
#         if order_id.startswith('http'):
#             parsed_url = urlparse(order_id)
#             query_params = parse_qs(parsed_url.query)
#             if 'orderid' in query_params:
#                 return query_params['orderid'][0]
#         return order_id



#     def save(self, commit=True):
#         instance = super(OrderForm, self).save(commit=False)
#         if self.user:
#             instance.user = self.user
#         if commit:
#             instance.save()
#             OrderLog.objects.create(user=self.user, order=instance, action="created")
#         return instance





from django import forms
from .models import Order, OrderLog
from urllib.parse import urlparse, parse_qs

class OrderForm(forms.ModelForm):
    CANCEL_CHOICES = [
        ('non-cancel', 'Non-Cancel'),
        ('cancel', 'Cancel'),
    ]

    CLONE_CHOICES = [
        ('non-clone', 'Non-Clone'),
        ('clone', 'Clone'),
    ]

    cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())
    clone_option = forms.ChoiceField(choices=CLONE_CHOICES, widget=forms.Select(), required=False)

    class Meta:
        model = Order
        exclude = ['user', 'timing', 'date']
        widgets = {
            'id_name': forms.TextInput(attrs={'placeholder': 'Enter ID Name'}),
            'order_id': forms.TextInput(attrs={'placeholder': 'Enter Order ID or URL'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Enter the amount'}),
            'address_code': forms.TextInput(attrs={'placeholder': 'Enter Address Code'}),
            'refresh_link': forms.TextInput(attrs={'placeholder': 'Enter Refresh Link'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['cancel_status'].empty_label = None
        self.fields['clone_option'].empty_label = None
        field_order = ['clone_option', 'id_name', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
        self.order_fields(field_order)

    # ... (rest of the form code remains the same)


    def clean_order_id(self):
        order_id = self.cleaned_data['order_id']
        if order_id.startswith('http'):
            parsed_url = urlparse(order_id)
            query_params = parse_qs(parsed_url.query)
            if 'orderid' in query_params:
                return query_params['orderid'][0]
        return order_id



    def save(self, commit=True):
        instance = super(OrderForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
            OrderLog.objects.create(user=self.user, order=instance, action="created")
        return instance
