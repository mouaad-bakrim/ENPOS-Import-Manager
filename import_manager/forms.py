from django import forms

class ExcelUploadForm(forms.Form):
    fichier = forms.FileField(
        label="Fichier Excel",
        widget=forms.FileInput(attrs={
            "accept": ".xlsx",
            "class": "form-control"
        })
    )

    def clean_fichier(self):
        fichier = self.cleaned_data["fichier"]

        if not fichier.name.lower().endswith(".xlsx"):
            raise forms.ValidationError("Format accepté : .xlsx uniquement")

        if fichier.size > 15 * 1024 * 1024:
            raise forms.ValidationError("Le fichier ne doit pas dépasser 15 MB.")

        return fichier
