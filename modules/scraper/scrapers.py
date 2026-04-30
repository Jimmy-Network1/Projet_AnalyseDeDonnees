import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import db
from models.scraping import ScrapingJob, ScrapingData
import traceback

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def scraper_offres_emploi(app):
    with app.app_context():
        job = ScrapingJob(source='emploi.cm', status='en_cours', started_at=datetime.utcnow())
        db.session.add(job)
        db.session.commit()
        
        try:
            url = "https://www.emploi.cm/recherche-jobs-cameroun"
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            count = 0
            offres = soup.find_all('div', class_='job-description-wrapper')
            if not offres:
                # Fallback if structure is different
                offres = soup.find_all('div', class_='card-job')
                
            for offre in offres[:20]: # Limite arbitraire
                titre_elem = offre.find('h3') or offre.find('h2') or offre.find('a')
                if titre_elem:
                    titre = titre_elem.text.strip()
                    lien_elem = offre.find('a')
                    lien = lien_elem['href'] if lien_elem and lien_elem.has_attr('href') else url
                    if lien.startswith('/'):
                        lien = "https://www.emploi.cm" + lien
                        
                    data = ScrapingData(job_id=job.id, titre=titre, contenu="Offre d'emploi au Cameroun", url=lien)
                    db.session.add(data)
                    count += 1
            
            job.status = 'succès'
            job.finished_at = datetime.utcnow()
            db.session.commit()
            return f"Succès ({count})"
        except Exception as e:
            app.logger.error(f"Erreur scraping emplois: {traceback.format_exc()}")
            job.status = 'erreur'
            job.finished_at = datetime.utcnow()
            db.session.commit()
            return f"Erreur: {str(e)[:50]}"

def scraper_classements(app):
    with app.app_context():
        job = ScrapingJob(source='webometrics.info (Cameroun)', status='en_cours', started_at=datetime.utcnow())
        db.session.add(job)
        db.session.commit()
        
        try:
            url = "https://www.webometrics.info/en/Africa/Cameroon"
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            count = 0
            table = soup.find('table', class_='sticky-enabled')
            if table:
                rows = table.find('tbody').find_all('tr')
                for row in rows[:20]:
                    cols = row.find_all('td')
                    if len(cols) > 1:
                        titre = cols[1].text.strip()
                        lien_elem = cols[1].find('a')
                        lien = lien_elem['href'] if lien_elem and lien_elem.has_attr('href') else url
                        if not lien.startswith('http'):
                            lien = "https://www.webometrics.info" + lien
                            
                        data = ScrapingData(job_id=job.id, titre=titre, contenu=f"Rang mondial: {cols[2].text.strip() if len(cols)>2 else 'N/A'}", url=lien)
                        db.session.add(data)
                        count += 1
            
            job.status = 'succès'
            job.finished_at = datetime.utcnow()
            db.session.commit()
            return f"Succès ({count})"
        except Exception as e:
            app.logger.error(f"Erreur scraping classements: {traceback.format_exc()}")
            job.status = 'erreur'
            job.finished_at = datetime.utcnow()
            db.session.commit()
            return f"Erreur: {str(e)[:50]}"

def scraper_actualites(app):
    with app.app_context():
        job = ScrapingJob(source='journalducameroun.com (Education)', status='en_cours', started_at=datetime.utcnow())
        db.session.add(job)
        db.session.commit()
        
        try:
            url = "https://www.journalducameroun.com/societe/education/"
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            count = 0
            articles = soup.find_all('article')
            for article in articles[:20]:
                titre_elem = article.find('h3') or article.find('h2')
                if titre_elem:
                    titre = titre_elem.text.strip()
                    lien_elem = article.find('a')
                    lien = lien_elem['href'] if lien_elem and lien_elem.has_attr('href') else url
                    
                    data = ScrapingData(job_id=job.id, titre=titre, contenu="Actualité éducative", url=lien)
                    db.session.add(data)
                    count += 1
            
            job.status = 'succès'
            job.finished_at = datetime.utcnow()
            db.session.commit()
            return f"Succès ({count})"
        except Exception as e:
            app.logger.error(f"Erreur scraping actualités: {traceback.format_exc()}")
            job.status = 'erreur'
            job.finished_at = datetime.utcnow()
            db.session.commit()
            return f"Erreur: {str(e)[:50]}"
