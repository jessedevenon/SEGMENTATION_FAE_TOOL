"""
FAE Analyzer - Version 7.2 FINAL
- Lecture automatique feuille "Données" (ignore "Instructions")
- Gestion automatique virgules/points dans CA
- Diagnostic d'import détaillé
- Colonnes dirigeant optionnelles
- SECTEUR : texte libre
"""

from __future__ import annotations

import pandas as pd
from typing import Dict
from datetime import datetime


REQUIRED_COLUMNS = [
    "NOM",
    "SECTEUR",
    "CA_HONORAIRES_HT",
    "OUTIL_COMPATIBLE_REFORME",
    "APPETENCE_INFORMATIQUE",
]

OPTIONAL_CONTACT_COLUMNS = [
    "DIRIGEANT_PRENOM",
    "DIRIGEANT_NOM",
    "DIRIGEANT_EMAIL",
]

SECTEURS_VALIDES = [
    "Autres",
    "Commerce de détail",
    "Hôtellerie",
    "Réparation de véhicules",
    "Activités juridiques et comptables",
    "Immobilier",
    "Industrie et fabrication",
    "Activités financières",
    "Autres services aux personnes",
    "Santé",
    "Travaux de construction",
    "Agriculture",
    "Architecture et ingénierie",
    "Enseignement",
    "Construction de bâtiments",
    "Transport",
    "Sports et loisirs",
    "Activités informatiques",
    "Services de conseil aux entreprises",
    "Industrie agroalimentaire",
    "Production audiovisuelle",
    "Édition",
    "Maintenance",
]


class FAEAnalyzer:
    def __init__(self, coefficients: Dict, tarifs: Dict):
        self.coef = coefficients
        self.tarifs = tarifs

    @staticmethod
    def _norm_text(x) -> str:
        if pd.isna(x):
            return ""
        return str(x).strip()

    @staticmethod
    def _norm_upper(x) -> str:
        return FAEAnalyzer._norm_text(x).upper()

    @staticmethod
    def _safe_float(x, default=0.0) -> float:
        try:
            val = float(x)
            if pd.isna(val):
                return default
            return val
        except Exception:
            return default

    @staticmethod
    def _compute_segment_from_ca(ca: float) -> str:
        if ca == 0:
            return "Pas d'honoraires"
        if ca < 1000:
            return "-1000€ HT"
        if ca < 2500:
            return "1000€–2500€ HT"
        if ca < 5000:
            return "2500€–5000€ HT"
        if ca <= 10000:
            return "5000€–10000€ HT"
        return ">10000€ HT"

    def load_data(self, file) -> pd.DataFrame:
        # Lecture de la feuille "Données" : ligne 1 = message d'intro, ligne 2 = en-têtes (NOM, SECTEUR, ...)
        try:
            df = pd.read_excel(file, sheet_name="Données", header=1)
            print(f"\n✅ Feuille 'Données' trouvée et chargée (en-têtes à la ligne 2)")
        except Exception:
            print(f"\n⚠️ Pas de feuille 'Données' trouvée, lecture de la première feuille (header=1)")
            df = pd.read_excel(file, sheet_name=0, header=1)
        
        print(f"\n" + "="*60)
        print(f"📊 DIAGNOSTIC IMPORT - {datetime.now().strftime('%H:%M:%S')}")
        print(f"="*60)
        print(f"📌 Lignes BRUTES importées depuis Excel : {len(df)}")
        print(f"📌 Colonnes trouvées : {list(df.columns)}")
        
        # Vérification colonnes manquantes
        missing_cols = []
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = ""
                missing_cols.append(col)
        
        if missing_cols:
            print(f"   ⚠️ Colonnes manquantes créées : {missing_cols}")

        for col in OPTIONAL_CONTACT_COLUMNS:
            if col not in df.columns:
                df[col] = ""

        # Nettoyage
        df["NOM"] = df["NOM"].astype(str).map(self._norm_text)
        df["SECTEUR"] = df["SECTEUR"].astype(str).map(self._norm_text)
        df["OUTIL_COMPATIBLE_REFORME"] = df["OUTIL_COMPATIBLE_REFORME"].astype(str).map(self._norm_upper)
        df["APPETENCE_INFORMATIQUE"] = df["APPETENCE_INFORMATIQUE"].astype(str).map(self._norm_upper)
        df.loc[df["APPETENCE_INFORMATIQUE"].str.contains("MEDIOCRE", na=False), "APPETENCE_INFORMATIQUE"] = "FAIBLE"

        # CA - Gestion automatique virgules/points
        print(f"\n🔢 Analyse CA_HONORAIRES_HT :")
        print(f"   Type de données brut : {df['CA_HONORAIRES_HT'].dtype}")
        print(f"   Exemple 5 premières valeurs : {df['CA_HONORAIRES_HT'].head().tolist()}")
        
        # Conversion : remplacer virgules par points si nécessaire
        df["CA_HONORAIRES_HT"] = df["CA_HONORAIRES_HT"].astype(str).str.replace(',', '.', regex=False)
        df["CA_HONORAIRES_HT"] = pd.to_numeric(df["CA_HONORAIRES_HT"], errors="coerce").fillna(0.0)
        
        nb_ca_zero = (df["CA_HONORAIRES_HT"] == 0).sum()
        print(f"   ⚠️ Lignes avec CA = 0 après conversion : {nb_ca_zero}")
        if df["CA_HONORAIRES_HT"].max() > 0:
            print(f"   ✅ CA min : {df['CA_HONORAIRES_HT'].min():.2f} € | max : {df['CA_HONORAIRES_HT'].max():.2f} €")

        # FILTRAGE LIGNES VIDES (NOM)
        print(f"\n🗑️ Filtrage lignes vides :")
        lignes_avant = len(df)
        print(f"   Avant filtrage : {lignes_avant} lignes")
        
        # Exemples de NOM avant filtrage
        noms_exemple = df['NOM'].head(10).tolist()
        if noms_exemple:
            print(f"   Exemples NOM (10 premiers) : {noms_exemple}")
        
        # Vérifier combien de NOM vides
        noms_vides = df["NOM"].str.strip() == ""
        noms_nan = df["NOM"] == "nan"
        total_vides = (noms_vides | noms_nan).sum()
        print(f"   ❌ Lignes avec NOM vide ou 'nan' : {total_vides}")
        
        df = df[~(noms_vides | noms_nan)]
        lignes_apres = len(df)
        print(f"   ✅ Après filtrage : {lignes_apres} lignes conservées")
        print(f"   🗑️ {lignes_avant - lignes_apres} lignes supprimées")
        
        if lignes_apres == 0:
            print(f"\n❌ ERREUR : Aucun client valide après filtrage !")
            print(f"   Vérifiez que votre fichier contient des données dans la colonne NOM.")
            return df
        
        # Vérification valeurs OUTIL
        print(f"\n🔧 Vérification OUTIL_COMPATIBLE_REFORME :")
        valeurs_outil = df["OUTIL_COMPATIBLE_REFORME"].value_counts()
        for val, count in valeurs_outil.items():
            print(f"      '{val}' : {count} clients")
        invalides_outil = df[~df["OUTIL_COMPATIBLE_REFORME"].isin(["OUI", "PARTIELLEMENT", "NON"])]
        if len(invalides_outil) > 0:
            print(f"   ❌ {len(invalides_outil)} lignes avec OUTIL INVALIDE")
            print(f"      Exemples invalides : {invalides_outil['OUTIL_COMPATIBLE_REFORME'].head(5).tolist()}")
            print(f"      Clients concernés : {invalides_outil['NOM'].head(5).tolist()}")
        
        # Vérification valeurs APPÉTENCE
        print(f"\n💡 Vérification APPETENCE_INFORMATIQUE :")
        valeurs_app = df["APPETENCE_INFORMATIQUE"].value_counts()
        for val, count in valeurs_app.items():
            print(f"      '{val}' : {count} clients")
        invalides_app = df[~df["APPETENCE_INFORMATIQUE"].isin(["TRES BON", "BON", "MOYEN", "FAIBLE"])]
        if len(invalides_app) > 0:
            print(f"   ❌ {len(invalides_app)} lignes avec APPÉTENCE INVALIDE")
            print(f"      Exemples invalides : {invalides_app['APPETENCE_INFORMATIQUE'].head(5).tolist()}")
            print(f"      Clients concernés : {invalides_app['NOM'].head(5).tolist()}")

        # SEGMENT
        if "SEGMENT" not in df.columns:
            df["SEGMENT"] = df["CA_HONORAIRES_HT"].apply(self._compute_segment_from_ca)
        else:
            empty_seg = df["SEGMENT"].isna() | (df["SEGMENT"].astype(str).str.strip() == "")
            if empty_seg.any():
                df.loc[empty_seg, "SEGMENT"] = df.loc[empty_seg, "CA_HONORAIRES_HT"].apply(self._compute_segment_from_ca)

        df["DIRIGEANT_PRENOM"] = df["DIRIGEANT_PRENOM"].astype(str).map(self._norm_text).replace({"nan": ""})
        df["DIRIGEANT_NOM"] = df["DIRIGEANT_NOM"].astype(str).map(self._norm_text).replace({"nan": ""})
        df["DIRIGEANT_EMAIL"] = df["DIRIGEANT_EMAIL"].astype(str).map(self._norm_text).replace({"nan": ""})

        # Validation secteurs
        secteurs_inconnus = df[~df["SECTEUR"].isin(SECTEURS_VALIDES) & (df["SECTEUR"] != "")]["SECTEUR"].unique()
        if len(secteurs_inconnus) > 0:
            print(f"\n📂 Secteurs personnalisés (texte libre) : {len(secteurs_inconnus)} secteurs différents")
            if len(secteurs_inconnus) <= 10:
                print(f"   Liste : {', '.join(secteurs_inconnus)}")

        print(f"\n" + "="*60)
        print(f"✅ RÉSULTAT FINAL")
        print(f"="*60)
        print(f"   🎯 CLIENTS VALIDES IMPORTÉS : {len(df)}")
        print(f"   💰 CA TOTAL : {df['CA_HONORAIRES_HT'].sum():,.2f} €")
        if len(df) > 0:
            print(f"   📊 CA MOYEN : {df['CA_HONORAIRES_HT'].mean():,.2f} €")
            print(f"   📈 CA MÉDIAN : {df['CA_HONORAIRES_HT'].median():,.2f} €")
        print(f"="*60 + "\n")

        return df

    def calculate_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        if len(df) == 0:
            return df
            
        df = df.copy()

        df["SCORE_OPPORTUNITE"] = df.apply(self._calculate_client_score, axis=1)
        df["PRIORITE"] = df["SCORE_OPPORTUNITE"].apply(self._assign_priority_internal)
        df["ETOILES"] = df["SCORE_OPPORTUNITE"].apply(self._assign_stars)

        return df

    def _calculate_client_score(self, row) -> float:
        app = self._norm_upper(row.get("APPETENCE_INFORMATIQUE", ""))
        outil = self._norm_upper(row.get("OUTIL_COMPATIBLE_REFORME", ""))

        if "FAIBLE" in app:
            coef_app = 0.5
        elif "MOYEN" in app:
            coef_app = 1
        elif app == "BON":
            coef_app = 2
        elif "TRES BON" in app or "TRÈS BON" in app:
            coef_app = 3
        else:
            coef_app = 0

        if "NON" in outil:
            coef_outil = self.coef["outil_non"]
        elif "PARTIEL" in outil:
            coef_outil = self.coef["outil_part"]
        elif "OUI" in outil:
            coef_outil = self.coef["outil_oui"]
        else:
            coef_outil = 0

        ca = self._safe_float(row.get("CA_HONORAIRES_HT", 0.0), default=0.0)

        score = (ca / 1500.0) * coef_outil * coef_app
        return round(score, 2)

    @staticmethod
    def _assign_priority_internal(score: float) -> str:
        if score >= 30:
            return "PRIORITÉ 1 - Audit Complet"
        if score >= 15:
            return "PRIORITÉ 2 - Formation"
        if score >= 5:
            return "PRIORITÉ 3 - Information"
        return "PRIORITÉ 4 - À Surveiller"

    @staticmethod
    def _assign_stars(score: float) -> str:
        if score >= 50:
            return "⭐⭐⭐⭐⭐"
        if score >= 30:
            return "⭐⭐⭐⭐"
        if score >= 15:
            return "⭐⭐⭐"
        if score >= 5:
            return "⭐⭐"
        return "⭐"

    def generate_summary(self, df: pd.DataFrame) -> Dict:
        total_clients = len(df)
        if total_clients == 0:
            return {
                "total_clients": 0,
                "ca_total": 0.0,
                "tier1_count": 0,
                "tier2_count": 0,
                "tier3_count": 0,
                "ignorer_count": 0,
                "ca_additionnel_max": 0.0,
                "ca_additionnel_min": 0.0,
            }
            
        ca_total = float(df["CA_HONORAIRES_HT"].sum())

        tier1 = df["PRIORITE"].str.contains("PRIORITÉ 1", na=False).sum()
        tier2 = df["PRIORITE"].str.contains("PRIORITÉ 2", na=False).sum()
        tier3 = df["PRIORITE"].str.contains("PRIORITÉ 3", na=False).sum()
        ign = df["PRIORITE"].str.contains("PRIORITÉ 4", na=False).sum()

        ca_add_max = (tier1 * self.tarifs["audit_max"]) + (tier2 * self.tarifs["formation_max"])
        ca_add_min = (tier1 * self.tarifs["audit_min"]) + (tier2 * self.tarifs["formation_min"])

        return {
            "total_clients": total_clients,
            "ca_total": ca_total,
            "tier1_count": int(tier1),
            "tier2_count": int(tier2),
            "tier3_count": int(tier3),
            "ignorer_count": int(ign),
            "ca_additionnel_max": float(ca_add_max),
            "ca_additionnel_min": float(ca_add_min),
        }

    def calculate_advanced_kpis(self, df: pd.DataFrame) -> Dict:
        summary = self.generate_summary(df)
        
        if summary["total_clients"] == 0:
            return {
                "jours_avant_reforme": 0,
                "mois_avant_reforme": 0.0,
                "total_heures_mission": 0,
                "etp_necessaires": 0.0,
                "total_clients": 0,
                "clients_outils_non_conformes": 0,
                "pct_flotte_non_conforme": 0.0,
                "score_maturite_digitale": 0,
                "clients_a_traiter_par_mois": 0,
                "ca_total": 0,
                "ca_total_a_risque": 0,
                "pct_ca_a_risque": 0.0,
                "ca_additionnel_max": 0,
                "valeur_fae_par_dossier": 0,
                "tier1_count": 0,
                "tier2_count": 0,
                "tier3_count": 0,
                "ignorer_count": 0,
            }

        deadline = datetime(2026, 9, 1)
        jours_restants = max(0, (deadline - datetime.now()).days)
        mois_restants = round(jours_restants / 30.0, 1)

        heures_p1 = summary["tier1_count"] * 8
        heures_p2 = summary["tier2_count"] * 3
        heures_p3 = summary["tier3_count"] * 0.5
        total_heures = heures_p1 + heures_p2 + heures_p3

        etp = round(total_heures / 1400.0, 1)

        nb_outils_non = int((df["OUTIL_COMPATIBLE_REFORME"].astype(str).str.upper().str.contains("NON", na=False)).sum())
        pct_outils_non = round((nb_outils_non / len(df) * 100.0) if len(df) else 0.0, 1)

        ca_risque = float(df[df["OUTIL_COMPATIBLE_REFORME"].astype(str).str.upper().str.contains("NON", na=False)]["CA_HONORAIRES_HT"].sum())
        pct_ca_risque = round((ca_risque / summary["ca_total"] * 100.0) if summary["ca_total"] else 0.0, 1)

        nb_outils_ok = int((df["OUTIL_COMPATIBLE_REFORME"].astype(str).str.upper().str.contains("OUI", na=False)).sum())
        nb_app_ok = int((df["APPETENCE_INFORMATIQUE"].astype(str).str.upper().isin(["TRES BON", "TRÈS BON", "BON"])).sum())
        maturite = int(((nb_outils_ok + nb_app_ok) / (2 * len(df))) * 100) if len(df) else 0

        clients_mois = int(summary["total_clients"] / max(mois_restants, 1))

        valeur_par_dossier = int(summary["ca_additionnel_max"] / len(df)) if len(df) else 0

        return {
            "jours_avant_reforme": int(jours_restants),
            "mois_avant_reforme": float(mois_restants),
            "total_heures_mission": int(total_heures),
            "etp_necessaires": float(etp),
            "total_clients": int(summary["total_clients"]),
            "clients_outils_non_conformes": int(nb_outils_non),
            "pct_flotte_non_conforme": float(pct_outils_non),
            "score_maturite_digitale": int(maturite),
            "clients_a_traiter_par_mois": int(clients_mois),
            "ca_total": int(summary["ca_total"]),
            "ca_total_a_risque": int(ca_risque),
            "pct_ca_a_risque": float(pct_ca_risque),
            "ca_additionnel_max": int(summary["ca_additionnel_max"]),
            "valeur_fae_par_dossier": int(valeur_par_dossier),
            "tier1_count": int(summary["tier1_count"]),
            "tier2_count": int(summary["tier2_count"]),
            "tier3_count": int(summary["tier3_count"]),
            "ignorer_count": int(summary["ignorer_count"]),
        }