from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ExcelUploadForm
from .services.excel_reader import inspect_excel


def dashboard(request):
    context = {"form": ExcelUploadForm()}

    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            fichier = form.cleaned_data["fichier"]

            upload_dir = Path(settings.MEDIA_ROOT) / "imports"
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_path = upload_dir / f"{uuid4().hex}.xlsx"

            with open(file_path, "wb+") as destination:
                for chunk in fichier.chunks():
                    destination.write(chunk)

            try:
                result = inspect_excel(file_path)
                context.update({
                    "form": form,
                    "result": result,
                    "filename": fichier.name,
                })
            except Exception as exc:
                context["error"] = f"Erreur de lecture Excel : {exc}"

        else:
            context["form"] = form

    return render(request, "import_manager/dashboard.html", context)


def download_template(request):
    from django.http import HttpResponse
    from .services.excel_template import create_template

    wb = create_template()

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="ENPOS_Tournee_Template.xlsx"'
    )

    wb.save(response)
    return response
