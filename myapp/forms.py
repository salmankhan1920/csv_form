# from django import forms
# from .models import Order

# class OrderForm(forms.ModelForm):
#     CANCEL_CHOICES = [
#         ('non-cancel', 'Non-Cancel'),
#         ('cancel', 'Cancel'),
#     ]

#     cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())

#     class Meta:
#         model = Order
#         fields = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'cancel_status']
#         widgets = {
#             'timing': forms.TimeInput(attrs={'readonly': True}),
#             'date': forms.DateInput(attrs={'readonly': True}),
#         }


# from django import forms
# from .models import Order

# class OrderForm(forms.ModelForm):
#     CANCEL_CHOICES = [
#         ('non-cancel', 'Non-Cancel'),
#         ('cancel', 'Cancel'),
#     ]

#     cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())

#     class Meta:
#         model = Order
#         fields = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'cancel_status']
#         widgets = {
#             'id_name': forms.TextInput(attrs={'placeholder': 'Enter ID Name'}),
#             'timing': forms.TimeInput(attrs={'readonly': True}),
#             'date': forms.DateInput(attrs={'readonly': True}),
#             'order_id': forms.TextInput(attrs={'placeholder': 'Enter Order ID'}),
#             'amount': forms.NumberInput(attrs={'placeholder': 'Enter 3 or 4 digits'}),
#             'address_code': forms.TextInput(attrs={'placeholder': 'Enter Address Code'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['cancel_status'].empty_label = None  # Removes the empty "-----" option


# from django import forms
# from .models import Order

# class OrderForm(forms.ModelForm):
#     CANCEL_CHOICES = [
#         ('non-cancel', 'Non-Cancel'),
#         ('cancel', 'Cancel'),
#     ]

#     cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())

#     class Meta:
#         model = Order
#         fields = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
#         widgets = {
#             'id_name': forms.TextInput(attrs={'placeholder': 'Enter ID Name'}),
#             'timing': forms.TimeInput(attrs={'readonly': True}),
#             'date': forms.DateInput(attrs={'readonly': True}),
#             'order_id': forms.TextInput(attrs={'placeholder': 'Enter Order ID'}),
#             'amount': forms.NumberInput(attrs={'placeholder': 'Enter 3 or 4 digits'}),
#             'address_code': forms.TextInput(attrs={'placeholder': 'Enter Address Code'}),
#             'refresh_link': forms.TextInput(attrs={'placeholder': 'Enter Refresh Link'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['cancel_status'].empty_label = None  # Removes the empty "-----" option
        
#         # Reorder the fields to place refresh_link after address_code
#         field_order = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
#         self.order_fields(field_order)


# from django import forms
# from .models import Order
# from urllib.parse import urlparse, parse_qs

# class OrderForm(forms.ModelForm):
#     CANCEL_CHOICES = [
#         ('non-cancel', 'Non-Cancel'),
#         ('cancel', 'Cancel'),
#     ]

#     cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())

#     class Meta:
#         model = Order
#         fields = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
#         widgets = {
#             'id_name': forms.TextInput(attrs={'placeholder': 'Enter ID Name'}),
#             'timing': forms.TimeInput(attrs={'readonly': True}),
#             'date': forms.DateInput(attrs={'readonly': True}),
#             'order_id': forms.TextInput(attrs={'placeholder': 'Enter Order ID or URL'}),
#             'amount': forms.NumberInput(attrs={'placeholder': 'Enter 3 or 4 digits'}),
#             'address_code': forms.TextInput(attrs={'placeholder': 'Enter Address Code'}),
#             'refresh_link': forms.TextInput(attrs={'placeholder': 'Enter Refresh Link'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['cancel_status'].empty_label = None
#         field_order = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
#         self.order_fields(field_order)

#     def clean_order_id(self):
#         order_id = self.cleaned_data['order_id']
#         if order_id.startswith('http'):
#             parsed_url = urlparse(order_id)
#             query_params = parse_qs(parsed_url.query)
#             if 'orderid' in query_params:
#                 return query_params['orderid'][0]
#         return order_id



from django import forms
from .models import Order
from urllib.parse import urlparse, parse_qs

class OrderForm(forms.ModelForm):
    CANCEL_CHOICES = [
        ('non-cancel', 'Non-Cancel'),
        ('cancel', 'Cancel'),
    ]

    cancel_status = forms.ChoiceField(choices=CANCEL_CHOICES, widget=forms.Select())

    class Meta:
        model = Order
        fields = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
        widgets = {
            'id_name': forms.TextInput(attrs={'placeholder': 'Enter ID Name'}),
            'timing': forms.TimeInput(attrs={'readonly': True}),
            'date': forms.DateInput(attrs={'readonly': True}),
            'order_id': forms.TextInput(attrs={'placeholder': 'Enter Order ID or URL'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Enter 3 or 4 digits'}),  # Changed to TextInput
            'address_code': forms.TextInput(attrs={'placeholder': 'Enter Address Code'}),
            'refresh_link': forms.TextInput(attrs={'placeholder': 'Enter Refresh Link'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['cancel_status'].empty_label = None
        field_order = ['id_name', 'timing', 'date', 'order_id', 'amount', 'address_code', 'refresh_link', 'cancel_status']
        self.order_fields(field_order)

    def clean_order_id(self):
        order_id = self.cleaned_data['order_id']
        if order_id.startswith('http'):
            parsed_url = urlparse(order_id)
            query_params = parse_qs(parsed_url.query)
            if 'orderid' in query_params:
                return query_params['orderid'][0]
        return order_id

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount:
            try:
                amount = int(amount)
                if len(str(amount)) not in [3, 4]:
                    raise forms.ValidationError("Amount must be 3 or 4 digits.")
            except ValueError:
                raise forms.ValidationError("Please enter a valid number.")
        return amount
