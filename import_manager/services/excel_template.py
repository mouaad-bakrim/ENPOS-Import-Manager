from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HEADERS = {
    "TOURNEE": [
        "Date", "Code_Vendeur", "Code_Secteur",
        "Nb_Clients", "Montant_TTC", "Remise_TTC", "Montant_DT"
    ],
    "VISITES_VENTES": [
        "Ref_Vente", "Code_Client", "Date_Visite", "Etat",
        "Selection_Type", "Montant", "Montant_HT", "Montant_TVA",
        "Montant_Poids", "Remise_TTC", "Montant_DT", "Paye_Esp"
    ],
    "LIGNES_VENTES": [
        "Ref_Vente", "Code_Produit", "Quantite", "Prix_Unitaire",
        "Subtotal_HT", "Subtotal_TTC", "Subtotal_TVA",
        "Subtotal_Poids", "Subtotal_Remise"
    ],
    "PAIEMENTS": [
        "Date", "Code_Mode_Paiement", "Montant",
        "Etat", "Selection_Type", "Code_Client",
        "Reference", "Titulaire", "Echeance"
    ],
}


def create_template():
    wb = Workbook()
    wb.remove(wb.active)

    for sheet_name, headers in HEADERS.items():
        ws = wb.create_sheet(sheet_name)
        ws.append(headers)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                start_color="183153",
                end_color="183153",
                fill_type="solid"
            )
            cell.alignment = Alignment(horizontal="center")

        for index, header in enumerate(headers, start=1):
            ws.column_dimensions[get_column_letter(index)].width = max(
                len(header) + 5, 18
            )

    return wb
