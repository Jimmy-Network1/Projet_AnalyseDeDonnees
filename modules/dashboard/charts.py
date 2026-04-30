import json
import pandas as pd
import plotly
import plotly.express as px
from models.questionnaire import Questionnaire, Reponse
from models.diplome import Diplome
from models.scraping import ScrapingData, ScrapingJob
from models import db

def graphique_taux_reponse():
    questionnaires = Questionnaire.query.all()
    data = []
    for q in questionnaires:
        count = len(q.reponses)
        data.append({'Questionnaire': q.titre, 'Réponses': count})
        
    if not data:
        # Données factices s'il n'y a rien en base
        df = pd.DataFrame([{'Questionnaire': 'Aucun', 'Réponses': 0}])
    else:
        df = pd.DataFrame(data)
        
    fig = px.bar(df, x='Questionnaire', y='Réponses', title='Nombre de réponses par questionnaire', color='Questionnaire')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def graphique_insertion_pro():
    diplomes = Diplome.query.all()
    data = [d.statut_insertion for d in diplomes if d.statut_insertion]
    
    if not data:
        # Données factices
        df = pd.DataFrame([{'Statut': 'En recherche', 'Nombre': 1}])
    else:
        df = pd.DataFrame(data, columns=['Statut'])
        counts = df['Statut'].value_counts().reset_index()
        counts.columns = ['Statut', 'Nombre']
        df = counts
    
    fig = px.pie(df, values='Nombre', names='Statut', title='Insertion professionnelle des diplômés')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def graphique_evolution():
    reponses = Reponse.query.all()
    data = [r.submitted_at.date() for r in reponses if r.submitted_at]
    
    if not data:
        # Données factices
        df = pd.DataFrame([{'Date': pd.Timestamp.now().date(), 'Nombre de réponses': 0}])
    else:
        df = pd.DataFrame(data, columns=['Date'])
        counts = df['Date'].value_counts().reset_index().sort_values('Date')
        counts.columns = ['Date', 'Nombre de réponses']
        df = counts
    
    fig = px.line(df, x='Date', y='Nombre de réponses', title='Évolution des réponses dans le temps', markers=True)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def graphique_offres_emploi():
    offres = ScrapingData.query.join(ScrapingJob).filter(ScrapingJob.source.like('%emploi%')).all()
    
    secteurs = []
    for o in offres:
        titre = o.titre.lower() if o.titre else ""
        if any(kw in titre for kw in ['informatique', 'développeur', 'it', 'logiciel', 'données']):
            secteurs.append('Informatique & IT')
        elif any(kw in titre for kw in ['finance', 'comptable', 'banque', 'audit']):
            secteurs.append('Finance & Comptabilité')
        elif any(kw in titre for kw in ['marketing', 'commercial', 'vente', 'communication']):
            secteurs.append('Marketing & Ventes')
        elif any(kw in titre for kw in ['ingénieur', 'technicien']):
            secteurs.append('Ingénierie')
        elif any(kw in titre for kw in ['rh', 'ressources humaines']):
            secteurs.append('Ressources Humaines')
        else:
            secteurs.append('Autre / Non classé')
            
    if not secteurs:
        # Données factices
        df = pd.DataFrame([{'Secteur': 'Aucun', "Nombre d'offres": 0}])
    else:
        df = pd.DataFrame(secteurs, columns=['Secteur'])
        counts = df['Secteur'].value_counts().reset_index()
        counts.columns = ['Secteur', "Nombre d'offres"]
        df = counts
    
    fig = px.bar(df, x='Secteur', y="Nombre d'offres", title="Offres d'emploi par secteur (estimé)", color='Secteur')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
