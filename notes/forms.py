from django import forms


class EventForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker1'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker2'}))
