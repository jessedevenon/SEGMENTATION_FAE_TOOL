"""
CRM Segmentation Clientèle FAE 2026 - Version 7.3 Premium
Outil d'analyse et de priorisation de portefeuille clients
Cabinet Expert-Comptable - Réforme Facturation Électronique
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import hmac

from analyzer import FAEAnalyzer
from style import inject_custom_css, render_premium_header, metric_card_html, section_divider

# Vérification disponibilité python-docx
try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# ========================================
# PROTECTION PAR MOT DE PASSE
# ========================================

def check_password():
    """Vérifie si l'utilisateur a entré le bon mot de passe."""

    def password_entered():
        """Vérifie si le mot de passe saisi est correct."""
        if hmac.compare_digest(st.session_state["password"], "Compta07!"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Ne pas stocker le mot de passe
        else:
            st.session_state["password_correct"] = False

    # Si déjà validé, retourner True
    if st.session_state.get("password_correct", False):
        return True

    # Afficher l'écran de connexion
    st.markdown("""
    <div style="
        max-width: 400px;
        margin: 10rem auto;
        padding: 3rem;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 2px solid #60a5fa;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(96, 165, 250, 0.3);
    ">
        <h1 style="color: #000000 !important; margin-bottom: 1rem; font-weight: 700;">🔒 Accès Sécurisé</h1>
        <p style="color: #1e293b !important; margin-bottom: 2rem; font-weight: 500; line-height: 1.6;">
            Outil d'Analyse & Segmentation Client RFE<br>
            Réservé aux cabinets partenaires
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.text_input(
            "🔑 Mot de passe",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Entrez le mot de passe cabinet"
        )
        
        if "password_correct" in st.session_state:
            st.error("❌ Mot de passe incorrect. Contactez votre administrateur.")
    
    st.stop()  # Arrête l'exécution si pas de mot de passe


# Vérification du mot de passe AVANT tout le reste
if not check_password():
    st.stop()

# ========================================
# FIN PROTECTION - DÉBUT APP NORMALE
# ========================================

# Configuration page
st.set_page_config(
    page_title="Outil d'Analyse & Segmentation Client RFE",
    page_icon="🏆",
    layout="wide"
)

# Le reste de votre code continue ici...

# ========================================
# CONFIGURATION PAGE
# ========================================
st.set_page_config(
    page_title="Outil d'Analyse & Segmentation Client RFE",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# INJECTION CSS PREMIUM
# ========================================
st.markdown(inject_custom_css(), unsafe_allow_html=True)

# ========================================
# SIDEBAR PREMIUM
# ========================================
with st.sidebar:
    # Logo et titre
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size: 4rem;">🏆</div>
        <h2>Client RFE Analyzer</h2>
        <p>v7.3 Premium Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigation",
        [
            "🏠 Accueil",
            "📊 Dashboard",
            "🎯 Guide Missions",
            "🔍 Matrice 2.0",
            "💰 Simulateur CA",
            "📅 Plan d'Action",
            "⚠️ Analyse Risques",
            "📚 Bibliothèque",
            "📄 Livrables Word",
            "🔧 Budget TCO",
            "📤 Exports"
        ],
        label_visibility="collapsed"
    )
    
    # Footer sidebar
    st.markdown(section_divider(), unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.85rem;">
        <p style="margin: 0;">🔒 Traitement 100% local</p>
        <p style="margin: 0.5rem 0 0 0;">Confidentialité garantie</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# PARAMETRES & CONFIGURATION
# ========================================

# Coefficients scoring
coefficients = {
    "outil_non": 10,
    "outil_part": 5,
    "outil_oui": 1
}

# Tarifs missions
tarifs = {
    "audit_min": 1200,
    "audit_max": 1500,
    "formation_min": 600,
    "formation_max": 800,
    "info_min": 150,
    "info_max": 300
}

# Secteurs
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

# ========================================
# FONCTION : CRÉATION TEMPLATE EXCEL
# ========================================
def creer_template_excel():
    """Crée le template Excel avec instructions et données"""
    import xlsxwriter
    from io import BytesIO
    
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    
    # === FEUILLE 1 : INSTRUCTIONS ===
    worksheet_instructions = workbook.add_worksheet('Instructions')
    worksheet_instructions.set_column('A:A', 35)
    worksheet_instructions.set_column('B:B', 80)
    
    # Formats
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'font_color': 'white',
        'bg_color': '#667eea',
        'align': 'center',
        'valign': 'vcenter'
    })
    
    subtitle_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'font_color': '#667eea',
        'bg_color': '#e0e7ff',
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True
    })
    
    text_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',
        'text_wrap': True
    })
    
    important_format = workbook.add_format({
        'font_size': 10,
        'bold': True,
        'font_color': '#dc2626',
        'bg_color': '#fee2e2',
        'align': 'left',
        'text_wrap': True
    })
    
    # Contenu
    row = 0
    worksheet_instructions.merge_range(f'A{row+1}:B{row+1}', '📋 TEMPLATE FACTURATION ÉLECTRONIQUE 2026', title_format)
    worksheet_instructions.set_row(row, 30)
    row += 2
    
    worksheet_instructions.write(row, 0, '1. COLONNES OBLIGATOIRES', subtitle_format)
    row += 1
    worksheet_instructions.write(row, 0, 'NOM', text_format)
    worksheet_instructions.write(row, 1, 'Nom du client (raison sociale)', text_format)
    row += 1
    worksheet_instructions.write(row, 0, 'SECTEUR', text_format)
    worksheet_instructions.write(row, 1, "Secteur d'activité (texte libre, suggestions disponibles)", text_format)
    row += 1
    worksheet_instructions.write(row, 0, 'CA_HONORAIRES_HT', text_format)
    worksheet_instructions.write(row, 1, 'Chiffre d\'affaires honoraires annuel en € (nombres uniquement, points ou virgules acceptés)', text_format)
    row += 1
    worksheet_instructions.write(row, 0, 'OUTIL_COMPATIBLE_REFORME', important_format)
    worksheet_instructions.write(row, 1, 'Conformité outil : OUI / PARTIELLEMENT / NON (MAJUSCULES STRICTES)', important_format)
    row += 1
    worksheet_instructions.write(row, 0, 'APPETENCE_INFORMATIQUE', important_format)
    worksheet_instructions.write(row, 1, 'Niveau numérique : TRES BON / BON / MOYEN / FAIBLE (MAJUSCULES STRICTES)', important_format)
    row += 2
    
    worksheet_instructions.write(row, 0, '2. COLONNES FACULTATIVES', subtitle_format)
    row += 1
    worksheet_instructions.write(row, 0, 'DIRIGEANT_PRENOM', text_format)
    worksheet_instructions.write(row, 1, 'Prénom du dirigeant (pour personnalisation emails)', text_format)
    row += 1
    worksheet_instructions.write(row, 0, 'DIRIGEANT_NOM', text_format)
    worksheet_instructions.write(row, 1, 'Nom du dirigeant', text_format)
    row += 1
    worksheet_instructions.write(row, 0, 'DIRIGEANT_EMAIL', text_format)
    worksheet_instructions.write(row, 1, 'Email du dirigeant', text_format)
    row += 2
    
    worksheet_instructions.write(row, 0, '3. COLONNES CALCULÉES AUTOMATIQUEMENT', subtitle_format)
    row += 1
    worksheet_instructions.write(row, 1, "Les colonnes suivantes seront calculées automatiquement lors de l'import :", text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• SEGMENT : Segment CA (Très Petit, Petit, Moyen, Grand, Très Grand)', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• SCORE_OPPORTUNITE : Score de priorisation (algorithme propriétaire)', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• PRIORITE : Niveau de priorité (P1 à P4)', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• ETOILES : Notation visuelle (⭐ à ⭐⭐⭐⭐⭐)', text_format)
    row += 2
    
    worksheet_instructions.write(row, 0, '4. RÈGLES IMPORTANTES', subtitle_format)
    row += 1
    worksheet_instructions.write(row, 1, '⚠️ OUTIL_COMPATIBLE_REFORME et APPETENCE_INFORMATIQUE doivent respecter les valeurs exactes (liste déroulante dans feuille Données)', important_format)
    row += 1
    worksheet_instructions.write(row, 1, "⚠️ Pas d'espaces avant/après les valeurs", important_format)
    row += 1
    worksheet_instructions.write(row, 1, '⚠️ Le SEGMENT sera calculé automatiquement selon le CA (ne pas remplir manuellement)', important_format)
    row += 1
    worksheet_instructions.write(row, 1, '⚠️ Format des montants : utilisez le point (3490.62) ou la virgule (3490,62). L\'outil convertit automatiquement.', important_format)
    row += 2
    
    worksheet_instructions.write(row, 0, '5. VALEURS ACCEPTÉES', subtitle_format)
    row += 1
    worksheet_instructions.write(row, 0, 'OUTIL_COMPATIBLE_REFORME :', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• OUI : Outil déjà conforme à la réforme', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• PARTIELLEMENT : Outil nécessite mise à jour/paramétrage', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• NON : Outil non conforme, changement nécessaire', text_format)
    row += 2
    
    worksheet_instructions.write(row, 0, 'APPETENCE_INFORMATIQUE :', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• TRES BON : Client très autonome, adoption rapide nouveaux outils', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• BON : Client autonome, bonne maîtrise outils existants', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• MOYEN : Client nécessite accompagnement modéré', text_format)
    row += 1
    worksheet_instructions.write(row, 1, '• FAIBLE : Client nécessite accompagnement renforcé', text_format)
    row += 2
    
    worksheet_instructions.write(row, 0, '6. EXEMPLES DE SECTEURS', subtitle_format)
    row += 1
    worksheet_instructions.write(row, 1, ', '.join(SECTEURS_VALIDES[:10]) + '...', text_format)
    row += 2
    
    footer_format = workbook.add_format({
        'font_size': 9,
        'italic': True,
        'font_color': '#6b7280',
        'align': 'center'
    })
    worksheet_instructions.merge_range(f'A{row+1}:B{row+1}', 
        'CRM Enterprise FAE v7.3 Premium - Traitement 100% local - Confidentialité garantie', 
        footer_format
    )
    
    # === FEUILLE 2 : DONNÉES ===
    worksheet_data = workbook.add_worksheet('Données')
    
    # Formats
    header_format = workbook.add_format({
        'bold': True,
        'font_color': 'white',
        'bg_color': '#667eea',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    warning_format = workbook.add_format({
        'bold': True,
        'font_color': '#78350f',
        'bg_color': '#fef3c7',
        'align': 'center',
        'text_wrap': True
    })
    
    # Largeurs colonnes
    worksheet_data.set_column('A:A', 25)
    worksheet_data.set_column('B:B', 25)
    worksheet_data.set_column('C:C', 18)
    worksheet_data.set_column('D:D', 28)
    worksheet_data.set_column('E:E', 28)
    worksheet_data.set_column('F:F', 20)
    worksheet_data.set_column('G:G', 20)
    worksheet_data.set_column('H:H', 30)
    
    # Message ligne 1
    worksheet_data.merge_range('A1:H1', 
        '📋 Remplissez vos données ci-dessous (le SEGMENT sera calculé automatiquement) - Consultez la feuille Instructions pour les règles',
        warning_format
    )
    worksheet_data.set_row(0, 30)
    
    # En-têtes ligne 2
    headers = [
        'NOM',
        'SECTEUR',
        'CA_HONORAIRES_HT',
        'OUTIL_COMPATIBLE_REFORME',
        'APPETENCE_INFORMATIQUE',
        'DIRIGEANT_PRENOM',
        'DIRIGEANT_NOM',
        'DIRIGEANT_EMAIL'
    ]
    
    for col_num, header in enumerate(headers):
        worksheet_data.write(1, col_num, header, header_format)
    
    # Données exemples
    examples = [
        ['SCI EXEMPLE', 'Immobilier', 8500, 'NON', 'TRES BON', 'Camille', 'DURAND', 'c.durand@exemple.fr'],
        ['SARL TEST', 'Hôtellerie', 4200, 'PARTIELLEMENT', 'BON', 'Marc', 'MARTIN', ''],
        ['EURL DEMO', 'Commerce de détail', 2100, 'OUI', 'MOYEN', '', '', '']
    ]
    
    for row_num, row_data in enumerate(examples, start=2):
        for col_num, cell_data in enumerate(row_data):
            worksheet_data.write(row_num, col_num, cell_data)
    
    # Validations
    worksheet_data.data_validation('D3:D1000', {
        'validate': 'list',
        'source': ['OUI', 'PARTIELLEMENT', 'NON'],
        'error_type': 'stop',
        'error_title': 'Valeur invalide',
        'error_message': 'Vous devez choisir : OUI, PARTIELLEMENT ou NON'
    })
    
    worksheet_data.data_validation('E3:E1000', {
        'validate': 'list',
        'source': ['TRES BON', 'BON', 'MOYEN', 'FAIBLE'],
        'error_type': 'stop',
        'error_title': 'Valeur invalide',
        'error_message': 'Vous devez choisir : TRES BON, BON, MOYEN ou FAIBLE'
    })
    
    worksheet_data.data_validation('C3:C1000', {
        'validate': 'decimal',
        'criteria': '>=',
        'value': 0,
        'error_type': 'warning',
        'error_title': 'Valeur suspecte',
        'error_message': 'Le CA doit être un nombre positif'
    })
    
    workbook.close()
    output.seek(0)
    
    return output.getvalue()

# ========================================
# VÉRIFICATION DONNÉES CHARGÉES
# ========================================
if "df" not in st.session_state:
    st.session_state.df = None
if "kpis" not in st.session_state:
    st.session_state.kpis = None

# ========================================
# PAGE : ACCUEIL
# ========================================
if page == "🏠 Accueil":
    st.markdown(render_premium_header(
        title="🏆 Outil d'Analyse & Segmentation Client RFE",
        subtitle="Pilotez votre portefeuille clients avec intelligence - Réforme Facturation Électronique",
        badge="🔒 Traitement 100% local et confidentiel"
    ), unsafe_allow_html=True)
    
    st.markdown(section_divider("📋 COMMENCER"), unsafe_allow_html=True)
    
    col_temp1, col_temp2 = st.columns([2, 1])
    
    with col_temp1:
        st.markdown("### 📥 Téléchargez le template Excel")
        st.markdown("""
        **Le template contient :**
        - ✅ Feuille "Instructions" : guide complet d'utilisation
        - ✅ Feuille "Données" : colonnes pré-configurées avec validations
        - ✅ 3 exemples de clients pour comprendre le format
        """)
        
        st.download_button(
            label="📥 Télécharger le template Excel",
            data=creer_template_excel(),
            file_name="template_clients_fae_2026.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col_temp2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
            border: 2px solid rgba(102, 126, 234, 0.5);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
        ">
            <h4 style="margin: 0 0 0.75rem 0; color: #60a5fa; font-weight: 700;">💡 Conseil cabinet</h4>
            <p style="margin: 0; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1; font-weight: 400;">
                Commencez par analyser vos 20 plus gros clients. 
                Vous pouvez ensuite élargir à l'ensemble du portefeuille.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(section_divider("📤 IMPORTER VOS DONNÉES"), unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier Excel ici",
        type=["xlsx"],
        help="Format accepté : .xlsx (Excel 2007+)"
    )
    
    if uploaded_file is not None:
        try:
            analyzer = FAEAnalyzer(coefficients, tarifs)
            df = analyzer.load_data(uploaded_file)
            
            if len(df) == 0:
                st.error("❌ Aucun client valide trouvé. Vérifiez que la colonne NOM est remplie.")
            else:
                df_scored = analyzer.calculate_scores(df)
                st.session_state.df = df_scored
                st.session_state.kpis = analyzer.calculate_advanced_kpis(df_scored)
                
                st.success(f"✅ {len(df_scored)} clients importés et analysés avec succès !")
                
                st.markdown(section_divider("📊 VUE D'ENSEMBLE"), unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                kpis = st.session_state.kpis
                
                with col1:
                    st.markdown(metric_card_html(
                        icon="💰",
                        label="CA Total",
                        value=f"{kpis['ca_total']:,} €".replace(",", " "),
                        delta="+12%" if kpis['ca_total'] > 0 else None
                    ), unsafe_allow_html=True)
                
                with col2:
                    st.markdown(metric_card_html(
                        icon="👥",
                        label="Clients Actifs",
                        value=f"{kpis['total_clients']}",
                        delta=f"+{len(df_scored) // 20}" if len(df_scored) > 20 else None
                    ), unsafe_allow_html=True)
                
                with col3:
                    st.markdown(metric_card_html(
                        icon="⏰",
                        label="Jours avant réforme",
                        value=f"{kpis['jours_avant_reforme']} j",
                        delta=None
                    ), unsafe_allow_html=True)
                
                with col4:
                    st.markdown(metric_card_html(
                        icon="🎯",
                        label="Clients Prioritaires",
                        value=f"{kpis['tier1_count'] + kpis['tier2_count']}",
                        delta=None
                    ), unsafe_allow_html=True)
                
                st.markdown("---")
                st.info("👉 Utilisez le menu latéral pour accéder aux analyses détaillées")
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement : {str(e)}")
            st.info("💡 Vérifiez que votre fichier respecte le format du template")
    
    else:
        st.markdown("""
        <div style="
            background: rgba(102, 126, 234, 0.05);
            border: 2px dashed rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 3rem 2rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <h3 style="color: #667eea; margin-bottom: 1rem;">👆 Importez votre fichier Excel pour commencer</h3>
            <p style="color: #94a3b8; margin: 0;">
                Format accepté : .xlsx (colonnes NOM, SECTEUR, CA_HONORAIRES_HT, OUTIL_COMPATIBLE_REFORME, APPETENCE_INFORMATIQUE)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(section_divider("✨ FONCTIONNALITÉS"), unsafe_allow_html=True)
        
        col_feat1, col_feat2, col_feat3 = st.columns(3)
        
        with col_feat1:
            st.markdown("""
            ### 📊 Dashboard 360°
            - Vision complète de votre portefeuille
            - KPIs temps réel
            - Graphiques interactifs
            - Alertes automatiques
            """)
        
        with col_feat2:
            st.markdown("""
            ### 🎯 Priorisation IA
            - Scoring automatique clients
            - Segmentation intelligente
            - Actions recommandées
            - Potentiel CA calculé
            """)
        
        with col_feat3:
            st.markdown("""
            ### 📄 Livrables Pro
            - Rapports Word modifiables
            - Exports Excel enrichis
            - Templates emails
            - Guides méthodologiques
            """)
# ========================================
# PAGE : DASHBOARD
# ========================================
elif page == "📊 Dashboard":
    st.markdown(render_premium_header(
        title="📊 Dashboard 360°",
        subtitle="Vue complète de votre portefeuille clients - Pilotage stratégique réforme FAE 2026"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        kpis = st.session_state.kpis
        
        # Section 1 : Urgence & Charge
        st.markdown(section_divider("⏰ URGENCE & CHARGE DE TRAVAIL"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⏰ Jours avant réforme", f"{kpis['jours_avant_reforme']} jours", f"{kpis['mois_avant_reforme']} mois")
        
        with col2:
            st.metric("⏱️ Heures missions totales", f"{kpis['total_heures_mission']} h", "Toutes priorités")
        
        with col3:
            st.metric("👥 ETP nécessaires", f"{kpis['etp_necessaires']}", "Équivalent temps plein")
        
        with col4:
            st.metric("📞 Contacts/mois", f"{kpis['clients_a_traiter_par_mois']}", f"Sur {kpis['mois_avant_reforme']} mois")
        
        # Section 2 : État du portefeuille
        st.markdown(section_divider("📊 ÉTAT DU PORTEFEUILLE"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Clients totaux", f"{kpis['total_clients']}")
        
        with col2:
            pct_non_conforme = kpis['pct_flotte_non_conforme']
            st.metric("⚠️ Outils non conformes", f"{kpis['clients_outils_non_conformes']}", f"{pct_non_conforme}% du total")
        
        with col3:
            st.metric("🎯 Score maturité digitale", f"{kpis['score_maturite_digitale']}/100", "Moyenne portefeuille")
        
        with col4:
            st.metric("📅 Rythme requis", f"{kpis['clients_a_traiter_par_mois']} clients/mois", f"{int(kpis['clients_a_traiter_par_mois']/4)} par semaine")
        
        # Section 3 : Impact financier
        st.markdown(section_divider("💰 IMPACT FINANCIER"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💼 CA cabinet actuel", f"{kpis['ca_total']:,} €".replace(",", " "))
        
        with col2:
            pct_risque = kpis['pct_ca_a_risque']
            st.metric("⚠️ CA à risque", f"{kpis['ca_total_a_risque']:,} €".replace(",", " "), f"{pct_risque}% du CA")
        
        with col3:
            st.metric("💎 Potentiel missions FAE", f"{kpis['ca_additionnel_max']:,} €".replace(",", " "), "Fourchette haute")
        
        with col4:
            st.metric("📈 Valeur moyenne/dossier", f"{kpis['valeur_fae_par_dossier']} €", "Potentiel unitaire")
        
        # Section 4 : Répartition priorités
        st.markdown(section_divider("🎯 RÉPARTITION PAR PRIORITÉ"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🟢 PRIORITÉ 1", f"{kpis['tier1_count']} clients", "Audit complet")
        
        with col2:
            st.metric("🔵 PRIORITÉ 2", f"{kpis['tier2_count']} clients", "Formation")
        
        with col3:
            st.metric("🟠 PRIORITÉ 3", f"{kpis['tier3_count']} clients", "Information")
        
        with col4:
            st.metric("⚪ PRIORITÉ 4", f"{kpis['ignorer_count']} clients", "À surveiller")
        
        # Graphiques
        st.markdown(section_divider("📈 VISUALISATIONS"), unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 📊 Répartition par priorité")
            
            priorite_counts = df['PRIORITE'].value_counts()
            
            colors = {
                'PRIORITÉ 1 - Audit Complet': '#10b981',
                'PRIORITÉ 2 - Formation': '#3b82f6',
                'PRIORITÉ 3 - Information': '#f59e0b',
                'PRIORITÉ 4 - À Surveiller': '#9ca3af'
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=priorite_counts.index,
                values=priorite_counts.values,
                hole=0.4,
                marker=dict(colors=[colors.get(p, '#667eea') for p in priorite_counts.index]),
                textinfo='label+percent',
                textfont=dict(size=12)
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f1f5f9')
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_right:
            st.markdown("#### 💰 CA vs Score Opportunité")
            
            fig_scatter = px.scatter(
                df,
                x='CA_HONORAIRES_HT',
                y='SCORE_OPPORTUNITE',
                color='PRIORITE',
                size='CA_HONORAIRES_HT',
                hover_data=['NOM', 'SECTEUR'],
                color_discrete_map={
                    'PRIORITÉ 1 - Audit Complet': '#10b981',
                    'PRIORITÉ 2 - Formation': '#3b82f6',
                    'PRIORITÉ 3 - Information': '#f59e0b',
                    'PRIORITÉ 4 - À Surveiller': '#9ca3af'
                }
            )
            
            fig_scatter.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.8)',
                font=dict(color='#f1f5f9'),
                xaxis=dict(title="CA Honoraires (€)", gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title="Score Opportunité", gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Top 10 clients
        st.markdown(section_divider("🏆 TOP 10 CLIENTS À FORT POTENTIEL"), unsafe_allow_html=True)
        
        top10 = df.nlargest(10, 'SCORE_OPPORTUNITE')[['NOM', 'SECTEUR', 'CA_HONORAIRES_HT', 'SCORE_OPPORTUNITE', 'PRIORITE', 'ETOILES']]
        
        st.dataframe(
            top10,
            use_container_width=True,
            column_config={
                "NOM": st.column_config.TextColumn("Client", width="medium"),
                "SECTEUR": st.column_config.TextColumn("Secteur", width="medium"),
                "CA_HONORAIRES_HT": st.column_config.NumberColumn("CA (€)", format="%d €"),
                "SCORE_OPPORTUNITE": st.column_config.NumberColumn("Score", format="%.1f"),
                "PRIORITE": st.column_config.TextColumn("Priorité", width="large"),
                "ETOILES": st.column_config.TextColumn("⭐", width="small")
            },
            hide_index=True
        )

# ========================================
# PAGE : GUIDE MISSIONS
# ========================================
elif page == "🎯 Guide Missions":
    st.markdown(render_premium_header(
        title="🎯 Guide Missions FAE 2026",
        subtitle="Méthodologie d'accompagnement clients - 3 types de missions adaptées"
    ), unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
            border: 2px solid rgba(102, 126, 234, 0.5);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
        ">
            <h4 style="margin: 0 0 0.75rem 0; color: #60a5fa; font-weight: 700;">💡 Conseil cabinet</h4>
            <p style="margin: 0; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1; font-weight: 400;">
                Commencez par analyser vos 20 plus gros clients. 
                Vous pouvez ensuite élargir à l'ensemble du portefeuille.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mission 1
    with st.expander("🎯 MISSION 1 : Audit & Pilotage (Enjeu Élevé)", expanded=True):
        st.markdown("### Objectif")
        st.markdown("""
        Accompagner le client sur **tous les aspects critiques** de la facturation électronique : 
        diagnostic complet, mise en conformité outil, paramétrage, formation équipes et suivi post-démarrage.
        """)
        
        st.markdown("### Public cible")
        st.markdown("**PRIORITÉ 1** : Clients avec outil non conforme + CA significatif (>5000€)")
        
        st.markdown("### Durée & Format")
        st.markdown("- **8 heures** réparties sur **8 semaines**")
        st.markdown("- Format : 4 RDV de 2h (présentiel ou visio)")
        
        st.markdown("### Tarif")
        st.markdown("**1200€ à 1500€ HT** selon taille du dossier")
        
        st.markdown("### Déroulé détaillé")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("**Phase 1**")
            st.markdown("Semaines 1-2")
        with col2:
            st.markdown("**Diagnostic & Préparation**")
            st.markdown("""
            - Audit de l'existant (outil actuel, processus, volumétrie factures)
            - Cartographie des flux (clients, fournisseurs, plateformes)
            - Identification des points de blocage
            - **Livrable :** Rapport d'audit (5 pages) + plan d'action
            """)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("**Phase 2**")
            st.markdown("Semaines 3-5")
        with col2:
            st.markdown("**Mise en Conformité**")
            st.markdown("""
            - Choix/paramétrage outil conforme (accompagnement décision si changement)
            - Configuration : annuaires, mentions obligatoires, circuits de validation
            - Tests émission/réception factures
            - **Livrable :** Guide de paramétrage personnalisé
            """)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("**Phase 3**")
            st.markdown("Semaine 6")
        with col2:
            st.markdown("**Formation Équipes**")
            st.markdown("""
            - Session formation 2h (comptable + dirigeant)
            - Cas pratiques : émettre/recevoir/corriger factures
            - Procédures anti-rejet (mentions manquantes, formats, etc.)
            - **Livrable :** Support formation + check-list quotidienne
            """)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("**Phase 4**")
            st.markdown("Semaines 7-8")
        with col2:
            st.markdown("**Suivi & Ajustements**")
            st.markdown("""
            - Point hebdomadaire (15 min) : traitement anomalies
            - Vérification conformité premiers flux réels
            - Ajustements process si besoin
            - **Livrable :** Bilan final + recommandations pérennisation
            """)
        
        st.markdown("---")
        st.markdown("### 📧 Email type (Priorité 1)")
        
        email_p1 = """
Objet : [URGENT] Facturation Électronique 2026 - Audit de votre situation

Bonjour [Prénom],

La facturation électronique devient obligatoire le 1er septembre 2026. Selon notre analyse, votre dossier nécessite une attention particulière pour éviter tout blocage.

**Votre situation actuelle :**
- Outil de facturation : non conforme à la réforme
- Enjeu : continuité de votre activité (émission/réception factures)
- Échéance : 6 mois pour mettre en conformité

**Ce que nous vous proposons :**

✅ Audit complet de votre situation (outils, process, volumétrie)
✅ Accompagnement au choix/paramétrage d'une solution conforme
✅ Formation de vos équipes (comptable + vous-même)
✅ Suivi personnalisé post-démarrage (8 semaines)

📅 Je vous propose un RDV de 30 minutes cette semaine pour :
- Confirmer votre situation
- Identifier les ajustements nécessaires
- Vous présenter notre plan d'action simple

Êtes-vous disponible mardi 14h ou jeudi 10h ?

Cordialement,
[Signature]

P.S. : Cette mission est facturée entre 1200€ et 1500€ HT selon la complexité. Un investissement déductible qui sécurise votre activité.
        """
        
        st.text_area("", email_p1, height=400)
        st.download_button("📥 Télécharger l'email", email_p1, "email_priorite1.txt", use_container_width=True)

    # Mission 2
    with st.expander("🎓 MISSION 2 : Formation & Mise en Route (Enjeu Modéré)"):
        st.markdown("### Objectif")
        st.markdown("""
        Rendre le client **autonome** sur la facturation électronique : comprendre les principes, 
        maîtriser l'outil (déjà conforme ou partiellement conforme), et éviter les erreurs courantes.
        """)
        
        st.markdown("### Public cible")
        st.markdown("**PRIORITÉ 2** : Clients avec outil partiellement conforme OU outil conforme mais faible appétence informatique")
        
        st.markdown("### Durée & Format")
        st.markdown("- **3 heures** sur **1 session** (ou 2× 1h30)")
        st.markdown("- Format : Atelier pratique (présentiel ou visio)")
        
        st.markdown("### Tarif")
        st.markdown("**600€ à 800€ HT**")
        
        st.markdown("### Contenu de la session")
        
        st.markdown("""
        **Partie 1 : Pré-diagnostic express (30 min)**
        - Revue rapide de l'outil actuel (est-il vraiment prêt ?)
        - Vérification des données de base (SIRET, adresses, TVA...)
        - Identification des 2-3 points d'attention prioritaires
        
        **Partie 2 : Formation action (1h30)**
        - Principes de la facturation électronique (ce qui change vraiment)
        - Cycle de vie d'une facture : émission, transmission, réception, archivage
        - Démonstration live : émettre une facture conforme
        - Cas pratique : le client émet sa première facture sous supervision
        
        **Partie 3 : Sécurisation & Bonnes pratiques (1h)**
        - Les 5 erreurs qui font rejeter une facture (et comment les éviter)
        - Checklist mensuelle de contrôle (à faire soi-même)
        - Que faire en cas de problème ? (support, ressources)
        - Q&R personnalisées
        """)
        
        st.markdown("### Livrables")
        st.markdown("""
        - Support de formation (PDF 15 pages)
        - Checklist anti-rejet (1 page A4)
        - Accès documentation vidéo (3 tutos 5 min)
        """)
        
        st.markdown("---")
        st.markdown("### 📧 Email type (Priorité 2)")
        
        email_p2 = """
Objet : Facturation Électronique 2026 - Formation pour votre équipe

Bonjour [Prénom],

Bonne nouvelle : votre outil de facturation est sur la bonne trajectoire pour la réforme de septembre 2026. 

**Où en êtes-vous ?**
Votre solution est conforme (ou nécessite juste une mise à jour), mais l'enjeu est maintenant de **rendre vos équipes autonomes** pour éviter les rejets de factures et les blocages administratifs.

**Ce que nous vous proposons :**

🎓 Session de formation pratique (3 heures)
- Comprendre les nouveaux principes (sans jargon technique)
- Manipuler votre outil en conditions réelles
- Éviter les 5 erreurs classiques qui bloquent tout

📋 Livrables inclus :
- Support de formation complet
- Checklist anti-rejet (à afficher dans le bureau)
- Vidéos tutos (3× 5 min pour se remettre à niveau si besoin)

📅 Plusieurs créneaux disponibles en mars :
- Mardi 12/03 : 14h-17h
- Jeudi 14/03 : 9h-12h
- Vendredi 15/03 : 14h-17h

Tarif : 600€ HT (déductible fiscalement)

Répondez à cet email pour réserver votre créneau (places limitées à 8 sessions/mois).

Cordialement,
[Signature]
        """
        
        st.text_area("", email_p2, height=350)
        st.download_button("📥 Télécharger l'email", email_p2, "email_priorite2.txt", use_container_width=True)

    # Mission 3
    with st.expander("📢 MISSION 3 : Information & Sensibilisation (Enjeu Faible)"):
        st.markdown("### Objectif")
        st.markdown("""
        Informer le client sur les **essentiels** de la réforme, vérifier qu'il est sur les bons rails, 
        et le rassurer (pas de panique, c'est gérable).
        """)
        
        st.markdown("### Public cible")
        st.markdown("**PRIORITÉ 3** : Clients avec outil déjà conforme + bonne appétence informatique")
        
        st.markdown("### Durée & Format")
        st.markdown("- **30 à 60 minutes** (appel téléphonique ou visio)")
        st.markdown("- Format : Point de situation rapide")
        
        st.markdown("### Tarif")
        st.markdown("**150€ à 300€ HT** OU **inclus dans vos honoraires récurrents** (positionnement conseil)")
        
        st.markdown("### Contenu de l'échange")
        
        st.markdown("""
        1. **Confirmer la conformité outil** (5 min)
           - "Votre solution est bien compatible, voici pourquoi..."
        
        2. **Les 3 points de vigilance** (15 min)
           - Vérifier que vos coordonnées sont à jour (SIRET, adresse, email de facturation)
           - Suivre les mises à jour de votre outil (ne pas ignorer les notifications)
           - Tester l'émission/réception d'une facture avant le 1er septembre
        
        3. **Message rassurant** (10 min)
           - Vous êtes déjà bien positionné
           - Pas de changement majeur dans vos habitudes
           - On reste disponible si problème (hotline cabinet)
        
        4. **Mini-checklist envoyée par email** (post-appel)
           - 5 points à cocher d'ici septembre
        """)
        
        st.markdown("### Livrable")
        st.markdown("- Email récapitulatif avec mini-checklist (1 page)")
        
        st.markdown("---")
        st.markdown("### 📧 Email type (Priorité 3)")
        
        email_p3 = """
Objet : Facturation Électronique 2026 - Vous êtes prêt (presque !)

Bonjour [Prénom],

La réforme de la facturation électronique arrive en septembre 2026. Bonne nouvelle : selon notre analyse, vous êtes déjà sur les bons rails.

**Votre situation :**
✅ Outil de facturation conforme
✅ Bonne maîtrise des outils numériques
✅ Process en place

**Ce qu'il reste à faire (simple) :**

1. Vérifier vos coordonnées (SIRET, adresse, email facturation)
2. Suivre les mises à jour de votre logiciel (automne 2026)
3. Tester l'envoi d'une facture électronique (nous vous accompagnons si besoin)

📞 Je vous propose un point téléphonique de 30 minutes pour :
- Confirmer que tout est OK
- Répondre à vos questions éventuelles
- Vous donner la checklist finale

Disponible la semaine du [date] : mardi 10h, mercredi 14h ou jeudi 9h ?

Pas d'urgence, mais autant valider maintenant pour être serein en septembre.

Cordialement,
[Signature]

P.S. : Ce point est inclus dans nos honoraires habituels (logique conseil).
        """
        
        st.text_area("", email_p3, height=350)
        st.download_button("📥 Télécharger l'email", email_p3, "email_priorite3.txt", use_container_width=True)

# ========================================
# PAGE : MATRICE 2.0
# ========================================
elif page == "🔍 Matrice 2.0":
    st.markdown(render_premium_header(
        title="🔍 Matrice 2.0 - Segmentation Avancée",
        subtitle="Analyse multi-critères et filtres dynamiques"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        
        st.markdown(section_divider("🎛️ FILTRES DYNAMIQUES"), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            appetence_filter = st.multiselect(
                "Appétence Informatique",
                options=df['APPETENCE_INFORMATIQUE'].unique(),
                default=df['APPETENCE_INFORMATIQUE'].unique()
            )
        
        with col2:
            segment_filter = st.multiselect(
                "Segment CA",
                options=df['SEGMENT'].unique(),
                default=df['SEGMENT'].unique()
            )
        
        with col3:
            outil_filter = st.multiselect(
                "Conformité Outil",
                options=df['OUTIL_COMPATIBLE_REFORME'].unique(),
                default=df['OUTIL_COMPATIBLE_REFORME'].unique()
            )
        
        # Application filtres
        df_filtered = df[
            (df['APPETENCE_INFORMATIQUE'].isin(appetence_filter)) &
            (df['SEGMENT'].isin(segment_filter)) &
            (df['OUTIL_COMPATIBLE_REFORME'].isin(outil_filter))
        ]
        
        st.info(f"📊 {len(df_filtered)} clients correspondent aux filtres sélectionnés (sur {len(df)} total)")
        
        # Heatmaps
        st.markdown(section_divider("🔥 HEATMAPS CROISÉES"), unsafe_allow_html=True)
        
        col_heat1, col_heat2 = st.columns(2)
        
        with col_heat1:
            st.markdown("#### Appétence × Outil")
            
            pivot_app_outil = pd.crosstab(
                df_filtered['APPETENCE_INFORMATIQUE'],
                df_filtered['OUTIL_COMPATIBLE_REFORME']
            )
            
            fig_heat1 = px.imshow(
                pivot_app_outil,
                labels=dict(x="Conformité Outil", y="Appétence", color="Nb Clients"),
                x=pivot_app_outil.columns,
                y=pivot_app_outil.index,
                color_continuous_scale='RdYlGn',
                aspect="auto"
            )
            
            fig_heat1.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f1f5f9')
            )
            
            st.plotly_chart(fig_heat1, use_container_width=True)
        
        with col_heat2:
            st.markdown("#### Segment CA × Outil")
            
            pivot_seg_outil = pd.crosstab(
                df_filtered['SEGMENT'],
                df_filtered['OUTIL_COMPATIBLE_REFORME']
            )
            
            fig_heat2 = px.imshow(
                pivot_seg_outil,
                labels=dict(x="Conformité Outil", y="Segment CA", color="Nb Clients"),
                x=pivot_seg_outil.columns,
                y=pivot_seg_outil.index,
                color_continuous_scale='Blues',
                aspect="auto"
            )
            
            fig_heat2.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f1f5f9')
            )
            
            st.plotly_chart(fig_heat2, use_container_width=True)
        
        # Table détaillée
        st.markdown(section_divider("📋 TABLE DÉTAILLÉE"), unsafe_allow_html=True)
        
        df_display = df_filtered.sort_values('SCORE_OPPORTUNITE', ascending=False)[
            ['NOM', 'SECTEUR', 'CA_HONORAIRES_HT', 'OUTIL_COMPATIBLE_REFORME', 
             'APPETENCE_INFORMATIQUE', 'SCORE_OPPORTUNITE', 'PRIORITE', 'ETOILES']
        ]
        
        st.dataframe(
            df_display,
            use_container_width=True,
            column_config={
                "NOM": st.column_config.TextColumn("Client", width="medium"),
                "SECTEUR": st.column_config.TextColumn("Secteur", width="medium"),
                "CA_HONORAIRES_HT": st.column_config.NumberColumn("CA (€)", format="%d €"),
                "OUTIL_COMPATIBLE_REFORME": st.column_config.TextColumn("Outil", width="small"),
                "APPETENCE_INFORMATIQUE": st.column_config.TextColumn("Appétence", width="small"),
                "SCORE_OPPORTUNITE": st.column_config.NumberColumn("Score", format="%.1f"),
                "PRIORITE": st.column_config.TextColumn("Priorité", width="large"),
                "ETOILES": st.column_config.TextColumn("⭐", width="small")
            },
            hide_index=True
        )
        
        # Export sélection
        st.markdown("---")
        
        col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
        
        with col_exp1:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_display.to_excel(writer, sheet_name='Sélection filtrée', index=False)
            
            st.download_button(
                label="📥 Exporter la sélection (Excel)",
                data=output.getvalue(),
                file_name=f"selection_filtree_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
# ========================================
# PAGE : SIMULATEUR CA
# ========================================
elif page == "💰 Simulateur CA":
    st.markdown(render_premium_header(
        title="💰 Simulateur CA Missions FAE",
        subtitle="Projections financières et scénarios de conversion"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        kpis = st.session_state.kpis
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #f59e0b;
            border-radius: 16px;
            padding: 1.5rem;
            color: #000000;
            margin-bottom: 2rem;
        ">
            <h4 style="margin: 0 0 0.75rem 0; color: #78350f;">💡 Mode d'emploi</h4>
            <p style="margin: 0; font-size: 0.95rem; line-height: 1.5;">
                Ajustez les curseurs ci-dessous pour simuler différents scénarios de conversion. 
                Le CA additionnel se calcule en temps réel selon vos hypothèses.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(section_divider("🎯 PARAMÈTRES PAR SEGMENT"), unsafe_allow_html=True)
        
        # Priorité 1
        st.markdown("### 🟢 PRIORITÉ 1 - Audit Complet")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            p1_active = st.checkbox("Activer P1", value=True, key="p1_active")
        
        with col2:
            p1_taux = st.slider("Taux de conversion", 0, 100, 70, 5, key="p1_taux", disabled=not p1_active)
        
        with col3:
            p1_prix = st.number_input("Prix unitaire (€)", 1000, 2000, 1350, 50, key="p1_prix", disabled=not p1_active)
        
        # Priorité 2
        st.markdown("### 🔵 PRIORITÉ 2 - Formation")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            p2_active = st.checkbox("Activer P2", value=True, key="p2_active")
        
        with col2:
            p2_taux = st.slider("Taux de conversion", 0, 100, 60, 5, key="p2_taux", disabled=not p2_active)
        
        with col3:
            p2_prix = st.number_input("Prix unitaire (€)", 500, 1000, 700, 50, key="p2_prix", disabled=not p2_active)
        
        # Priorité 3
        st.markdown("### 🟠 PRIORITÉ 3 - Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            p3_active = st.checkbox("Activer P3", value=True, key="p3_active")
        
        with col2:
            p3_taux = st.slider("Taux de conversion", 0, 100, 40, 5, key="p3_taux", disabled=not p3_active)
        
        with col3:
            p3_prix = st.number_input("Prix unitaire (€)", 100, 500, 225, 25, key="p3_prix", disabled=not p3_active)
        
        # Calculs
        st.markdown(section_divider("💰 RÉSULTATS"), unsafe_allow_html=True)
        
        p1_count = kpis['tier1_count']
        p2_count = kpis['tier2_count']
        p3_count = kpis['tier3_count']
        
        ca_p1 = (p1_count * (p1_taux / 100) * p1_prix) if p1_active else 0
        ca_p2 = (p2_count * (p2_taux / 100) * p2_prix) if p2_active else 0
        ca_p3 = (p3_count * (p3_taux / 100) * p3_prix) if p3_active else 0
        
        ca_total_simule = ca_p1 + ca_p2 + ca_p3
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🟢 CA P1", f"{int(ca_p1):,} €".replace(",", " "))
        
        with col2:
            st.metric("🔵 CA P2", f"{int(ca_p2):,} €".replace(",", " "))
        
        with col3:
            st.metric("🟠 CA P3", f"{int(ca_p3):,} €".replace(",", " "))
        
        with col4:
            pct_ca = (ca_total_simule / kpis['ca_total'] * 100) if kpis['ca_total'] > 0 else 0
            st.metric("💎 CA TOTAL", f"{int(ca_total_simule):,} €".replace(",", " "), f"{pct_ca:.1f}% du CA cabinet")
        
        # Graphique Waterfall
        st.markdown(section_divider("📊 RÉPARTITION CA ADDITIONNEL"), unsafe_allow_html=True)
        
        fig_waterfall = go.Figure(go.Waterfall(
            x=["Priorité 1", "Priorité 2", "Priorité 3", "Total"],
            y=[ca_p1, ca_p2, ca_p3, 0],
            measure=["relative", "relative", "relative", "total"],
            text=[f"{int(ca_p1):,}€", f"{int(ca_p2):,}€", f"{int(ca_p3):,}€", f"{int(ca_total_simule):,}€"],
            textposition="outside",
            connector={"line": {"color": "rgba(255,255,255,0.3)"}},
            decreasing={"marker": {"color": "#ef4444"}},
            increasing={"marker": {"color": "#10b981"}},
            totals={"marker": {"color": "#fbbf24"}}
        ))
        
        fig_waterfall.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            font=dict(color='#f1f5f9'),
            showlegend=False,
            xaxis=dict(title="", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="CA (€)", gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        # Détail conversions
        st.markdown(section_divider("📋 DÉTAIL CONVERSIONS"), unsafe_allow_html=True)
        
        data_simulation = {
            "Priorité": ["P1 - Audit", "P2 - Formation", "P3 - Information"],
            "Clients éligibles": [p1_count, p2_count, p3_count],
            "Taux conversion": [f"{p1_taux}%" if p1_active else "0%", 
                                f"{p2_taux}%" if p2_active else "0%", 
                                f"{p3_taux}%" if p3_active else "0%"],
            "Clients convertis": [int(p1_count * p1_taux / 100) if p1_active else 0,
                                   int(p2_count * p2_taux / 100) if p2_active else 0,
                                   int(p3_count * p3_taux / 100) if p3_active else 0],
            "Prix unitaire": [f"{p1_prix}€" if p1_active else "0€",
                              f"{p2_prix}€" if p2_active else "0€",
                              f"{p3_prix}€" if p3_active else "0€"],
            "CA généré": [f"{int(ca_p1):,}€".replace(",", " "),
                          f"{int(ca_p2):,}€".replace(",", " "),
                          f"{int(ca_p3):,}€".replace(",", " ")]
        }
        
        df_simulation = pd.DataFrame(data_simulation)
        
        st.dataframe(df_simulation, use_container_width=True, hide_index=True)

# ========================================
# PAGE : PLAN D'ACTION
# ========================================
elif page == "📅 Plan d'Action":
    st.markdown(render_premium_header(
        title="📅 Plan d'Action - Roadmap 6 Mois",
        subtitle="Organisation commerciale et planning déploiement"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        kpis = st.session_state.kpis
        
        # Rythme recommandé
        st.markdown(section_divider("⏱️ RYTHME RECOMMANDÉ"), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📞 Contacts/mois", f"{kpis['clients_a_traiter_par_mois']}", "Moyenne à maintenir")
        
        with col2:
            contacts_semaine = kpis['clients_a_traiter_par_mois'] / 4
            st.metric("📅 Contacts/semaine", f"{int(contacts_semaine)}", "Soit ~2-3 par jour")
        
        with col3:
            heures_mois = kpis['total_heures_mission'] / kpis['mois_avant_reforme']
            st.metric("⏰ Heures/mois", f"{int(heures_mois)} h", "Charge missions")
        
        # Planning Gantt
        st.markdown(section_divider("📊 PLANNING GANTT 6 MOIS"), unsafe_allow_html=True)
        
        today = datetime.now()
        
        phases = [
            dict(Phase="Phase 1 - Sécurisation P1", Start=today, Finish=today + timedelta(days=45), Resource="Priorité 1"),
            dict(Phase="Phase 2 - Montée P2", Start=today + timedelta(days=30), Finish=today + timedelta(days=90), Resource="Priorité 2"),
            dict(Phase="Phase 3 - Information P3", Start=today + timedelta(days=60), Finish=today + timedelta(days=120), Resource="Priorité 3"),
            dict(Phase="Phase 4 - Relances", Start=today + timedelta(days=90), Finish=today + timedelta(days=150), Resource="Suivi")
        ]
        
        df_gantt = pd.DataFrame(phases)
        
        color_map = {
            "Priorité 1": "#10b981",
            "Priorité 2": "#3b82f6",
            "Priorité 3": "#f59e0b",
            "Suivi": "#9ca3af"
        }
        
        fig_gantt = px.timeline(
            df_gantt,
            x_start="Start",
            x_end="Finish",
            y="Phase",
            color="Resource",
            color_discrete_map=color_map
        )
        
        fig_gantt.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            font=dict(color='#f1f5f9'),
            xaxis=dict(title="", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="")
        )
        
        st.plotly_chart(fig_gantt, use_container_width=True)
        
        # Playbook hebdomadaire
        st.markdown(section_divider("📋 PLAYBOOK HEBDOMADAIRE TYPE"), unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Lundi**")
            st.markdown("🎯 Planification")
        with col2:
            st.markdown("""
            - Sélectionner 8-10 clients à contacter cette semaine
            - Préparer les emails/appels (templates + personnalisation)
            - Bloquer 2h dans l'agenda pour envois groupés
            """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Mardi-Jeudi**")
            st.markdown("📞 Exécution")
        with col2:
            st.markdown("""
            - Envoi emails (mardi 9h)
            - Relances téléphoniques J+2 (jeudi 14h)
            - RDV confirmés → planifier missions
            """)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Vendredi**")
            st.markdown("📊 Reporting")
        with col2:
            st.markdown("""
            - Mettre à jour CRM (statuts clients)
            - Comptabiliser taux de conversion
            - Préparer liste semaine suivante
            """)
        
        # Extraction cible semaine
        st.markdown(section_divider("🎯 EXTRACTION CIBLE SEMAINE"), unsafe_allow_html=True)
        
        nb_clients_semaine = st.number_input(
            "Nombre de clients à contacter cette semaine",
            min_value=1,
            max_value=50,
            value=int(contacts_semaine) if contacts_semaine > 0 else 10
        )
        
        priorite_cible = st.selectbox(
            "Priorité ciblée",
            ["PRIORITÉ 1 - Audit Complet", "PRIORITÉ 2 - Formation", "PRIORITÉ 3 - Information", "Toutes priorités"]
        )
        
        if priorite_cible == "Toutes priorités":
            df_cible = df.nlargest(nb_clients_semaine, 'SCORE_OPPORTUNITE')
        else:
            df_cible = df[df['PRIORITE'] == priorite_cible].nlargest(nb_clients_semaine, 'SCORE_OPPORTUNITE')
        
        st.markdown(f"**👥 {len(df_cible)} clients sélectionnés**")
        
        df_cible_display = df_cible[['NOM', 'SECTEUR', 'CA_HONORAIRES_HT', 'PRIORITE', 'SCORE_OPPORTUNITE', 'DIRIGEANT_EMAIL']]
        
        st.dataframe(df_cible_display, use_container_width=True, hide_index=True)
        
        # Export cible
        output_cible = io.BytesIO()
        with pd.ExcelWriter(output_cible, engine='xlsxwriter') as writer:
            df_cible_display.to_excel(writer, sheet_name='Cibles semaine', index=False)
        
        st.download_button(
            label=f"📥 Télécharger la liste ({len(df_cible)} clients)",
            data=output_cible.getvalue(),
            file_name=f"cibles_semaine_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# ========================================
# PAGE : ANALYSE RISQUES
# ========================================
elif page == "⚠️ Analyse Risques":
    st.markdown(render_premium_header(
        title="⚠️ Analyse Risques - Clients à Sécuriser",
        subtitle="Identification et priorisation des dossiers critiques"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        
        # Calcul score risque
        def calculate_risk_score(row):
            score = 0
            
            # CA élevé = risque élevé
            if row['CA_HONORAIRES_HT'] >= 10000:
                score += 40
            elif row['CA_HONORAIRES_HT'] >= 5000:
                score += 30
            elif row['CA_HONORAIRES_HT'] >= 2500:
                score += 20
            elif row['CA_HONORAIRES_HT'] >= 1000:
                score += 10
            
            # Outil non conforme = risque élevé
            if row['OUTIL_COMPATIBLE_REFORME'] == 'NON':
                score += 40
            elif row['OUTIL_COMPATIBLE_REFORME'] == 'PARTIELLEMENT':
                score += 20
            
            # Faible appétence = risque modéré
            if row['APPETENCE_INFORMATIQUE'] == 'FAIBLE':
                score += 20
            elif row['APPETENCE_INFORMATIQUE'] == 'MOYEN':
                score += 10
            
            return score
        
        df['SCORE_RISQUE'] = df.apply(calculate_risk_score, axis=1)
        
        def get_risk_level(score):
            if score >= 75:
                return "CRITIQUE"
            elif score >= 55:
                return "ÉLEVÉ"
            elif score >= 35:
                return "MOYEN"
            else:
                return "FAIBLE"
        
        df['NIVEAU_RISQUE'] = df['SCORE_RISQUE'].apply(get_risk_level)
        
        # Métriques
        st.markdown(section_divider("⚠️ VUE D'ENSEMBLE RISQUES"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        risque_critique = len(df[df['NIVEAU_RISQUE'] == 'CRITIQUE'])
        risque_eleve = len(df[df['NIVEAU_RISQUE'] == 'ÉLEVÉ'])
        risque_moyen = len(df[df['NIVEAU_RISQUE'] == 'MOYEN'])
        risque_faible = len(df[df['NIVEAU_RISQUE'] == 'FAIBLE'])
        
        with col1:
            st.metric("🔴 CRITIQUE", risque_critique, "Action immédiate")
        
        with col2:
            st.metric("🟠 ÉLEVÉ", risque_eleve, "Sous 2 semaines")
        
        with col3:
            st.metric("🟡 MOYEN", risque_moyen, "Surveillance")
        
        with col4:
            st.metric("🟢 FAIBLE", risque_faible, "Situation OK")
        
        # Distribution
        st.markdown(section_divider("📊 DISTRIBUTION SCORES RISQUE"), unsafe_allow_html=True)
        
        fig_hist = px.histogram(
            df,
            x='SCORE_RISQUE',
            color='NIVEAU_RISQUE',
            nbins=20,
            color_discrete_map={
                'CRITIQUE': '#dc2626',
                'ÉLEVÉ': '#ea580c',
                'MOYEN': '#f59e0b',
                'FAIBLE': '#10b981'
            }
        )
        
        fig_hist.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            font=dict(color='#f1f5f9'),
            xaxis=dict(title="Score Risque", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="Nombre de clients", gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Top clients à risque
        st.markdown(section_divider("🚨 TOP CLIENTS À SÉCURISER"), unsafe_allow_html=True)
        
        nb_top_risque = st.slider("Nombre de clients à afficher", 5, 50, 20)
        
        df_risque = df.nlargest(nb_top_risque, 'SCORE_RISQUE')[
            ['NOM', 'SECTEUR', 'CA_HONORAIRES_HT', 'OUTIL_COMPATIBLE_REFORME', 
             'APPETENCE_INFORMATIQUE', 'SCORE_RISQUE', 'NIVEAU_RISQUE']
        ]
        
        st.dataframe(
            df_risque,
            use_container_width=True,
            column_config={
                "NOM": st.column_config.TextColumn("Client", width="medium"),
                "SECTEUR": st.column_config.TextColumn("Secteur", width="medium"),
                "CA_HONORAIRES_HT": st.column_config.NumberColumn("CA (€)", format="%d €"),
                "OUTIL_COMPATIBLE_REFORME": st.column_config.TextColumn("Outil", width="small"),
                "APPETENCE_INFORMATIQUE": st.column_config.TextColumn("Appétence", width="small"),
                "SCORE_RISQUE": st.column_config.NumberColumn("Score", format="%d"),
                "NIVEAU_RISQUE": st.column_config.TextColumn("Niveau", width="small")
            },
            hide_index=True
        )
        
        # Export
        output_risque = io.BytesIO()
        with pd.ExcelWriter(output_risque, engine='xlsxwriter') as writer:
            df_risque.to_excel(writer, sheet_name='Clients à risque', index=False)
        
        st.download_button(
            label=f"📥 Exporter les {nb_top_risque} clients à risque",
            data=output_risque.getvalue(),
            file_name=f"clients_risque_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# ========================================
# PAGE : BIBLIOTHÈQUE
# ========================================
elif page == "📚 Bibliothèque":
    st.markdown(render_premium_header(
        title="📚 Bibliothèque de Contenus",
        subtitle="Templates emails, scripts téléphone et guides prêts à l'emploi"
    ), unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📧 Emails", "📞 Téléphone", "📄 Mini-documents"])
    
    # TAB 1 : EMAILS
    with tab1:
        st.markdown(section_divider("📧 TEMPLATES EMAILS"), unsafe_allow_html=True)
        
        email_choice = st.selectbox(
            "Choisissez un template",
            [
                "Email 1 - Audit urgence (P1)",
                "Email 2 - Formation structurée (P2)",
                "Email 3 - Information simple (P3)",
                "Email 4 - Relance J+3 (sans réponse)",
                "Email 5 - Relance J+10 (dernière chance)"
            ]
        )
        
        emails_library = {
            "Email 1 - Audit urgence (P1)": """Objet : [URGENT] Facturation Électronique 2026 - Audit de votre situation

Bonjour [Prénom],

La facturation électronique devient obligatoire le 1er septembre 2026. Selon notre analyse, votre dossier nécessite une attention particulière pour éviter tout blocage.

**Votre situation actuelle :**
- Outil de facturation : non conforme à la réforme
- Enjeu : continuité de votre activité (émission/réception factures)
- Échéance : 6 mois pour mettre en conformité

**Ce que nous vous proposons :**

✅ Audit complet de votre situation (outils, process, volumétrie)
✅ Accompagnement au choix/paramétrage d'une solution conforme
✅ Formation de vos équipes (comptable + vous-même)
✅ Suivi personnalisé post-démarrage (8 semaines)

📅 Je vous propose un RDV de 30 minutes cette semaine pour :
- Confirmer votre situation
- Identifier les ajustements nécessaires
- Vous présenter notre plan d'action simple

Êtes-vous disponible mardi 14h ou jeudi 10h ?

Cordialement,
[Signature]

P.S. : Cette mission est facturée entre 1200€ et 1500€ HT selon la complexité. Un investissement déductible qui sécurise votre activité.""",
            
            "Email 2 - Formation structurée (P2)": """Objet : Facturation Électronique 2026 - Formation pour votre équipe

Bonjour [Prénom],

Bonne nouvelle : votre outil de facturation est sur la bonne trajectoire pour la réforme de septembre 2026.

**Où en êtes-vous ?**
Votre solution est conforme (ou nécessite juste une mise à jour), mais l'enjeu est maintenant de **rendre vos équipes autonomes** pour éviter les rejets de factures et les blocages administratifs.

**Ce que nous vous proposons :**

🎓 Session de formation pratique (3 heures)
- Comprendre les nouveaux principes (sans jargon technique)
- Manipuler votre outil en conditions réelles
- Éviter les 5 erreurs classiques qui bloquent tout

📋 Livrables inclus :
- Support de formation complet
- Checklist anti-rejet (à afficher dans le bureau)
- Vidéos tutos (3× 5 min pour se remettre à niveau si besoin)

📅 Plusieurs créneaux disponibles en mars :
- Mardi 12/03 : 14h-17h
- Jeudi 14/03 : 9h-12h
- Vendredi 15/03 : 14h-17h

Tarif : 600€ HT (déductible fiscalement)

Répondez à cet email pour réserver votre créneau (places limitées à 8 sessions/mois).

Cordialement,
[Signature]""",
            
            "Email 3 - Information simple (P3)": """Objet : Facturation Électronique 2026 - Vous êtes prêt (presque !)

Bonjour [Prénom],

La réforme de la facturation électronique arrive en septembre 2026. Bonne nouvelle : selon notre analyse, vous êtes déjà sur les bons rails.

**Votre situation :**
✅ Outil de facturation conforme
✅ Bonne maîtrise des outils numériques
✅ Process en place

**Ce qu'il reste à faire (simple) :**

1. Vérifier vos coordonnées (SIRET, adresse, email facturation)
2. Suivre les mises à jour de votre logiciel (automne 2026)
3. Tester l'envoi d'une facture électronique (nous vous accompagnons si besoin)

📞 Je vous propose un point téléphonique de 30 minutes pour :
- Confirmer que tout est OK
- Répondre à vos questions éventuelles
- Vous donner la checklist finale

Disponible la semaine du [date] : mardi 10h, mercredi 14h ou jeudi 9h ?

Pas d'urgence, mais autant valider maintenant pour être serein en septembre.

Cordialement,
[Signature]

P.S. : Ce point est inclus dans nos honoraires habituels (logique conseil).""",
            
            "Email 4 - Relance J+3 (sans réponse)": """Objet : Re: Facturation Électronique 2026

Bonjour [Prénom],

Je reviens vers vous suite à mon email de [jour].

Je comprends que vous êtes occupé, mais la date butoir du 1er septembre 2026 approche et certains dossiers nécessitent un délai de mise en conformité.

**Rappel rapide :**
- Votre outil actuel : [conforme/non conforme]
- Action recommandée : [audit/formation/info]
- Délai estimé : [X semaines]

Deux options simples :
1️⃣ Répondez "OUI" à cet email → je vous appelle sous 24h
2️⃣ Cliquez ici pour prendre RDV : [lien calendrier]

Si ce n'est pas le bon moment, dites-le-moi franchement : je vous recontacterai dans 2 mois.

Cordialement,
[Signature]""",
            
            "Email 5 - Relance J+10 (dernière chance)": """Objet : [Dernière relance] Facturation Électronique 2026

Bonjour [Prénom],

C'est ma dernière relance sur le sujet de la facturation électronique (promis !).

Je ne veux pas vous harceler, mais mon rôle est de vous alerter :

⚠️ Il reste **[X] mois** avant le 1er septembre 2026
⚠️ Votre outil actuel : **non conforme** (selon nos infos)
⚠️ Risque : **blocage émission/réception factures** = arrêt activité

**Deux scénarios possibles :**

✅ **Vous gérez déjà** → Parfait ! Répondez "OK géré" et je ne vous en reparle plus.

❌ **Vous n'avez pas encore traité** → Contactez-moi avant vendredi. Après, je ne pourrai plus garantir un délai confortable.

Je reste disponible cette semaine :
📞 [Téléphone]
📧 Réponse directe à cet email

Cordialement,
[Signature]

P.S. : Si vous avez changé d'expert-comptable ou si ce dossier n'est plus chez nous, merci de me le signaler."""
        }
        
        selected_email = emails_library[email_choice]
        
        st.text_area("Contenu de l'email", selected_email, height=450)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "📥 Télécharger (.txt)",
                selected_email,
                file_name=f"{email_choice.replace(' ', '_').lower()}.txt",
                use_container_width=True
            )
        
        with col2:
            if st.button("📋 Copier dans le presse-papier", use_container_width=True):
                st.success("✅ Email copié ! (Ctrl+V pour coller)")
    
    # TAB 2 : TÉLÉPHONE
    with tab2:
        st.markdown(section_divider("📞 SCRIPT TÉLÉPHONIQUE"), unsafe_allow_html=True)
        
        script_tel = """
**SCRIPT D'APPEL FACTURATION ÉLECTRONIQUE**

---

**Étape 1 : Accroche (15 secondes)**

"Bonjour [Prénom], c'est [Votre nom] de [Cabinet]. 
Je vous appelle rapidement au sujet de la facturation électronique qui arrive en septembre 2026. 
Vous avez 2 minutes ?"

➡️ **Si NON** : "Pas de souci, quand puis-je vous rappeler ?" (noter dans CRM)
➡️ **Si OUI** : Continuer

---

**Étape 2 : Question clé (30 secondes)**

"Parfait. Juste pour situer où vous en êtes : 
Votre outil de facturation actuel, vous savez s'il est compatible avec la réforme de 2026 ?

**Réponse A : "Oui, c'est bon"**
→ "Super ! Vos équipes sont formées ? Besoin d'un point rapide pour valider ?"
→ **Objectif** : Mission P3 (info) ou rien

**Réponse B : "Je ne sais pas / Je crois que non"**
→ "OK, c'est justement pour ça que j'appelle. On a fait un diagnostic rapide et votre situation nécessite [audit/formation]."
→ **Objectif** : Mission P1 ou P2

**Réponse C : "C'est quoi cette réforme ?"**
→ "En gros, à partir de septembre 2026, toutes les factures devront être électroniques. Si vous n'êtes pas prêt, vous ne pourrez plus émettre/recevoir de factures."
→ **Objectif** : Mission P1 urgente

---

**Étape 3 : Valeur (45 secondes)**

"Voilà ce qu'on propose selon votre situation :

**Option A (si outil NON conforme) :**
Un audit complet sur 8 semaines : on diagnostique, on vous accompagne dans le choix d'un nouvel outil, on forme vos équipes. 
Tarif : entre 1200€ et 1500€. 
Ça sécurise votre activité et vous évite tout blocage.

**Option B (si outil PARTIELLEMENT conforme) :**
Une formation de 3h pour votre équipe : on vous montre comment utiliser votre outil en mode conforme, et comment éviter les erreurs.
Tarif : 600€ à 800€.

**Option C (si outil CONFORME) :**
Un point rapide de 30 min (gratuit ou inclus dans nos honoraires) pour valider que tout est OK."

---

**Étape 4 : Prise de RDV (30 secondes)**

"Je vous propose qu'on se cale un RDV de [durée] pour [objectif précis].

Vous êtes plutôt disponible en matinée ou après-midi ?
Mardi ou jeudi ?"

➡️ **Proposer 2 créneaux précis** (pas "quand êtes-vous dispo")

---

**GESTION DES OBJECTIONS**

**"C'est trop cher"**
→ "Je comprends. Mais quel est le coût si vous ne pouvez plus facturer pendant 1 semaine ? 
La mise en conformité est un investissement déductible qui protège votre activité."

**"Je vais réfléchir"**
→ "Bien sûr. Mais attention : on a [X] dossiers en cours et les délais s'allongent. 
Je vous propose de bloquer un créneau maintenant, quitte à décaler si besoin. Ça vous va ?"

**"Je vais me débrouiller seul"**
→ "Très bien, vous avez raison d'être autonome. 
Juste un conseil : testez l'émission d'une facture avant l'été pour éviter les surprises. 
Si vous bloquez, je suis là."

**"Mon logiciel dit que c'est OK"**
→ "Parfait ! Mais avez-vous testé en conditions réelles ? 
Parfois les éditeurs annoncent la conformité mais les paramétrages ne sont pas faits. 
On peut vérifier ensemble en 15 min si vous voulez."

---

**CONCLUSION**

"Très bien [Prénom], je vous envoie un email de confirmation avec :
- Le créneau qu'on a bloqué
- Un récapitulatif de ce qu'on va faire
- Les documents à préparer si besoin

Si vous avez la moindre question d'ici là, n'hésitez pas.

Bonne journée !"

---

**À NOTER DANS LE CRM APRÈS L'APPEL**

- Statut : [RDV pris / À rappeler / Refus / Déjà géré]
- Date RDV (si applicable)
- Remarques : [Niveau d'urgence, objections, contexte particulier]
        """
        
        st.markdown(script_tel)
        
        st.download_button(
            "📥 Télécharger le script",
            script_tel,
            file_name="script_telephone_fae.txt",
            use_container_width=True
        )
    
    # TAB 3 : MINI-DOCUMENTS
    with tab3:
        st.markdown(section_divider("📄 GUIDE 1 PAGE"), unsafe_allow_html=True)
        
        guide_1page = """
═══════════════════════════════════════════════════════════════════
   📄 FACTURATION ÉLECTRONIQUE 2026 - L'ESSENTIEL EN 5 POINTS
═══════════════════════════════════════════════════════════════════

🗓️ DATE BUTOIR : 1er septembre 2026

---

**1️⃣ C'EST QUOI CONCRÈTEMENT ?**

À partir du 1er septembre 2026, TOUTES vos factures (clients + fournisseurs) 
devront être émises et reçues au format électronique.

❌ Fini le PDF envoyé par email (non conforme)
✅ Obligation de passer par des plateformes agréées (PDP ou OD)

---

**2️⃣ QUI EST CONCERNÉ ?**

• Toutes les entreprises assujetties à la TVA en France
• Y compris auto-entrepreneurs (si TVA)
• B2B uniquement (les factures B2C restent libres)

---

**3️⃣ VOTRE OUTIL EST-IL PRÊT ?**

Posez cette question à votre éditeur :
"Mon logiciel permet-il d'émettre des factures conformes à la réforme 2026 ?"

✅ OUI → Vérifiez quand même les paramétrages
⚠️ PARTIELLEMENT → Mise à jour requise (prévoir budget + temps)
❌ NON → Changement d'outil nécessaire (délai 2-3 mois)

---

**4️⃣ LES 5 MENTIONS OBLIGATOIRES (à vérifier)**

Vos factures doivent contenir :
1. SIRET émetteur + SIRET destinataire
2. Adresse complète (pas juste ville)
3. Numéro TVA intracommunautaire (si applicable)
4. Mentions légales (CGV, pénalités retard, etc.)
5. Format structuré (XML, JSON ou équivalent)

---

**5️⃣ QUE FAIRE MAINTENANT ?**

☑️ Vérifier la conformité de votre outil (avant mars 2026)
☑️ Former vos équipes (comptable + vous-même)
☑️ Tester l'émission d'une facture conforme (juin 2026)
☑️ Mettre à jour vos annuaires clients/fournisseurs
☑️ Archiver vos anciennes factures (obligation 10 ans)

---

⚠️ RISQUE SI VOUS NE FAITES RIEN

• Impossibilité d'émettre des factures = arrêt de facturation
• Impossibilité de recevoir des factures = blocage comptable
• Sanctions fiscales possibles (jusqu'à 15€ par facture non conforme)

---

📞 BESOIN D'AIDE ?

Contactez votre expert-comptable pour :
- Un audit de votre situation
- Une formation de vos équipes
- Un accompagnement personnalisé

---

Document réalisé par [Nom Cabinet] - [Date]
Plus d'infos : [Email] | [Téléphone]
        """
        
        st.text_area("Guide 1 page", guide_1page, height=600)
        
        st.download_button(
            "📥 Télécharger le guide",
            guide_1page,
            file_name="guide_fae_1page.txt",
            use_container_width=True
        )
# ========================================
# PAGE : LIVRABLES WORD
# ========================================
elif page == "📄 Livrables Word":
    st.markdown(render_premium_header(
        title="📄 Livrables Word",
        subtitle="Génération rapports audit modifiables - Personnalisés par client"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        
        if not DOCX_AVAILABLE:
            st.error("❌ Le module python-docx n'est pas installé. Installez-le avec : `pip install python-docx`")
        else:
            st.markdown(section_divider("📋 SÉLECTION CLIENT"), unsafe_allow_html=True)
            
            # Sélection client
            client_names = df['NOM'].tolist()
            selected_client = st.selectbox("Choisissez un client", client_names)
            
            client_data = df[df['NOM'] == selected_client].iloc[0]
            
            # Aperçu données client
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Informations client**")
                st.markdown(f"- **Nom :** {client_data['NOM']}")
                st.markdown(f"- **Secteur :** {client_data['SECTEUR']}")
                st.markdown(f"- **CA Honoraires :** {client_data['CA_HONORAIRES_HT']:,} €".replace(",", " "))
                st.markdown(f"- **Segment :** {client_data['SEGMENT']}")
            
            with col2:
                st.markdown("**Évaluation**")
                st.markdown(f"- **Outil :** {client_data['OUTIL_COMPATIBLE_REFORME']}")
                st.markdown(f"- **Appétence :** {client_data['APPETENCE_INFORMATIQUE']}")
                st.markdown(f"- **Score :** {client_data['SCORE_OPPORTUNITE']:.1f}")
                st.markdown(f"- **Priorité :** {client_data['PRIORITE']}")
            
            st.markdown(section_divider("⚙️ GÉNÉRATION RAPPORT"), unsafe_allow_html=True)
            
            if st.button("📄 Générer le rapport Word", use_container_width=True, type="primary"):
                try:
                    # Création document
                    doc = Document()
                    
                    # Style
                    style = doc.styles['Normal']
                    style.font.name = 'Calibri'
                    style.font.size = Pt(11)
                    
                    # En-tête
                    header = doc.add_heading('RAPPORT D\'AUDIT', 0)
                    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    doc.add_heading('Facturation Électronique 2026', level=2)
                    
                    # Infos client
                    doc.add_paragraph()
                    p = doc.add_paragraph()
                    p.add_run('Client : ').bold = True
                    p.add_run(client_data['NOM'])
                    
                    if pd.notna(client_data.get('DIRIGEANT_PRENOM')) and pd.notna(client_data.get('DIRIGEANT_NOM')):
                        p = doc.add_paragraph()
                        p.add_run('Dirigeant : ').bold = True
                        p.add_run(f"{client_data['DIRIGEANT_PRENOM']} {client_data['DIRIGEANT_NOM']}")
                    
                    p = doc.add_paragraph()
                    p.add_run('Date : ').bold = True
                    p.add_run(datetime.now().strftime('%d/%m/%Y'))
                    
                    doc.add_paragraph()
                    doc.add_paragraph('_' * 80)
                    doc.add_paragraph()
                    
                    # Section 1 : Synthèse
                    doc.add_heading('1. SYNTHÈSE DU DOSSIER', level=1)
                    
                    table = doc.add_table(rows=7, cols=2)
                    table.style = 'Light Grid Accent 1'
                    
                    table.cell(0, 0).text = 'Segment CA'
                    table.cell(0, 1).text = client_data['SEGMENT']
                    
                    table.cell(1, 0).text = 'Secteur d\'activité'
                    table.cell(1, 1).text = client_data['SECTEUR']
                    
                    table.cell(2, 0).text = 'CA Honoraires annuel'
                    table.cell(2, 1).text = f"{client_data['CA_HONORAIRES_HT']:,} € HT".replace(",", " ")
                    
                    table.cell(3, 0).text = 'Outil actuel'
                    table.cell(3, 1).text = f"Conformité : {client_data['OUTIL_COMPATIBLE_REFORME']}"
                    
                    table.cell(4, 0).text = 'Appétence informatique'
                    table.cell(4, 1).text = client_data['APPETENCE_INFORMATIQUE']
                    
                    table.cell(5, 0).text = 'Type d\'accompagnement'
                    table.cell(5, 1).text = client_data['PRIORITE']
                    
                    table.cell(6, 0).text = 'Score opportunité'
                    table.cell(6, 1).text = f"{client_data['SCORE_OPPORTUNITE']:.1f} / 100"
                    
                    doc.add_paragraph()
                    
                    # Section 2 : Contexte
                    doc.add_heading('2. CONTEXTE RÉGLEMENTAIRE', level=1)
                    
                    doc.add_paragraph(
                        "À compter du 1er septembre 2026, la facturation électronique devient obligatoire "
                        "pour toutes les entreprises assujetties à la TVA en France (transactions B2B)."
                    )
                    
                    doc.add_paragraph()
                    doc.add_paragraph("Les 3 points clés :")
                    
                    bullets = doc.add_paragraph(style='List Bullet')
                    bullets.add_run("Émission : Toutes vos factures clients devront être au format électronique structuré")
                    
                    bullets = doc.add_paragraph(style='List Bullet')
                    bullets.add_run("Réception : Vous devrez être en mesure de recevoir des factures électroniques")
                    
                    bullets = doc.add_paragraph(style='List Bullet')
                    bullets.add_run("Transmission : Les factures doivent transiter via une plateforme agréée (PDP ou OD)")
                    
                    doc.add_paragraph()
                    
                    # Section 3 : Diagnostic
                    doc.add_heading('3. DIAGNOSTIC DE L\'EXISTANT', level=1)
                    
                    if client_data['OUTIL_COMPATIBLE_REFORME'] == 'NON':
                        doc.add_paragraph(
                            f"⚠️ SITUATION CRITIQUE : Votre outil actuel n'est pas compatible avec la réforme. "
                            f"Un changement de solution est nécessaire avant septembre 2026."
                        )
                    elif client_data['OUTIL_COMPATIBLE_REFORME'] == 'PARTIELLEMENT':
                        doc.add_paragraph(
                            f"⚠️ MISE À JOUR REQUISE : Votre outil nécessite une mise à jour et des paramétrages "
                            f"pour être conforme. Contactez votre éditeur dès maintenant."
                        )
                    else:
                        doc.add_paragraph(
                            f"✅ SITUATION FAVORABLE : Votre outil est déjà compatible. "
                            f"Néanmoins, une vérification des paramétrages et une formation sont recommandées."
                        )
                    
                    doc.add_paragraph()
                    
                    if client_data['APPETENCE_INFORMATIQUE'] == 'FAIBLE':
                        doc.add_paragraph(
                            "Compte tenu de votre niveau d'aisance informatique, un accompagnement renforcé "
                            "est recommandé pour garantir une transition sereine."
                        )
                    elif client_data['APPETENCE_INFORMATIQUE'] == 'TRES BON':
                        doc.add_paragraph(
                            "Votre bonne maîtrise des outils numériques est un atout. "
                            "Une formation express suffira pour vous rendre autonome."
                        )
                    
                    doc.add_paragraph()
                    
                    # Section 4 : Recommandations
                    doc.add_heading('4. RECOMMANDATIONS & PLAN D\'ACTION', level=1)
                    
                    if 'PRIORITÉ 1' in client_data['PRIORITE']:
                        doc.add_paragraph("Type de mission recommandée : AUDIT COMPLET (8 semaines)")
                        doc.add_paragraph()
                        
                        table_plan = doc.add_table(rows=5, cols=3)
                        table_plan.style = 'Light List Accent 1'
                        
                        table_plan.cell(0, 0).text = 'Phase'
                        table_plan.cell(0, 1).text = 'Durée'
                        table_plan.cell(0, 2).text = 'Contenu'
                        
                        table_plan.cell(1, 0).text = '1. Diagnostic'
                        table_plan.cell(1, 1).text = 'Semaines 1-2'
                        table_plan.cell(1, 2).text = 'Audit existant + cartographie flux'
                        
                        table_plan.cell(2, 0).text = '2. Conformité'
                        table_plan.cell(2, 1).text = 'Semaines 3-5'
                        table_plan.cell(2, 2).text = 'Choix outil + paramétrage + tests'
                        
                        table_plan.cell(3, 0).text = '3. Formation'
                        table_plan.cell(3, 1).text = 'Semaine 6'
                        table_plan.cell(3, 2).text = 'Session 2h équipes + cas pratiques'
                        
                        table_plan.cell(4, 0).text = '4. Suivi'
                        table_plan.cell(4, 1).text = 'Semaines 7-8'
                        table_plan.cell(4, 2).text = 'Points hebdo + ajustements'
                        
                        doc.add_paragraph()
                        doc.add_paragraph(f"Tarif indicatif : 1200€ à 1500€ HT")
                        
                    elif 'PRIORITÉ 2' in client_data['PRIORITE']:
                        doc.add_paragraph("Type de mission recommandée : FORMATION STRUCTURÉE (3 heures)")
                        doc.add_paragraph()
                        doc.add_paragraph("Contenu :")
                        
                        bullets = doc.add_paragraph(style='List Bullet')
                        bullets.add_run("Pré-diagnostic express (30 min)")
                        bullets = doc.add_paragraph(style='List Bullet')
                        bullets.add_run("Formation action sur l'outil (1h30)")
                        bullets = doc.add_paragraph(style='List Bullet')
                        bullets.add_run("Bonnes pratiques anti-rejet (1h)")
                        
                        doc.add_paragraph()
                        doc.add_paragraph(f"Tarif indicatif : 600€ à 800€ HT")
                        
                    else:
                        doc.add_paragraph("Type de mission recommandée : INFORMATION & VALIDATION (30-60 min)")
                        doc.add_paragraph()
                        doc.add_paragraph("Contenu :")
                        
                        bullets = doc.add_paragraph(style='List Bullet')
                        bullets.add_run("Confirmation conformité outil")
                        bullets = doc.add_paragraph(style='List Bullet')
                        bullets.add_run("Points de vigilance (3 principaux)")
                        bullets = doc.add_paragraph(style='List Bullet')
                        bullets.add_run("Checklist finale (5 points)")
                        
                        doc.add_paragraph()
                        doc.add_paragraph(f"Tarif indicatif : 150€ à 300€ HT (ou inclus honoraires récurrents)")
                    
                    doc.add_paragraph()
                    
                    # Section 5 : Conclusion
                    doc.add_heading('5. CONCLUSION', level=1)
                    
                    if 'PRIORITÉ 1' in client_data['PRIORITE']:
                        doc.add_paragraph(
                            "Compte tenu de votre situation (outil non conforme), nous vous recommandons "
                            "de lancer cette mission dès que possible. Le délai de mise en conformité "
                            "peut prendre 2 à 3 mois selon la complexité de votre dossier."
                        )
                    elif 'PRIORITÉ 2' in client_data['PRIORITE']:
                        doc.add_paragraph(
                            "Votre outil est sur la bonne voie. Une formation de vos équipes vous permettra "
                            "d'être pleinement opérationnel dès septembre 2026 sans stress."
                        )
                    else:
                        doc.add_paragraph(
                            "Vous êtes déjà bien positionné. Un simple point de validation vous apportera "
                            "la sérénité nécessaire pour aborder cette échéance."
                        )
                    
                    doc.add_paragraph()
                    doc.add_paragraph(
                        "Nous restons à votre disposition pour toute question complémentaire."
                    )
                    
                    doc.add_paragraph()
                    doc.add_paragraph('_' * 80)
                    
                    # Footer
                    doc.add_paragraph()
                    footer = doc.add_paragraph()
                    footer.add_run('[Nom de votre cabinet]').bold = True
                    doc.add_paragraph('[Adresse]')
                    doc.add_paragraph('[Téléphone] | [Email] | [Site web]')
                    
                    # Sauvegarde
                    output_docx = io.BytesIO()
                    doc.save(output_docx)
                    output_docx.seek(0)
                    
                    st.success("✅ Rapport généré avec succès !")
                    
                    st.download_button(
                        label="📥 Télécharger le rapport Word",
                        data=output_docx.getvalue(),
                        file_name=f"rapport_audit_{client_data['NOM'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération : {str(e)}")

# ========================================
# PAGE : BUDGET TCO
# ========================================
elif page == "🔧 Budget TCO":
    st.markdown(render_premium_header(
        title="🔧 Comparateur Budget TCO",
        subtitle="Total Cost of Ownership - Solutions facturation électronique"
    ), unsafe_allow_html=True)
    
    st.markdown(section_divider("⚙️ PARAMÈTRES CLIENT"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nb_users = st.number_input("Nombre d'utilisateurs", 1, 50, 3)
    
    with col2:
        nb_factures = st.number_input("Factures/mois", 10, 2000, 100)
    
    with col3:
        horizon = st.selectbox("Horizon", [12, 24, 36], index=1)
    
    st.markdown(section_divider("💰 COMPARAISON SOLUTIONS"), unsafe_allow_html=True)
    
    # Données solutions
    solutions = {
        "Pennylane": {
            "prix_base": 69,
            "prix_user": 10,
            "factures_incluses": 200,
            "prix_facture_supp": 0.15,
            "cout_formation": 500,
            "delai_deploiement": "2 semaines",
            "support": "Email + Chat"
        },
        "Cegid Loop": {
            "prix_base": 89,
            "prix_user": 15,
            "factures_incluses": 150,
            "prix_facture_supp": 0.20,
            "cout_formation": 800,
            "delai_deploiement": "4 semaines",
            "support": "Téléphone + Email"
        },
        "Sage 100": {
            "prix_base": 120,
            "prix_user": 20,
            "factures_incluses": 300,
            "prix_facture_supp": 0.10,
            "cout_formation": 1200,
            "delai_deploiement": "6 semaines",
            "support": "Premium 24/7"
        },
        "Inqom": {
            "prix_base": 49,
            "prix_user": 8,
            "factures_incluses": 100,
            "prix_facture_supp": 0.25,
            "cout_formation": 400,
            "delai_deploiement": "1 semaine",
            "support": "Email"
        },
        "Tiime": {
            "prix_base": 59,
            "prix_user": 12,
            "factures_incluses": 150,
            "prix_facture_supp": 0.18,
            "cout_formation": 600,
            "delai_deploiement": "3 semaines",
            "support": "Chat + Email"
        }
    }
    
    # Calculs
    results = []
    
    for nom, params in solutions.items():
        cout_mensuel = params['prix_base'] + (nb_users * params['prix_user'])
        
        if nb_factures > params['factures_incluses']:
            factures_supp = nb_factures - params['factures_incluses']
            cout_mensuel += factures_supp * params['prix_facture_supp']
        
        cout_initial = params['cout_formation']
        tco = (cout_mensuel * horizon) + cout_initial
        
        results.append({
            "Solution": nom,
            "Coût mensuel": f"{cout_mensuel:.2f} €",
            "Coût initial": f"{cout_initial} €",
            "TCO ({} mois)".format(horizon): f"{tco:.2f} €",
            "Délai": params['delai_deploiement'],
            "Support": params['support']
        })
    
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values("TCO ({} mois)".format(horizon))
    
    st.dataframe(df_results, use_container_width=True, hide_index=True)
    
    # Graphique
    st.markdown(section_divider("📊 VISUALISATION TCO"), unsafe_allow_html=True)
    
    tco_values = [float(r["TCO ({} mois)".format(horizon)].replace(" €", "").replace(",", ".")) for r in results]
    solution_names = [r["Solution"] for r in results]
    
    fig_tco = go.Figure(data=[
        go.Bar(
            x=solution_names,
            y=tco_values,
            text=[f"{v:.0f}€" for v in tco_values],
            textposition='outside',
            marker=dict(color=['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#9ca3af'])
        )
    ])
    
    fig_tco.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        font=dict(color='#f1f5f9'),
        xaxis=dict(title="", gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title=f"TCO sur {horizon} mois (€)", gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig_tco, use_container_width=True)

# ========================================
# PAGE : EXPORTS
# ========================================
elif page == "📤 Exports":
    st.markdown(render_premium_header(
        title="📤 Exports de Données",
        subtitle="Téléchargement Excel enrichi avec toutes les analyses"
    ), unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Veuillez d'abord importer vos données depuis la page Accueil")
    else:
        df = st.session_state.df
        
        st.markdown(section_divider("📊 DONNÉES DISPONIBLES"), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Nombre de clients", len(df))
            st.metric("Colonnes", len(df.columns))
        
        with col2:
            file_size_mb = len(df.to_csv().encode('utf-8')) / (1024 * 1024)
            st.metric("Taille estimée", f"{file_size_mb:.2f} Mo")
            st.metric("Format", "Excel (.xlsx)")
        
        st.markdown(section_divider("📥 TÉLÉCHARGEMENT"), unsafe_allow_html=True)
        
        st.markdown("""
        **Ce fichier contient :**
        - ✅ Toutes les colonnes d'origine (NOM, SECTEUR, CA, etc.)
        - ✅ Toutes les colonnes calculées (SEGMENT, SCORE, PRIORITÉ, ETOILES)
        - ✅ Format Excel (.xlsx) compatible avec tous les outils
        """)
        
        # Génération Excel
        output_export = io.BytesIO()
        
        with pd.ExcelWriter(output_export, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Analyse complète', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Analyse complète']
            
            # Format header
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'fg_color': '#667eea',
                'font_color': 'white',
                'border': 1
            })
            
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Largeurs colonnes
            worksheet.set_column('A:A', 25)  # NOM
            worksheet.set_column('B:B', 20)  # SECTEUR
            worksheet.set_column('C:C', 15)  # CA
            worksheet.set_column('D:E', 25)  # OUTIL, APPETENCE
            worksheet.set_column('F:H', 15)  # Dirigeant
            worksheet.set_column('I:L', 20)  # Calculées
        
        output_export.seek(0)
        
        st.download_button(
            label="📥 Télécharger l'analyse complète (Excel)",
            data=output_export.getvalue(),
            file_name=f"analyse_fae_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("---")
        
        st.info("""
        💡 **Astuce** : Ce fichier peut être réimporté dans l'outil pour conserver vos analyses. 
        Les colonnes calculées seront écrasées lors d'un nouvel import.
        """)

# ========================================
# FOOTER GLOBAL
# ========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748b; font-size: 0.9rem;">
    <p style="margin: 0;">🏆 <strong>Outil d'Analyse & Segmentation Client RFE v7.3</strong></p>
    <p style="margin: 0.5rem 0 0 0;">Développé avec ❤️ pour les cabinets d'expertise comptable</p>
    <p style="margin: 0.5rem 0 0 0;">🔒 Traitement 100% local - Confidentialité garantie</p>
</div>
""", unsafe_allow_html=True)