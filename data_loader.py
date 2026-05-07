import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

class DataLoader:
    def __init__(self, host, user, password, index_id):
        self.es = Elasticsearch(host, basic_auth=(user, password))
        self.index_id = index_id
        self.core_cols = ["ticket", "tache_objet", "statut_tache", "priorite", "date_debut", "date_finprevue", "date_fin", "proces_label", "proces_statut", "site_nom", "site_statut", "zone", "region", "departement", "projet_nom", "annee", "porteur", "equipe", "domaine", "utilisateur", "statut_global"]

    def fetch_and_process(self):
        results = scan(self.es, index=self.index_id, query={"query": {"match_all": {}}})
        df = pd.DataFrame([doc['_source'] for doc in results])
        if df.empty:
            return []
        df = df.drop_duplicates("ticket")

        # Nettoyage et Stats (votre logique actuelle)
        clean_cols = ["tache_objet", "proces_label", "site_nom", "zone", "region", 
                      "departement", "projet_nom", "porteur", "utilisateur", "annee", "priorite"]
        
        for col in clean_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower().str.strip()

        stats_mapping = {'zone': 'total_tasks_zone','projet_nom': 'total_tasks_projet','region': 'total_tasks_region','departement': 'total_tasks_departement','porteur': 'total_tasks_porteur','utilisateur': 'total_tasks_utilisateur','domaine': 'total_tasks_domaine','proces_label': 'total_tasks_process_label','annee': 'total_tasks_annee','statut_tache': 'total_tasks_statut_tache','priorite': 'total_tasks_priorite'}
        for col_orig, col_dest in stats_mapping.items():
            if col_orig in df.columns:
                df[col_dest] = df.groupby(col_orig)['ticket'].transform('count')
        
        # Construction du texte source
        df["document_text"] = df.apply(self._build_full_source_text, axis=1)
        return df["document_text"].tolist()

    
    def _build_full_source_text(self, row):
        stat_parts = [ f"Statistiques globales :",
            f"- Pour le projet '{row.get('projet_nom')}', il y a {row.get('total_tasks_projet', 0)} tâches.",
            f"- Dans la zone {row.get('zone')}, on compte {row.get('total_tasks_zone', 0)} tâches.",
            f"- L'utilisateur {row.get('utilisateur')} gère {row.get('total_tasks_utilisateur', 0)} tâches au total.",
            f"- Le statut '{row.get('statut_tache')}' concerne {row.get('total_tasks_statut_tache', 0)} tickets.",
            f"- Le domaine '{row.get('domaine')}' regroupe {row.get('total_tasks_domaine', 0)} tâches.",
            f"- La région {row.get('region')} compte {row.get('total_tasks_region', 0)} tâches.",
            f"- Le département {row.get('departement')} a {row.get('total_tasks_departement', 0)} tâches.",
            f"- Le porteur {row.get('porteur')} est responsable de {row.get('total_tasks_porteur', 0)} tâches."
            f"- L'année {row.get('annee')} a vu la création de {row.get('total_tasks_annee', 0)} tâches.",
            f"- Le processus '{row.get('proces_label')}' inclut {row.get('total_tasks_process_label', 0)} tâches.",
            f"- La priorité '{row.get('priorite')}' concerne {row.get('total_tasks_priorite', 0)} tâches."]
        stat_context = "\n".join(stat_parts)
        detail_parts = [f"Détails du ticket n°{row['ticket']} :"]
        for col in self.core_cols:
            if col in ["ticket", "projet_nom", "zone"]:
                continue
            
            value = row.get(col, None)
            if pd.notnull(value) and str(value).lower() not in ["none", "nan", "null"]:
                detail_parts.append(f"Le champ {col} est '{value}'")
        detail_parts_str = "\n".join(detail_parts)
        return f"[STATS]: {stat_context}\n[DETAILS]: {detail_parts_str}"