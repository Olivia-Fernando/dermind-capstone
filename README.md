# DerMind — Dashboard Capstone Data Science

## Cara Menjalankan Dashboard

### 1. Install dependencies

bash
pip install -r requirements.txt

### 2. Letakkan semua file CSV di folder yang sama

Pastikan file di satu folder yang sama dengan `dashboard_dermind.py`:

- `master_mental_health_clean.csv`
- `master_skin_image_manifest.csv`
- `HAM10000_clean.csv`
- `master_sephora.csv`
- `healthy_lifestyle_city_2021_cleaned.csv`

### 3. Jalankan dashboard

```bash
streamlit run dashboard_dermind.py
```

Dashboard akan terbuka otomatis di browser: `https://dermind-capstone-cc26-psu382.streamlit.app/`

---

## Cara Menjalankan EDA & Explanatory Analysis

Buka di Google Colab atau VSCode dengan Jupyter:

- `EDA_Mental_Health.ipynb`
- `EDA_Skin.ipynb`
- `EDA_Skincare_Lifestyle.ipynb`
- `Explanatory_Analysis.ipynb`

---

## Struktur File

```
dermind_capstone/
│
├──  dashboard/
│   ├── data/
│   │   ├── dataset.zip/                           
│   │       ├── HAM10000_clean.csv                       
│   │       ├── healthy_lifestyle_city_2021_cleaned.csv  
│   │       ├── master_mental_health_clean.csv           
│   │       ├── master_sephora.csv                       
│   │       ├── master_skin_image_manifest.csv           
│   │   
│   │
│   └── dashboard_dermind.py                        
│
├── EDA_Mental_Health.ipynb                          
├── EDA_Skin.ipynb                                   
├── EDA_Skincare_Lifestyle.ipynb                     
├── Explanatory_Analysis.ipynb                       
├──  README.md                                     
└── requirements.txt                                 
```

## 6 Pertanyaan Bisnis

| #   | Pertanyaan                               | Dataset                | Fitur Platform           |
| --- | ---------------------------------------- | ---------------------- | ------------------------ |
| PB1 | Kondisi mental health paling dominan?    | master_mental_health   | AI Mental Health Chatbot |
| PB2 | Pola teks bisa membedakan kondisi?       | master_mental_health   | AI Mental Health Chatbot |
| PB3 | Kondisi kulit paling umum?               | master_skin + HAM10000 | AI Skin Detection        |
| PB4 | Usia & lokasi berkorelasi dengan kulit?  | HAM10000               | AI Skin Detection        |
| PB5 | Produk skincare paling direkomendasikan? | master_sephora         | Konten Artikel           |
| PB6 | Faktor lifestyle paling berpengaruh?     | healthy_lifestyle      | Konten Artikel           |
