import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter
import zipfile
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="DerMind Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = "data"
ZIP_PATH = os.path.join(DATA_DIR, "dataset.zip")

def extract_if_needed():
    required_files = [
        "master_mental_health_clean.csv",
        "HAM10000_clean.csv", 
        "healthy_lifestyle_city_2021_cleaned.csv",
        "master_sephora.csv",
        "master_skin_image_manifest.csv"
    ]
    
    all_exist = all(os.path.exists(os.path.join(DATA_DIR, f)) for f in required_files)
    
    if not all_exist:
        if os.path.exists(ZIP_PATH):
            with st.spinner("📦 Mengekstrak dataset... (hanya sekali)"):
                with zipfile.ZipFile(ZIP_PATH, "r") as z:
                    z.extractall(DATA_DIR)
            st.toast("✅ Dataset berhasil diekstrak!", icon="🎉")
        else:
            st.error(f"❌ File tidak ditemukan: {ZIP_PATH}\n\n"
                     f"Pastikan file `dataset.zip` ada di folder `data/`")
            st.stop()

extract_if_needed()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Main background putih */
.stApp { background: #F8FAF9; color: #1A2E1A; }
.block-container { padding: 1.5rem 2rem 3rem; }

/* ── SIDEBAR gelap seperti screenshot ── */
[data-testid="stSidebar"] {
    background: #1A1A2E !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #94A3B8 !important; font-size:0.78rem !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div {
    background: #16213E !important;
    border: 1px solid #2D5016 !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    color: #E2E8F0 !important;
}

/* Metric cards hijau */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #D1FAE5;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 10px rgba(16,185,129,0.08);
}
[data-testid="stMetricLabel"] { color: #6B7280 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { color: #059669 !important; font-size: 1.7rem !important; font-weight: 700; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; color: #10B981 !important; }

/* Headers */
h1 { color: #065F46 !important; font-weight: 700 !important; }
h2 { color: #064E3B !important; font-weight: 600 !important; border-bottom: 2px solid #D1FAE5; padding-bottom: 0.5rem; }
h3 { color: #047857 !important; }

/* PB card */
.pb-card {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border-left: 4px solid #059669;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(5,150,105,0.1);
}
.pb-card h3 { color: #065F46 !important; margin: 0 0 0.25rem; font-size: 1rem; }
.pb-card p  { color: #374151; margin: 0; font-size: 0.9rem; }

/* Insight box */
.insight {
    background: #ECFDF5;
    border: 1px solid #6EE7B7;
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #1F2937;
    line-height: 1.6;
}
.insight strong { color: #065F46; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: #F0FDF4;
    border-radius: 8px;
    color: #374151;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    border: 1px solid #D1FAE5;
}
.stTabs [aria-selected="true"] {
    background: #059669 !important;
    color: #FFFFFF !important;
    font-weight: 600;
    border-color: #059669 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }

/* Expander */
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #D1FAE5 !important;
    border-radius: 12px !important;
    margin-bottom: 0.6rem;
}
[data-testid="stExpander"] summary {
    font-weight: 600;
    color: #065F46 !important;
    padding: 0.8rem 1rem;
}
[data-testid="stExpander"] summary:hover { background: #F0FDF4; border-radius: 12px; }

/* Divider */
hr { border-color: #D1FAE5 !important; margin: 1rem 0; }

/* Selectbox main */
.stSelectbox > div { background: #FFFFFF; border-radius: 8px; border-color: #D1FAE5; }

/* Footer */
.footer { color: #9CA3AF; font-size: 0.75rem; text-align: center; padding-top: 2rem; }

/* Banner hero */
.hero-banner {
    background: linear-gradient(135deg, #065F46 0%, #047857 50%, #059669 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
}
.hero-banner h1 { color: white !important; font-size: 1.8rem; margin: 0 0 0.5rem; }
.hero-banner p  { color: #A7F3D0; margin: 0; font-size: 0.9rem; }

/* KPI card hijau */
.kpi-card {
    background: white;
    border: 1px solid #D1FAE5;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(5,150,105,0.07);
}
.kpi-card .kpi-val { color: #059669; font-size: 1.6rem; font-weight: 700; }
.kpi-card .kpi-lbl { color: #6B7280; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-card .kpi-sub { color: #10B981; font-size: 0.8rem; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

G1  = "#059669"
G2  = "#10B981"
G3  = "#34D399"
G4  = "#6EE7B7"
BG  = "#F8FAF9"
CA  = "#FFFFFF"
TX  = "#1F2937"
R   = "#EF4444"
Y   = "#F59E0B"
BL  = "#3B82F6"
P   = "#8B5CF6"
CY  = "#06B6D4"
PAL = [G1, "#0D9488", BL, Y, R, P, CY, "#F97316", "#EC4899", "#84CC16", G3, G4]

def darkfig():
    plt.rcParams.update({
        "figure.facecolor": CA, "axes.facecolor": "#F0FDF4",
        "axes.edgecolor": "#D1FAE5", "axes.labelcolor": TX,
        "xtick.color": TX, "ytick.color": TX,
        "text.color": TX, "grid.color": "#D1FAE5",
        "legend.facecolor": CA, "legend.edgecolor": "#D1FAE5",
        "legend.labelcolor": TX, "figure.dpi": 130,
    })

@st.cache_data(show_spinner=False)
def load():
    mh   = pd.read_csv(os.path.join(DATA_DIR, "data/master_mental_health_clean.csv"))
    skin = pd.read_csv(os.path.join(DATA_DIR, "data/master_skin_image_manifest.csv"))
    ham  = pd.read_csv(os.path.join(DATA_DIR, "data/HAM10000_clean.csv"))
    sep  = pd.read_csv(os.path.join(DATA_DIR, "data/master_sephora.csv"), low_memory=False)
    life = pd.read_csv(os.path.join(DATA_DIR, "data/healthy_lifestyle_city_2021_cleaned.csv"))
    life.columns = ["city","rank","sunshine_hours","water_cost","obesity_levels",
                    "life_expectancy","pollution_index","hours_worked",
                    "happiness","outdoor_activities","takeout_places","gym_cost"]
    for col in ["sunshine_hours","pollution_index","hours_worked"]:
        life[col] = pd.to_numeric(life[col], errors="coerce")
    DX = {"nv":"Melanocytic Nevi","mel":"Melanoma","bkl":"Benign Keratosis",
          "bcc":"Basal Cell Carcinoma","akiec":"Actinic Keratosis",
          "vasc":"Vascular Lesions","df":"Dermatofibroma"}
    ham["dx_full"] = ham["dx"].map(DX)
    ham["age_group"] = pd.cut(ham["age"], bins=[0,20,40,60,85],
                               labels=["0-20","21-40","41-60","61-85"])
    return mh, skin, ham, sep, life

with st.spinner("🔄 Memuat dataset DerMind..."):
    mh, skin, ham, sep, life = load()

STOPWORDS = set(["i","the","a","and","to","of","is","in","it","my","that","for","me","was","on",
    "are","have","been","with","at","this","but","not","they","so","if","do","be","we","an","or",
    "as","he","she","his","her","their","you","your","from","all","had","when","what","there",
    "were","about","him","can","just","would","will","one","out","up","no","by","like","get",
    "got","its","also","more","than","then","into","some","which","who","how","very","still",
    "even","after","before","could","should","because","am","has","does","did","other","being",
    "those","these","them","such","through","where","much","too","only","know","think","feel",
    "want","need","make","see","go","going","really","time","every","people","life","say","said"])

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.2rem 0 0.8rem;">
        <div style="font-size:2.5rem;">🏥</div>
        <div style="color:#10B981;font-size:1.3rem;font-weight:700;margin:0.3rem 0 0.1rem;">DerMind</div>
        <div style="color:#64748B;font-size:0.75rem;">Platform Kesehatan Digital AI</div>
        <div style="color:#475569;font-size:0.72rem;margin-top:0.2rem;">Capstone Project : CC26-PSU382</div>
    </div>
    <hr style="border-color:#2D3748;margin:0.5rem 0 1rem;">
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#94A3B8;font-size:0.78rem;font-weight:600;margin-bottom:0.4rem;'>📌 Navigasi Halaman</p>", unsafe_allow_html=True)

    page = st.selectbox("", [
        "🏠  Overview",
        "🧠  PB1 — Dominasi Kondisi Mental",
        "📝  PB2 — Pola Teks Mental Health",
        "🧴  PB3 — Distribusi Penyakit Kulit",
        "👤  PB4 — Demografis & Kulit",
        "💄  PB5 — Sentimen Skincare",
        "🌍  PB6 — Gaya Hidup & Kesehatan",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2D3748;margin:1rem 0 0.8rem;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.76rem;color:#64748B;line-height:2.1;">
    <span style="color:#94A3B8;font-weight:600;font-size:0.72rem;">DATASET</span><br>
    🧠 Mental Health &nbsp;<span style="color:#10B981;font-weight:600;">{len(mh):,}</span><br>
    🧴 Skin Manifest &nbsp;<span style="color:#10B981;font-weight:600;">{len(skin):,}</span><br>
    🔬 HAM10000 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#10B981;font-weight:600;">{len(ham):,}</span><br>
    💄 Sephora &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#10B981;font-weight:600;">{len(sep):,}</span><br>
    🌍 Lifestyle &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#10B981;font-weight:600;">{len(life)} kota</span>
    </div>
    """, unsafe_allow_html=True)

if "Overview" in page:
    st.markdown("""
    <div class="hero-banner">
        <h1>🏥 Platform Kesehatan Digital Berbasis AI</h1>
        <p>Deteksi Mental Health &bull; Analisis Kondisi Kulit &bull; Dashboard Kesehatan</p>
        <p style="margin-top:0.4rem;font-size:0.82rem;">Capstone Project : CC26-PSU382 &nbsp;|&nbsp; DerMind &nbsp;|&nbsp; DerMind Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, icon, val, lbl, sub in [
        (c1,"🧠", f"{len(mh):,}", "Mental Health Records", "7 kondisi"),
        (c2,"🧴", f"{len(skin):,}", "Skin Image Manifest",  "3 sumber"),
        (c3,"💄", f"{len(sep):,}", "Ulasan Skincare",       "Sephora dataset"),
        (c4,"🌍", f"{len(life)}",  "Kota Lifestyle",        "44 kota dunia"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
            <div style="font-size:1.8rem;">{icon}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-lbl">{lbl}</div>
            <div class="kpi-sub">↑ {sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#059669,#0D9488);border-radius:14px;
                padding:1rem 1.5rem;margin-bottom:1.2rem;">
        <span style="color:white;font-weight:700;font-size:1rem;">🎯 Fitur Platform Kesehatan Digital</span>
    </div>
    """, unsafe_allow_html=True)

    fa, fb = st.columns(2)
    fa.markdown("""
    <div style="background:white;border:1px solid #D1FAE5;border-radius:14px;padding:1.2rem;height:100%;">
        <div style="color:#059669;font-weight:700;margin-bottom:0.8rem;font-size:0.95rem;">🤖 2 Fitur AI Utama</div>
        <div style="color:#374151;font-size:0.88rem;line-height:2.1;">
            🧠 <b>AI Mental Health Chatbot</b><br>
            &nbsp;&nbsp;&nbsp;→ Klasifikasi kondisi dari teks pengguna<br>
            🧴 <b>AI Skin Detection</b><br>
            &nbsp;&nbsp;&nbsp;→ Deteksi kondisi kulit dari gambar kamera
        </div>
    </div>
    """, unsafe_allow_html=True)
    fb.markdown("""
    <div style="background:white;border:1px solid #D1FAE5;border-radius:14px;padding:1.2rem;height:100%;">
        <div style="color:#047857;font-weight:700;margin-bottom:0.8rem;font-size:0.95rem;">📄 Fitur Konten Pendukung</div>
        <div style="color:#374151;font-size:0.88rem;line-height:2.1;">
            📰 Artikel Kesehatan &amp; Skincare<br>
            💬 Komunitas Diskusi<br>
            🎪 Event &amp; Berita Kesehatan<br>
            👤 Profil User &nbsp;|&nbsp; ⚙️ Admin Panel
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#059669,#0D9488);border-radius:14px;
                padding:1rem 1.5rem;margin-bottom:1rem;">
        <span style="color:white;font-weight:700;font-size:1rem;">📌 6 Pertanyaan Bisnis — Klik untuk Detail</span>
    </div>
    """, unsafe_allow_html=True)

    pbs = [
        ("🧠","PB1","Kondisi mental health apa yang paling dominan berdasarkan data teks pengguna?",
         "Normal + Depression = 60% data (16.127 + 15.468 records).",
         "Imbalance ratio 18:1 → wajib class_weight='balanced' atau SMOTE.",
         "AI Mental Health Chatbot","#ECFDF5","#059669"),

        ("📝","PB2","Apakah pola teks dapat membedakan kondisi mental health secara signifikan?",
         "YA — Normal median 10 kata vs Bipolar median 143 kata. Setiap kondisi punya kata kunci khas.",
         "Gunakan TF-IDF + word_count sebagai fitur numerik tambahan untuk model.",
         "AI Mental Health Chatbot","#F0FDF4","#047857"),

        ("🧴","PB3","Kondisi kulit apa yang paling umum ditemukan dalam dataset?",
         "Psoriasis (8.6%) dan Seborrheic Keratoses (8.5%) paling dominan dari 20.015 gambar.",
         "Kelas HAM10000 Vascular Lesions & Dermatofibroma perlu augmentasi (<500 gambar).",
         "AI Skin Detection","#ECFDF5","#059669"),

        ("👤","PB4","Apakah usia & lokasi tubuh berkorelasi dengan jenis kondisi kulit?",
         "YA — Basal Cell Carcinoma & Actinic Keratosis dominan pada usia 61-85 tahun (avg 66-67 th).",
         "Usia, lokasi tubuh, dan gender harus menjadi fitur tambahan model selain gambar.",
         "AI Skin Detection","#F0FDF4","#047857"),

        ("💄","PB5","Produk skincare apa yang paling direkomendasikan berdasarkan sentimen?",
         "Treatments (82.9%) dan High Tech Tools (81.9%) paling positif. Rating 5⭐ = 63% ulasan.",
         "Basis konten artikel skincare DerMind — rekomendasi produk per tipe kulit.",
         "Konten Artikel","#ECFDF5","#059669"),

        ("🌍","PB6","Faktor gaya hidup apa yang paling mempengaruhi kesehatan & kebahagiaan?",
         "Outdoor activities & sunshine hours berkorelasi positif. Obesitas & polusi berkorelasi negatif.",
         "Kota terbaik: Amsterdam, Copenhagen, Helsinki — polusi rendah + outdoor activities tinggi.",
         "Konten Artikel","#F0FDF4","#047857"),
    ]

    for ico, pb, q, ans, impl, feat, bg, accent in pbs:
        with st.expander(f"{ico}  {pb} — {q}"):
            st.markdown(f"""
            <div style="background:{bg};border-radius:10px;padding:1rem 1.2rem;">
                <div style="margin-bottom:0.6rem;">
                    <span style="color:#6B7280;font-size:0.8rem;font-weight:600;">✅ JAWABAN</span><br>
                    <span style="color:#1F2937;font-size:0.92rem;">{ans}</span>
                </div>
                <div style="margin-bottom:0.6rem;">
                    <span style="color:#6B7280;font-size:0.8rem;font-weight:600;">💡 IMPLIKASI MODEL</span><br>
                    <span style="color:#374151;font-size:0.9rem;">{impl}</span>
                </div>
                <div>
                    <span style="background:{accent};color:white;font-size:0.75rem;font-weight:600;
                                 padding:0.25rem 0.7rem;border-radius:20px;">🎯 {feat}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif "PB1" in page:
    st.title("🧠  PB1 — Dominasi Kondisi Mental Health")
    st.markdown("""<div class="pb-card"><h3>❓ Pertanyaan Bisnis 1</h3>
    <p>Kondisi mental health apa yang paling dominan berdasarkan data teks pengguna?</p></div>""",
    unsafe_allow_html=True)

    vc = mh["label"].value_counts()
    tot = len(mh)
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Teks", f"{tot:,}")
    k2.metric("Jumlah Kondisi", str(mh["label"].nunique()))
    k3.metric("Kondisi Dominan", vc.index[0], f"{vc.values[0]/tot*100:.1f}%")
    k4.metric("Imbalance Ratio", f"{vc.max()/vc.min():.1f}x")
    st.markdown("<hr>", unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["📊 Distribusi Label","📈 Imbalance Analysis","🔍 Per Sumber Data"])

    with t1:
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        bars = axes[0].barh(vc.index, vc.values, color=PAL[:len(vc)], edgecolor="none", height=0.6)
        for bar,val in zip(bars, vc.values):
            axes[0].text(bar.get_width()+100, bar.get_y()+bar.get_height()/2,
                f"{val:,}  ({val/tot*100:.1f}%)", va="center", fontsize=9, color=TX)
        axes[0].invert_yaxis()
        axes[0].set_title("Jumlah Teks per Kondisi", color=TX, fontweight="bold")
        axes[0].set_xlabel("Jumlah Data", color=TX)
        axes[0].grid(axis="x", alpha=0.4)
        w,t2_,at = axes[1].pie(vc.values, labels=vc.index, autopct="%1.1f%%",
            colors=PAL[:len(vc)], startangle=90, pctdistance=0.82,
            wedgeprops={"edgecolor":"white","linewidth":2,"width":0.55})
        for x in t2_+at: x.set_color(TX); x.set_fontsize(9)
        axes[1].set_title("Proporsi Label (Donut)", color=TX, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t2:
        darkfig()
        ratios = vc.max()/vc
        barcol = [G1 if r<=2 else Y if r<=5 else R for r in ratios.values]
        fig, ax = plt.subplots(figsize=(10,5))
        bars2 = ax.barh(ratios.index, ratios.values, color=barcol, edgecolor="none", height=0.55)
        for bar,val in zip(bars2, ratios.values):
            ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
                f"{val:.1f}x", va="center", fontsize=10, color=TX)
        patches = [mpatches.Patch(color=G1,label="≤2x (seimbang)"),
                   mpatches.Patch(color=Y,label="≤5x (perhatian)"),
                   mpatches.Patch(color=R,label=">5x (kritis)")]
        ax.legend(handles=patches, fontsize=9)
        ax.set_title("Rasio Imbalance per Kelas", color=TX, fontweight="bold")
        ax.set_xlabel("Rasio", color=TX)
        ax.invert_yaxis(); ax.grid(axis="x", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t3:
        darkfig()
        srcs = mh["source"].unique()
        fig, axes = plt.subplots(1, len(srcs), figsize=(13,5))
        if len(srcs)==1: axes=[axes]
        for ax,src in zip(axes, srcs):
            sub = mh[mh["source"]==src]["label"].value_counts()
            ax.bar(sub.index, sub.values, color=PAL[:len(sub)], edgecolor="none", width=0.7)
            ax.set_title(f"{src.upper()}  (n={len(mh[mh['source']==src]):,})",
                color=TX, fontweight="bold")
            ax.set_ylabel("Jumlah", color=TX)
            ax.tick_params(axis="x", rotation=30)
            ax.grid(axis="y", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    st.markdown("""<div class="insight">
    ✅ <strong>Jawaban PB1:</strong> Kondisi paling dominan adalah <strong>Normal (30.6%)</strong>
    dan <strong>Depression (29.2%)</strong> — bersama menyumbang ~60% data. Mayoritas pengguna
    platform akan mencari bantuan terkait depresi. <strong>Personality Disorder (1.7%)</strong>
    adalah kelas paling minor — imbalance ratio 18x, model AI wajib menggunakan
    <code>class_weight='balanced'</code> atau teknik SMOTE.
    </div>""", unsafe_allow_html=True)

elif "PB2" in page:
    st.title("📝  PB2 — Pola Teks sebagai Pembeda Kondisi Mental Health")
    st.markdown("""<div class="pb-card"><h3>❓ Pertanyaan Bisnis 2</h3>
    <p>Apakah pola teks (panjang, kata kunci) dapat membedakan kondisi mental health secara signifikan?</p>
    </div>""", unsafe_allow_html=True)

    lbl_order = mh.groupby("label")["word_count"].median().sort_values().index.tolist()
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Median Normal",     f"{mh[mh.label=='Normal']['word_count'].median():.0f} kata")
    k2.metric("Median Bipolar",    f"{mh[mh.label=='Bipolar']['word_count'].median():.0f} kata")
    k3.metric("Median Depression", f"{mh[mh.label=='Depression']['word_count'].median():.0f} kata")
    k4.metric("Selisih Max−Min",   f"{mh.groupby('label')['word_count'].median().max()-mh.groupby('label')['word_count'].median().min():.0f} kata")
    st.markdown("<hr>", unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["📏 Panjang Teks","🔑 Kata Kunci per Label","📊 % Teks Pendek"])

    with t1:
        mhcap = mh[mh.word_count<=500]
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        dv = [mhcap[mhcap.label==l]["word_count"].values for l in lbl_order]
        vp = axes[0].violinplot(dv, positions=range(len(lbl_order)), showmedians=True)
        for body,col in zip(vp["bodies"], PAL): body.set_facecolor(col); body.set_alpha(0.75)
        vp["cmedians"].set_color(TX)
        for el in ["cbars","cmins","cmaxes"]: vp[el].set_color("#D1FAE5")
        axes[0].set_xticks(range(len(lbl_order)))
        axes[0].set_xticklabels(lbl_order, rotation=30, fontsize=9)
        axes[0].set_title("Distribusi Word Count (Violin)", color=TX, fontweight="bold")
        axes[0].set_ylabel("Jumlah Kata", color=TX)
        axes[0].grid(axis="y", alpha=0.4)
        med = mh.groupby("label")["word_count"].median().reindex(lbl_order)
        bars = axes[1].barh(med.index, med.values, color=PAL[:len(med)], edgecolor="none", height=0.6)
        for bar,val in zip(bars, med.values):
            axes[1].text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
                f"{val:.0f} kata", va="center", fontsize=9, color=TX)
        axes[1].set_title("Median Word Count per Label", color=TX, fontweight="bold")
        axes[1].set_xlabel("Median Kata", color=TX)
        axes[1].grid(axis="x", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t2:
        sel = st.selectbox("Pilih kondisi:", mh["label"].unique(), key="kw_sel")
        darkfig()
        txts = mh[mh.label==sel]["text_clean"].dropna().str.lower().str.split()
        wds  = [w for ws in txts for w in ws if w.isalpha() and w not in STOPWORDS and len(w)>2]
        top  = Counter(wds).most_common(14)
        if top:
            wl,cl = zip(*top)
            ci = list(mh["label"].unique()).index(sel) % len(PAL)
            fig, ax = plt.subplots(figsize=(10,5))
            ax.barh(list(wl)[::-1], list(cl)[::-1], color=PAL[ci], alpha=0.85, edgecolor="none")
            ax.set_title(f"Top 14 Kata Kunci — {sel}", color=TX, fontweight="bold")
            ax.set_xlabel("Frekuensi", color=TX)
            ax.grid(axis="x", alpha=0.4)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True); plt.close()

    with t3:
        darkfig()
        pct = mh.groupby("label").apply(lambda x:(x.word_count<30).mean()*100).reindex(lbl_order)
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        bars = axes[0].barh(pct.index, pct.values, color=PAL[:len(pct)], edgecolor="none", height=0.55)
        for bar,val in zip(bars, pct.values):
            axes[0].text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
                f"{val:.1f}%", va="center", fontsize=9, color=TX)
        axes[0].set_title("% Teks Pendek (<30 kata)", color=TX, fontweight="bold")
        axes[0].set_xlabel("Persentase (%)", color=TX)
        axes[0].grid(axis="x", alpha=0.4)
        for lbl, col in zip(["Normal","Depression","Suicidal"], [G1, BL, R]):
            sub = mh[(mh.label==lbl)&(mh.word_count<=400)]["word_count"]
            axes[1].hist(sub, bins=35, alpha=0.55, label=lbl, color=col, edgecolor="none")
        axes[1].set_title("Histogram Word Count: 3 Kondisi Utama", color=TX, fontweight="bold")
        axes[1].set_xlabel("Word Count", color=TX); axes[1].set_ylabel("Frekuensi", color=TX)
        axes[1].legend(); axes[1].grid(alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    st.markdown("""<div class="insight">
    ✅ <strong>Jawaban PB2:</strong> YA, pola teks sangat signifikan membedakan kondisi.
    <strong>Normal</strong> median 10 kata (86% teks &lt;30 kata), sedangkan
    <strong>Bipolar</strong> dan <strong>Personality Disorder</strong> median 134–143 kata.
    Kata kunci khas: Suicidal (<em>suicide, kill, pain</em>), Depression (<em>depressed, worthless</em>).
    <strong>Rekomendasi:</strong> TF-IDF + fitur <code>word_count</code> → akurasi model meningkat.
    </div>""", unsafe_allow_html=True)

elif "PB3" in page:
    st.title("🧴  PB3 — Distribusi Kondisi Kulit dalam Dataset")
    st.markdown("""<div class="pb-card"><h3>❓ Pertanyaan Bisnis 3</h3>
    <p>Kondisi kulit apa yang paling umum ditemukan dalam dataset dan bagaimana distribusinya?</p>
    </div>""", unsafe_allow_html=True)

    vc_skin = skin["label"].value_counts()
    vc_ham  = ham["dx_full"].value_counts()
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Gambar", f"{len(skin):,}")
    k2.metric("Jumlah Kelas", str(skin.label.nunique()))
    k3.metric("Total HAM10000", f"{len(ham):,}")
    k4.metric("Kelas HAM10000", "7 kelas klinis")
    st.markdown("<hr>", unsafe_allow_html=True)

    t1,t2 = st.tabs(["📊 Master Skin Manifest","🔬 HAM10000 Klinis"])

    with t1:
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(16,7))
        cols_b = (PAL*4)[:len(vc_skin)]
        bars = axes[0].barh(vc_skin.index, vc_skin.values, color=cols_b, edgecolor="none", height=0.7)
        for bar,val in zip(bars, vc_skin.values):
            axes[0].text(bar.get_width()+5, bar.get_y()+bar.get_height()/2,
                f"{val:,}  ({val/len(skin)*100:.1f}%)", va="center", fontsize=7.5, color=TX)
        axes[0].invert_yaxis()
        axes[0].set_title(f"Kelas Penyakit Kulit (Total: {len(skin):,})", color=TX, fontweight="bold")
        axes[0].set_xlabel("Jumlah Gambar", color=TX)
        axes[0].grid(axis="x", alpha=0.4)
        vc_src = skin["source"].value_counts()
        w,t_,at = axes[1].pie(vc_src.values, labels=vc_src.index, autopct="%1.1f%%",
            colors=[G1,G2,P], startangle=90,
            wedgeprops={"edgecolor":"white","linewidth":2,"width":0.55})
        for x in t_+at: x.set_color(TX); x.set_fontsize(10)
        axes[1].set_title("Proporsi Sumber Data", color=TX, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t2:
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        labels_h = list(vc_ham.index)
        bars = axes[0].bar(labels_h, vc_ham.values, color=PAL[:7], edgecolor="none", width=0.7)
        for bar,val in zip(bars, vc_ham.values):
            axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+40,
                f"{val:,}", ha="center", va="bottom", fontsize=8, color=TX)
        axes[0].set_title("HAM10000 — Distribusi 7 Kelas", color=TX, fontweight="bold")
        axes[0].set_ylabel("Jumlah", color=TX)
        axes[0].tick_params(axis="x", rotation=25)
        axes[0].grid(axis="y", alpha=0.4)
        tc = [G1 if v>=500 else R for v in vc_ham.values]
        axes[1].bar(labels_h, vc_ham.values, color=tc, edgecolor="none", width=0.7)
        axes[1].axhline(500, color=Y, ls="--", lw=1.5, label="Min threshold (500)")
        ok  = mpatches.Patch(color=G1, label="≥500 (cukup)")
        bad = mpatches.Patch(color=R,  label="<500 (perlu augmentasi)")
        axes[1].legend(handles=[ok,bad])
        axes[1].set_title("Kesiapan Data per Kelas", color=TX, fontweight="bold")
        axes[1].set_ylabel("Jumlah", color=TX)
        axes[1].tick_params(axis="x", rotation=25)
        axes[1].grid(axis="y", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    st.markdown("""<div class="insight">
    ✅ <strong>Jawaban PB3:</strong> Kondisi paling umum adalah <strong>Psoriasis (8.6%)</strong>
    dan <strong>Seborrheic Keratoses (8.5%)</strong>. Total 30.000+ gambar dari DermNet (94.2%),
    AcneDataset, dan HAM10000. Kelas <strong>Vascular Lesions</strong> dan <strong>Dermatofibroma</strong>
    di HAM10000 di bawah threshold 500 — augmentasi wajib sebelum training model CNN.
    </div>""", unsafe_allow_html=True)

elif "PB4" in page:
    st.title("👤  PB4 — Korelasi Demografis dengan Penyakit Kulit")
    st.markdown("""<div class="pb-card"><h3>❓ Pertanyaan Bisnis 4</h3>
    <p>Apakah faktor demografis (usia, lokasi tubuh) berkorelasi dengan jenis kondisi kulit?</p>
    </div>""", unsafe_allow_html=True)

    avg_age = ham.groupby("dx_full")["age"].mean()
    k1,k2,k3 = st.columns(3)
    k1.metric("Penyakit Tertua",  avg_age.idxmax(), f"avg {avg_age.max():.1f} th")
    k2.metric("Penyakit Termuda", avg_age.idxmin(), f"avg {avg_age.min():.1f} th")
    k3.metric("Top Lokasi Lesi",  ham.localization.mode()[0],
              f"{ham.localization.value_counts().values[0]:,} kasus")
    st.markdown("<hr>", unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["📅 Distribusi Usia","📍 Lokasi Tubuh","⚧ Gender"])

    with t1:
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        avg_sorted = avg_age.sort_values()
        bc = [R if v>=60 else Y if v>=45 else G1 for v in avg_sorted.values]
        bars = axes[0].barh(avg_sorted.index, avg_sorted.values, color=bc, edgecolor="none", height=0.6)
        for bar,val in zip(bars, avg_sorted.values):
            axes[0].text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                f"{val:.1f} th", va="center", fontsize=9, color=TX)
        axes[0].axvline(50, color=Y, ls="--", lw=1.2, alpha=0.8, label="50 th")
        axes[0].set_title("Rata-rata Usia per Penyakit", color=TX, fontweight="bold")
        axes[0].set_xlabel("Usia (tahun)", color=TX)
        axes[0].legend(); axes[0].grid(axis="x", alpha=0.4)
        ac = pd.crosstab(ham.age_group, ham.dx_full, normalize="columns")*100
        sns.heatmap(ac, ax=axes[1], cmap="Greens", annot=True, fmt=".1f",
            linewidths=0.5, linecolor="white", cbar_kws={"shrink":0.8})
        axes[1].set_title("Distribusi Usia per Penyakit (%)", color=TX, fontweight="bold")
        axes[1].tick_params(axis="x", rotation=25)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t2:
        darkfig()
        toplocs = ham.localization.value_counts().head(7).index
        cloc = pd.crosstab(ham.dx_full, ham.localization)[toplocs]
        fig, ax = plt.subplots(figsize=(12,6))
        sns.heatmap(cloc, ax=ax, cmap="Greens", annot=True, fmt="d",
            linewidths=0.5, linecolor="white", cbar_kws={"shrink":0.8})
        ax.set_title("Distribusi Penyakit per Lokasi Tubuh (HAM10000)", color=TX, fontweight="bold")
        ax.tick_params(axis="x", rotation=25); ax.tick_params(axis="y", rotation=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t3:
        darkfig()
        gc = pd.crosstab(ham.dx_full, ham.sex, normalize="index")*100
        for col in ["male","female"]:
            if col not in gc.columns: gc[col]=0
        fig, ax = plt.subplots(figsize=(10,5))
        gc[["male","female"]].plot(kind="bar", ax=ax, color=[BL,"#EC4899"],
            edgecolor="none", width=0.7)
        ax.axhline(50, color=TX, ls="--", lw=0.8, alpha=0.4)
        ax.set_title("Distribusi Gender per Penyakit (%)", color=TX, fontweight="bold")
        ax.set_ylabel("Persentase (%)", color=TX)
        ax.tick_params(axis="x", rotation=25)
        ax.legend(title="Gender"); ax.grid(axis="y", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    st.markdown("""<div class="insight">
    ✅ <strong>Jawaban PB4:</strong> YA, sangat signifikan.
    <strong>Basal Cell Carcinoma</strong> dan <strong>Actinic Keratosis</strong>
    dominan usia 61-85 tahun (avg 66-67 th). <strong>Punggung</strong> dan lower extremity
    lokasi paling sering. Usia, lokasi tubuh, dan gender harus menjadi fitur tambahan
    model AI Skin Detection selain gambar.
    </div>""", unsafe_allow_html=True)

elif "PB5" in page:
    st.title("💄  PB5 — Sentimen & Rekomendasi Produk Skincare")
    st.markdown("""<div class="pb-card"><h3>❓ Pertanyaan Bisnis 5</h3>
    <p>Produk skincare kategori apa yang paling direkomendasikan berdasarkan sentimen pengguna?</p>
    </div>""", unsafe_allow_html=True)

    sv = sep.sentiment.value_counts()
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Ulasan",     f"{len(sep):,}")
    k2.metric("Sentimen Positif", f"{sv.get('Positive',0)/len(sep)*100:.1f}%", f"{sv.get('Positive',0):,}")
    k3.metric("Avg Rating",       f"{sep.rating.mean():.2f} ⭐")
    k4.metric("Total Brand",      str(sep.brand_name.nunique()))
    st.markdown("<hr>", unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["📊 Sentimen & Rating","🏆 Top Brand","👤 per Tipe Kulit"])

    with t1:
        topcats = sep.secondary_category.value_counts().head(8).index
        dftop   = sep[sep.secondary_category.isin(topcats)]
        sc = pd.crosstab(dftop.secondary_category, dftop.sentiment, normalize="index")*100
        for c in ["Positive","Neutral","Negative"]:
            if c not in sc.columns: sc[c]=0
        sc = sc[["Positive","Neutral","Negative"]].sort_values("Positive", ascending=True)
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(14,6))
        sc.plot(kind="barh", ax=axes[0], color=[G1,"#94A3B8",R], stacked=True, edgecolor="none", width=0.7)
        axes[0].axvline(75, color=Y, ls="--", lw=1.5, alpha=0.8)
        axes[0].set_title("Sentimen per Kategori (Top 8)", color=TX, fontweight="bold")
        axes[0].set_xlabel("Persentase (%)", color=TX)
        axes[0].legend(loc="lower right"); axes[0].grid(axis="x", alpha=0.4)
        rv = sep.rating.value_counts().sort_index()
        bc = [R,"#F97316","#94A3B8",G2,G1]
        bars = axes[1].bar(rv.index.astype(str), rv.values, color=bc, edgecolor="none", width=0.7)
        for bar,val in zip(bars, rv.values):
            axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+100,
                f"{val:,}", ha="center", va="bottom", fontsize=8, color=TX)
        axes[1].set_title("Distribusi Rating (1–5 ⭐)", color=TX, fontweight="bold")
        axes[1].set_xlabel("Rating", color=TX); axes[1].set_ylabel("Jumlah", color=TX)
        axes[1].grid(axis="y", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t2:
        darkfig()
        tb = (sep.groupby("brand_name")
              .agg(avg_rating=("rating","mean"), total=("rating","count"))
              .query("total>=100").sort_values("avg_rating", ascending=True).tail(10))
        fig, ax = plt.subplots(figsize=(10,5))
        bars = ax.barh(tb.index, tb.avg_rating, color=PAL[:10], edgecolor="none", height=0.6)
        for bar,val in zip(bars, tb.avg_rating):
            ax.text(bar.get_width()+0.01, bar.get_y()+bar.get_height()/2,
                f"{val:.2f} ⭐", va="center", fontsize=9, color=TX)
        ax.set_title("Top 10 Brand — Avg Rating (min 100 ulasan)", color=TX, fontweight="bold")
        ax.set_xlabel("Avg Rating", color=TX)
        ax.set_xlim(3.5, 5.3); ax.grid(axis="x", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t3:
        darkfig()
        dfs = sep[sep.skin_type!="Unknown"]
        sc2 = pd.crosstab(dfs.skin_type, dfs.sentiment, normalize="index")*100
        for c in ["Positive","Neutral","Negative"]:
            if c not in sc2.columns: sc2[c]=0
        sc2 = sc2[["Positive","Neutral","Negative"]]
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        sc2.plot(kind="bar", ax=axes[0], color=[G1,"#94A3B8",R], stacked=True, edgecolor="none", width=0.7)
        axes[0].set_title("Sentimen per Tipe Kulit (%)", color=TX, fontweight="bold")
        axes[0].set_ylabel("Persentase (%)", color=TX)
        axes[0].tick_params(axis="x", rotation=0); axes[0].legend()
        axes[0].grid(axis="y", alpha=0.4)
        sr = dfs.groupby("skin_type").is_recommended.mean()*100
        bars2 = axes[1].bar(sr.index, sr.values, color=PAL[:4], edgecolor="none", width=0.6)
        for bar,val in zip(bars2, sr.values):
            axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=9, color=TX)
        axes[1].set_title("% Produk Direkomendasikan per Tipe Kulit", color=TX, fontweight="bold")
        axes[1].set_ylabel("% Direkomendasikan", color=TX)
        axes[1].set_ylim(60,100); axes[1].grid(axis="y", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    st.markdown("""<div class="insight">
    ✅ <strong>Jawaban PB5:</strong> <strong>Treatments (82.9%)</strong> dan
    <strong>High Tech Tools (81.9%)</strong> mendapat sentimen positif tertinggi.
    79% ulasan positif, rating 5-bintang mendominasi 63% ulasan.
    Tingkat rekomendasi tinggi di semua tipe kulit (74–76%).
    Basis konten artikel skincare DerMind — khususnya kulit <strong>combination</strong> (50%+ pengguna).
    </div>""", unsafe_allow_html=True)

elif "PB6" in page:
    st.title("🌍  PB6 — Faktor Gaya Hidup & Kesehatan")
    st.markdown("""<div class="pb-card"><h3>❓ Pertanyaan Bisnis 6</h3>
    <p>Faktor gaya hidup apa yang paling mempengaruhi kesehatan dan kebahagiaan?</p>
    </div>""", unsafe_allow_html=True)

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Kota #1 Tersehat", life.iloc[0]["city"], f"Rank {life.iloc[0]['rank']}")
    k2.metric("Happiness Tertinggi", life.loc[life.happiness.idxmax(),"city"],
              f"{life.happiness.max():.2f}")
    k3.metric("Korelasi + Happiness", "Outdoor Activities", "vs happiness")
    k4.metric("Korelasi − Happiness", "Obesity Level",      "vs happiness")
    st.markdown("<hr>", unsafe_allow_html=True)

    numcols = ["sunshine_hours","obesity_levels","life_expectancy",
               "pollution_index","hours_worked","happiness","outdoor_activities"]
    life_n = life.dropna(subset=numcols)

    t1,t2,t3 = st.tabs(["📊 Korelasi","🏙️ Top 10 Kota","🔍 Explorer Scatter"])

    with t1:
        darkfig()
        fig, axes = plt.subplots(1,2, figsize=(14,6))
        corr_h = life_n[numcols].corr()["happiness"].drop("happiness").sort_values()
        bc = [G1 if v>0 else R for v in corr_h.values]
        axes[0].barh(corr_h.index, corr_h.values, color=bc, edgecolor="none", height=0.6)
        axes[0].axvline(0, color=TX, lw=0.8)
        for i,val in enumerate(corr_h.values):
            axes[0].text(val+(0.01 if val>=0 else -0.01), i,
                f"{val:.2f}", va="center", ha="left" if val>=0 else "right",
                fontsize=9, color=TX)
        axes[0].set_title("Korelasi Faktor vs Happiness (Pearson)", color=TX, fontweight="bold")
        axes[0].set_xlabel("Koefisien Korelasi", color=TX)
        axes[0].grid(axis="x", alpha=0.4)
        mask = np.triu(np.ones_like(life_n[numcols].corr(), dtype=bool))
        sns.heatmap(life_n[numcols].corr(), mask=mask, ax=axes[1], cmap="Greens",
            center=0, annot=True, fmt=".2f", linewidths=0.5, linecolor="white",
            cbar_kws={"shrink":0.8})
        axes[1].set_title("Heatmap Korelasi Semua Indikator", color=TX, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t2:
        darkfig()
        top10 = life.head(10)
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        bc2 = [G1 if i<3 else G2 if i<7 else G3 for i in range(len(top10))]
        axes[0].barh(top10.city[::-1], top10.happiness[::-1], color=bc2[::-1], edgecolor="none", height=0.6)
        axes[0].set_title("Top 10 Kota — Happiness Score", color=TX, fontweight="bold")
        axes[0].set_xlabel("Happiness Score", color=TX)
        axes[0].grid(axis="x", alpha=0.4)
        axes[1].scatter(life_n.obesity_levels, life_n.happiness, color=G1, s=70, alpha=0.85, edgecolors="none")
        z = np.polyfit(life_n.obesity_levels, life_n.happiness, 1)
        xl = np.linspace(life_n.obesity_levels.min(), life_n.obesity_levels.max(), 50)
        axes[1].plot(xl, np.poly1d(z)(xl), "--", color=Y, lw=2)
        for _,row in life.head(6).iterrows():
            axes[1].annotate(row.city, (row.obesity_levels, row.happiness),
                xytext=(3,3), textcoords="offset points", fontsize=7.5, color="#6B7280")
        r = life_n.obesity_levels.corr(life_n.happiness)
        axes[1].set_title(f"Obesitas vs Happiness  (r = {r:.2f})", color=TX, fontweight="bold")
        axes[1].set_xlabel("Obesity Level (%)", color=TX)
        axes[1].set_ylabel("Happiness Score", color=TX)
        axes[1].grid(alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    with t3:
        st.markdown("#### 🔍 Eksplorasi korelasi dua variabel")
        xa,ya = st.columns(2)
        xv = xa.selectbox("Sumbu X:", [c for c in numcols if c!="happiness"], index=0)
        yv = ya.selectbox("Sumbu Y:", numcols, index=5)
        darkfig()
        sub = life_n[[xv,yv,"city"]].dropna()
        fig, ax = plt.subplots(figsize=(10,5))
        ax.scatter(sub[xv], sub[yv], color=G1, s=75, alpha=0.85, edgecolors="none")
        z2 = np.polyfit(sub[xv], sub[yv], 1)
        xl2 = np.linspace(sub[xv].min(), sub[xv].max(), 50)
        ax.plot(xl2, np.poly1d(z2)(xl2), "--", color=Y, lw=2)
        for _,row in sub.iterrows():
            ax.annotate(row.city, (row[xv], row[yv]),
                xytext=(3,3), textcoords="offset points", fontsize=7, color="#9CA3AF")
        rv = sub[xv].corr(sub[yv])
        ax.set_title(f"{xv}  vs  {yv}   (r = {rv:.2f})", color=TX, fontweight="bold")
        ax.set_xlabel(xv, color=TX); ax.set_ylabel(yv, color=TX)
        ax.grid(alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close()

    st.markdown("""<div class="insight">
    ✅ <strong>Jawaban PB6:</strong> Faktor paling berkorelasi positif dengan kebahagiaan:
    <strong>outdoor activities</strong> dan <strong>sunshine hours</strong>.
    Paling negatif: <strong>tingkat obesitas</strong> dan <strong>pollution index</strong>.
    Kota tersehat (Amsterdam, Copenhagen, Helsinki): polusi rendah + outdoor activities tinggi
    + jam kerja moderat. Temuan ini menjadi konten artikel wellness DerMind.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    DerMind Capstone Project : CC26-PSU382 &nbsp;|&nbsp; DerMind Dashboard &nbsp;|&nbsp;
    52.940 Mental Health · 20.015 Skin · 10.015 HAM10000 · 49.394 Sephora · 44 Lifestyle Cities
</div>
""", unsafe_allow_html=True)
