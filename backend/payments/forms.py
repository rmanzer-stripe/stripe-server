from django import forms


class EvidenceForm(forms.Form):
    dispute_id = forms.CharField()
    uncategorized_text = forms.CharField()
