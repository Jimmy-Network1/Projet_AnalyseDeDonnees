import io
import pandas as pd
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from models.questionnaire import Questionnaire, Reponse

def get_reponses_dataframe(questionnaire_id):
    """Prépare un DataFrame pandas avec les réponses d'un questionnaire."""
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        return None, None
        
    reponses = Reponse.query.filter_by(questionnaire_id=questionnaire_id).all()
    questions = questionnaire.questions
    
    data = []
    for r in reponses:
        row = {
            'ID Réponse': r.id,
            'Date Soumission': r.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Utilisateur (Email)': r.user.email if r.user else 'Anonyme'
        }
        for q in questions:
            detail = next((d for d in r.details if d.question_id == q.id), None)
            row[q.texte] = detail.valeur if detail else ''
        data.append(row)
        
    return pd.DataFrame(data), questionnaire.titre

def generer_csv(questionnaire_id):
    """Génère un fichier CSV en mémoire."""
    df, titre = get_reponses_dataframe(questionnaire_id)
    if df is None:
        return None, None
        
    output = io.StringIO()
    df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
    
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8-sig'))
    mem.seek(0)
    return mem, f"{titre}_reponses.csv"

def generer_excel(questionnaire_id):
    """Génère un fichier Excel en mémoire avec en-têtes colorés."""
    df, titre = get_reponses_dataframe(questionnaire_id)
    if df is None:
        return None, None
        
    output = io.BytesIO()
    
    # Utilisation du moteur openpyxl
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Réponses', index=False)
        worksheet = writer.sheets['Réponses']
        
        # Style d'en-tête (Gras + Fond bleu)
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="0070C0", end_color="0070C0", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            
        # Ajustement sommaire de la largeur des colonnes
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = min(adjusted_width, 50) # Limit max width
            
    output.seek(0)
    return output, f"{titre}_reponses.xlsx"

def generer_pdf(questionnaire_id):
    """Génère un rapport PDF des réponses en mémoire."""
    df, titre = get_reponses_dataframe(questionnaire_id)
    if df is None:
        return None, None
        
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Titre du PDF
    elements.append(Paragraph(f"Rapport des réponses : {titre}", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Statistiques
    elements.append(Paragraph(f"Total des réponses : {len(df)}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Tableau des données (limité en colonnes pour le PDF)
    if not df.empty:
        # Prendre seulement les 5 premières colonnes pour que ça rentre sur la page
        display_columns = df.columns[:5].tolist()
        data = [display_columns] # En-tête
        
        for index, row in df.iterrows():
            # Truncate text if it's too long
            row_data = [str(row[col])[:30] + '...' if len(str(row[col])) > 30 else str(row[col]) for col in display_columns]
            data.append(row_data)
            
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0070C0')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTSIZE', (0,1), (-1,-1), 8),
        ]))
        elements.append(t)
        
        if len(df.columns) > 5:
             elements.append(Spacer(1, 10))
             elements.append(Paragraph(f"<i>Note : Seules les 5 premières colonnes sont affichées dans ce PDF sur les {len(df.columns)} colonnes totales. Utilisez l'export Excel pour la vue complète.</i>", styles['Italic']))
    else:
        elements.append(Paragraph("Aucune réponse pour ce questionnaire.", styles['Italic']))

    doc.build(elements)
    output.seek(0)
    return output, f"{titre}_rapport.pdf"
