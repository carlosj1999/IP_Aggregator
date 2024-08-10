# aggregator/forms.py

from django import forms

class IPAggregatorForm(forms.Form):
    ip_addresses = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}))
    output_format = forms.ChoiceField(choices=[
        ('cidr', 'CIDR'),
        ('mask', 'Mask'),
        ('range', 'Range'),
        ('b-n', 'B-N'),
        ('hta', 'HTA'),
        ('zbb', 'ZBB'),
    ])
    why_blocked = forms.CharField(required=False)
    asn_code = forms.CharField(required=False)