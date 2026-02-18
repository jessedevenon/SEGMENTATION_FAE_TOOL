"""
Style CSS premium pour ClientHub Pro
Version 7.3 - Design Portfolio Premium (OPTIMISÉ PERFORMANCES)
"""

def inject_custom_css():
    """Injecte le CSS personnalisé dans Streamlit"""
    
    css = """
    <style>
    /* ========================================
       IMPORTS FONTS PREMIUM - PRÉCHARGEMENT
    ======================================== */
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');
    
    /* ========================================
       VARIABLES COULEURS PREMIUM
    ======================================== */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gold-gradient: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        --dark-bg: #0f172a;
        --card-bg: rgba(255, 255, 255, 0.05);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --accent-gold: #fbbf24;
    }
    
    /* ========================================
       RESET & BASE
    ======================================== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Cache éléments Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ========================================
       BACKGROUND OPTIMISÉ - SANS ANIMATION
    ======================================== */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e293b 50%,
            #0f172a 100%
        );
        position: relative;
        min-height: 100vh;
    }
    
    /* Pattern géométrique statique (animation désactivée pour perf) */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 15% 25%, rgba(102, 126, 234, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 85% 75%, rgba(118, 75, 162, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        /* animation désactivée pour performances */
    }
    
    /* Lignes diagonales simplifiées */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(45deg, transparent 48%, rgba(102, 126, 234, 0.015) 49%, rgba(102, 126, 234, 0.015) 51%, transparent 52%);
        background-size: 80px 80px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.25;
    }
    
    /* Container principal - FIX Z-INDEX & ESPACEMENT */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        position: relative;
        z-index: 10;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Fix z-index pour tous les contenus */
    .stMarkdown, 
    .element-container, 
    .stButton, 
    .stMetric, 
    .stDataFrame, 
    .stPlotlyChart, 
    .stExpander, 
    .stTabs,
    .stSelectbox,
    .stMultiSelect,
    .stFileUploader,
    .stDownloadButton,
    .stTextInput,
    .stNumberInput,
    .stSlider,
    .stRadio,
    .stCheckbox,
    div[data-testid="stVerticalBlock"], 
    div[data-testid="column"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="metric-container"] {
        position: relative;
        z-index: 15;
    }
    
    /* Force contenu principal au-dessus */
    .main > div,
    .main .block-container > div {
        position: relative;
        z-index: 15 !important;
    }
    
    /* ========================================
       HEADER PREMIUM - FIX OVERLAP
    ======================================== */
    .premium-header {
        background: var(--primary-gradient);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        z-index: 50;
        clear: both;
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
        border-radius: 50%;
        z-index: -1;
    }
    
    .premium-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: white !important;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .premium-header p {
        font-size: 1rem;
        color: rgba(255,255,255,0.9) !important;
        margin-top: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .premium-header .subtitle {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 0.8rem;
        backdrop-filter: blur(5px);
        position: relative;
        z-index: 2;
        color: white !important;
    }
    
    /* ========================================
       MÉTRIQUES PREMIUM - OPTIMISÉES
    ======================================== */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: var(--gold-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
    
    /* Container métriques - BLUR RÉDUIT */
    div[data-testid="metric-container"] {
        background: var(--glass-bg);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* ========================================
       SIDEBAR PREMIUM - FIX LISIBILITÉ
    ======================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(15, 23, 42, 0.98) 0%, 
            rgba(30, 41, 59, 0.98) 100%
        ) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
        background: transparent !important;
    }
    
    /* Logo sidebar */
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-logo h2 {
        color: #f1f5f9 !important;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
    }
    
    .sidebar-logo p {
        color: #94a3b8 !important;
        font-size: 0.85rem;
        margin: 0;
    }
    
    /* Navigation sidebar - TEXTE BLANC */
    section[data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 0.5rem;
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        color: #f1f5f9 !important;
        transition: all 0.2s ease;
        cursor: pointer;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: var(--primary-gradient) !important;
        border-color: transparent !important;
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: var(--primary-gradient) !important;
        border-color: transparent !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        color: white !important;
    }
    
    /* Texte sidebar général */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #f1f5f9 !important;
    }
    
    /* ========================================
       
    
    /* ========================================
       GRAPHIQUES & CHARTS - OPTIMISÉS
    ======================================== */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        background: var(--glass-bg);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* ========================================
       EXPANDERS PREMIUM - BLEU CLAIR FORCÉ
    ======================================== */
    
    /* Header expander - BLEU CLAIR */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border: 2px solid #60a5fa !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        color: #000000 !important;
        font-weight: 700 !important;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(96, 165, 250, 0.2);
    }
    
    /* Texte dans le header - NOIR FORCÉ */
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader div,
    .streamlit-expanderHeader span {
        color: #000000 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transform: translateY(-1px);
    }
    
    /* Contenu expander - BLEU TRÈS CLAIR */
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        border: 2px solid #93c5fd !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1.5rem !important;
    }
    
    /* TOUS les textes du contenu en NOIR */
    .streamlit-expanderContent,
    .streamlit-expanderContent *,
    .streamlit-expanderContent p,
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent li,
    .streamlit-expanderContent td {
        color: #1e293b !important;
    }
    
    .streamlit-expanderContent h1,
    .streamlit-expanderContent h2,
    .streamlit-expanderContent h3,
    .streamlit-expanderContent h4 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    .streamlit-expanderContent strong,
    .streamlit-expanderContent b {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Markdown dans expander - NOIR */
    .streamlit-expanderContent .stMarkdown,
    .streamlit-expanderContent .stMarkdown *,
    .streamlit-expanderContent .stMarkdown p,
    .streamlit-expanderContent .stMarkdown li {
        color: #1e293b !important;
    }
    
    /* Colonnes dans expander - NOIR */
    .streamlit-expanderContent [data-testid="column"],
    .streamlit-expanderContent [data-testid="column"] *,
    .streamlit-expanderContent [data-testid="column"] p,
    .streamlit-expanderContent [data-testid="column"] div {
        color: #1e293b !important;
    }
    
    .streamlit-expanderContent [data-testid="column"] strong {
        color: #000000 !important;
    }
    
    /* Icônes */
    .streamlit-expanderHeader svg {
        color: #3b82f6 !important;
    }
       TABLES / DATAFRAMES
    ======================================== */
    .dataframe {
        background: transparent !important;
        border: none !important;
    }
    
    .dataframe thead tr {
        background: var(--primary-gradient) !important;
    }
    
    .dataframe th {
        background: transparent !important;
        color: white !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
        letter-spacing: 0.5px;
        padding: 1rem !important;
        border: none !important;
    }
    
    .dataframe tbody {
        background: var(--glass-bg) !important;
    }
    
    .dataframe td {
        padding: 0.875rem 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: var(--text-primary) !important;
        border-left: none !important;
        border-right: none !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(102, 126, 234, 0.1) !important;
    }
    
    .dataframe tr:first-child td {
        border-top: none !important;
    }
    
    /* Container dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* ========================================
       INPUTS & SELECTS - TEXTE BLANC
    ======================================== */
    .stSelectbox label, .stMultiSelect label, .stTextInput label, 
    .stNumberInput label, .stSlider label, .stTextArea label {
        color: #f1f5f9 !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--glass-bg) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        backdrop-filter: blur(5px);
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: var(--glass-bg);
    }
    
    .stSlider > div > div > div > div {
        background: var(--primary-gradient) !important;
    }
    
    /* ========================================
       SELECTBOX DROPDOWN - OPTIONS BLANCHES
    ======================================== */
    
    /* Menu déroulant */
    div[data-baseweb="select"] ul {
        background: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    div[data-baseweb="select"] li {
        color: #f1f5f9 !important;
        background: transparent !important;
        padding: 0.75rem 1rem;
    }
    
    div[data-baseweb="select"] li:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        color: white !important;
    }
    
    /* Texte sélectionné */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #f1f5f9 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] span {
        color: #f1f5f9 !important;
    }
    
    /* Options menu (alternative selector) */
    [role="listbox"] {
        background: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
    }
    
    [role="option"] {
        color: #f1f5f9 !important;
        background: transparent !important;
        padding: 0.75rem 1rem;
    }
    
    [role="option"]:hover {
        background: rgba(102, 126, 234, 0.2) !important;
    }
    
    [aria-selected="true"][role="option"] {
        background: rgba(102, 126, 234, 0.3) !important;
        color: white !important;
        font-weight: 600;
    }
    
    /* ========================================
       TEXT AREA - TEXTE BLANC
    ======================================== */
    .stTextArea textarea {
        background: var(--glass-bg) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        backdrop-filter: blur(5px);
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem;
        line-height: 1.6;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3);
        outline: none;
    }    /* ========================================
       BOUTONS - TRANSITIONS RAPIDES
    ======================================== */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Bouton primary */
    .stButton > button[kind="primary"] {
        background: var(--primary-gradient);
    }
    
    /* Bouton download */
    .stDownloadButton > button {
        background: var(--gold-gradient);
        color: #0f172a;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(251, 191, 36, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(251, 191, 36, 0.5);
    }
    
    /* ========================================
       TABS
    ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--glass-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        color: var(--text-primary);
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        border-color: transparent !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* ========================================
       DIVIDERS
    ======================================== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.1) 50%, 
            transparent 100%
        );
        margin: 2rem 0;
    }
    
    /* ========================================
       ALERTES / MESSAGES
    ======================================== */
    .stAlert {
        background: var(--glass-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        backdrop-filter: blur(5px);
        color: #f1f5f9 !important;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
        color: #d1fae5 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        border-color: rgba(245, 158, 11, 0.3);
        color: #fef3c7 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border-color: rgba(239, 68, 68, 0.3);
        color: #fee2e2 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.3);
        color: #dbeafe !important;
    }
    
   /* ========================================
       BOÎTES COLORÉES - CONTRASTE AMÉLIORÉ
    ======================================== */
    div[style*="background: linear-gradient(135deg, #fef3c7"] {
        position: relative;
        z-index: 20 !important;
    }
    
    div[style*="background: rgba(102, 126, 234, 0.05)"] {
        position: relative;
        z-index: 20 !important;
    }
    
    /* Override direct pour bloc jaune conseil */
    div[style*="#fef3c7"] h4,
    div[style*="#fde68a"] h4,
    div[style*="#78350f"] h4 {
        color: #78350f !important;
    }
    
    div[style*="#fef3c7"] p,
    div[style*="#fde68a"] p,
    div[style*="#78350f"] p {
        color: #92400e !important;
    }
    
    /* ========================================
       ANIMATIONS SIMPLIFIÉES
    ======================================== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* ========================================
       SCROLLBAR CUSTOM
    ======================================== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark-bg);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
        border: 2px solid var(--dark-bg);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* ========================================
       TOOLTIPS
    ======================================== */
    [data-testid="stTooltipIcon"] {
        color: var(--accent-gold);
    }
    
    /* ========================================
       RESPONSIVE
    ======================================== */
    @media (max-width: 768px) {
        .premium-header h1 {
            font-size: 1.8rem;
        }
        
        .premium-header p {
            font-size: 0.9rem;
        }
        
        div[data-testid="metric-container"] {
            padding: 1rem !important;
        }
        
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
        }
    }
    
    /* ========================================
       SECTION HEADERS - TEXTES LISIBLES
    ======================================== */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #f1f5f9 !important;
    }
    
    h2 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.875rem;
        color: #f1f5f9 !important;
    }
    
    h3 {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: #f1f5f9 !important;
    }
    
    h4 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        margin-bottom: 0.5rem;
    }
    
    /* Paragraphes et listes - GRIS CLAIR */
    p {
        color: #cbd5e1 !important;
        line-height: 1.6;
    }
    
    li {
        color: #cbd5e1 !important;
        line-height: 1.6;
    }
    
    /* Markdown général - BLANC */
    .stMarkdown {
        color: #f1f5f9 !important;
    }
    
    .stMarkdown p {
        color: #cbd5e1 !important;
    }
    
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4 {
        color: #f1f5f9 !important;
    }
    
    .stMarkdown ul li,
    .stMarkdown ol li {
        color: #cbd5e1 !important;
    }
    
    .stMarkdown strong,
    .stMarkdown b {
        color: #f1f5f9 !important;
        font-weight: 700;
    }
    
    /* Éléments en ligne */
    strong, b {
        color: #f1f5f9 !important;
    }
    
    em, i {
        color: #cbd5e1 !important;
    }
    
    /* Links - BLEU CLAIR */
    a {
        color: #60a5fa !important;
        text-decoration: none;
        transition: color 0.2s;
    }
    
    a:hover {
        color: #93c5fd !important;
        text-decoration: underline;
    }
    
    /* Code inline */
    code {
        background: rgba(255, 255, 255, 0.1);
        color: #fbbf24;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    
    /* Blockquote */
    blockquote {
        border-left: 3px solid #667eea;
        padding-left: 1rem;
        color: #cbd5e1 !important;
        font-style: italic;
    }
    
    /* ========================================
       UPLOAD WIDGET - COMPACT CENTRÉ BLEU
    ======================================== */
    .stFileUploader {
        max-width: 600px !important;
        margin: 2rem auto !important;
        border: 3px dashed #60a5fa;
        border-radius: 20px;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(96, 165, 250, 0.2);
    }
    
    .stFileUploader:hover {
        border-color: #3b82f6;
        background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    
    /* Container principal upload */
    div[data-testid="stFileUploadDropzone"] {
        max-width: 600px !important;
        margin: 0 auto !important;
    }
    
    /* Label principal - NOIR */
    .stFileUploader label {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-align: center;
        display: block;
        margin-bottom: 1rem;
    }
    
    /* Texte "Glissez-déposez..." - NOIR */
    .stFileUploader [data-testid="stFileUploaderLabel"] {
        color: #1e293b !important;
        font-weight: 600 !important;
        text-align: center;
    }
    
    .stFileUploader p {
        color: #334155 !important;
        font-weight: 500;
        text-align: center;
        font-size: 0.95rem;
    }
    
    /* Zone de drop - NOIR */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        color: #1e293b !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] div {
        color: #334155 !important;
    }
    
    /* Tous les textes dans upload - NOIR */
    .stFileUploader div {
        color: #334155 !important;
    }
    
    .stFileUploader span {
        color: #334155 !important;
    }
    
    /* Texte instructions upload */
    .stFileUploader small {
        color: #475569 !important;
        text-align: center;
        display: block;
        margin-top: 0.5rem;
    }
    
    /* Bouton browse files - TEXTE NOIR */
    .stFileUploader button {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border: 2px solid #3b82f6 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin: 1rem auto 0 auto !important;
        display: block !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.2s ease;
    }
    
    .stFileUploader button:hover {
        transform: translateY(-2px);
        background: #ffffff !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        border-color: #2563eb !important;
    }
    
    /* Force texte noir dans le bouton */
    .stFileUploader button span {
        color: #000000 !important;
    }
    }
    
    .stFileUploader button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Icône upload centrée */
    .stFileUploader svg {
        display: block;
        margin: 0 auto 1rem auto;
        color: #3b82f6 !important;
    }
    
    /* ========================================
       FORCE BLOC JAUNE - OVERRIDE TOTAL
    ======================================== */
    div[style*="color: #78350f"] {
        color: #000000 !important;
    }
    
    div[style*="color: #78350f"] * {
        color: #000000 !important;
    }
    
    div[style*="border: 2px solid #f59e0b"] h4 {
        color: #000000 !important;
    }
    
    div[style*="border: 2px solid #f59e0b"] p {
        color: #000000 !important;
    }
    /* ========================================
       OVERRIDE EXPANDERS - FORCE ABSOLUE
    ======================================== */
    
    details summary {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border: 2px solid #60a5fa !important;
        color: #000000 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
    }
    
    details summary * {
        color: #000000 !important;
    }
    
    details[open] > div:last-child {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        border: 2px solid #93c5fd !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1.5rem !important;
    }
    
    details[open] > div:last-child * {
        color: #1e293b !important;
    }
    
    details[open] > div:last-child h1,
    details[open] > div:last-child h2,
    details[open] > div:last-child h3,
    details[open] > div:last-child h4,
    details[open] > div:last-child strong {
        color: #000000 !important;
    }

    </style>
    """
    
    return css


def render_premium_header(title, subtitle, badge=None):
    """Render un header premium avec titre, sous-titre et badge optionnel"""
    
    badge_html = ""
    if badge:
        badge_html = f'<div class="subtitle">{badge}</div>'
    
    html = f"""
    <div class="premium-header animate-in">
        <h1>{title}</h1>
        <p>{subtitle}</p>
        {badge_html}
    </div>
    """
    
    return html


def metric_card_html(icon, label, value, delta=None):
    """Génère HTML pour une métrique custom avec icône"""
    
    delta_html = ""
    if delta:
        delta_color = "#10b981" if "+" in str(delta) else "#ef4444"
        delta_arrow = "↑" if "+" in str(delta) else "↓"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.95rem; margin-top: 0.5rem; font-weight: 600;">{delta_arrow} {delta}</div>'
    
    html = f"""
    <div style="
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
        height: 100%;
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 48px rgba(102, 126, 234, 0.3)'" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.2)'">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">{icon}</div>
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                {label}
            </div>
        </div>
        <div style="font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {value}
        </div>
        {delta_html}
    </div>
    """
    
    return html


def section_divider(text=""):
    """Crée un séparateur de section stylé"""
    
    if text:
        html = f"""
        <div style="display: flex; align-items: center; margin: 3rem 0 2rem 0;">
            <div style="flex: 1; height: 1px; background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%);"></div>
            <div style="padding: 0 2rem; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">
                {text}
            </div>
            <div style="flex: 1; height: 1px; background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%);"></div>
        </div>
        """
    else:
        html = '<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%); margin: 2rem 0;">'
    
    return html