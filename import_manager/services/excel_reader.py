from openpyxl import load_workbook

EXPECTED_SHEETS = {
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


def inspect_excel(file_path):
    wb = load_workbook(file_path, read_only=True, data_only=True)

    result = {
        "sheets": [],
        "errors": [],
        "counts": {},
        "preview": {},
    }

    for sheet_name, required_columns in EXPECTED_SHEETS.items():
        if sheet_name not in wb.sheetnames:
            result["errors"].append(
                f"Feuille manquante : {sheet_name}"
            )
            continue

        ws = wb[sheet_name]
        rows = ws.iter_rows(values_only=True)

        headers = next(rows, None)

        if not headers:
            result["errors"].append(
                f"La feuille {sheet_name} est vide."
            )
            continue

        headers = [
            str(value).strip() if value is not None else ""
            for value in headers
        ]

        missing = [
            col for col in required_columns
            if col not in headers
        ]

        if missing:
            result["errors"].append(
                f"{sheet_name} : colonnes manquantes : "
                + ", ".join(missing)
            )
            continue

        data_rows = [
            row for row in rows
            if any(value is not None for value in row)
        ]

        result["sheets"].append(sheet_name)
        result["counts"][sheet_name] = len(data_rows)
        result["preview"][sheet_name] = data_rows[:5]

    wb.close()
    return result
