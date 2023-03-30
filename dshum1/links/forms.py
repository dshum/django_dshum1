from django import forms

from .models import Link, LinkTag


class CreateLinkForm(forms.ModelForm):
    title = forms.CharField(label='Title', required=True, max_length=255)
    url = forms.URLField(label='URL', required=True)
    tags = forms.ModelMultipleChoiceField(
        queryset=LinkTag.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Link
        fields = ('title', 'url', 'tags')
