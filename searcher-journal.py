import streamlit as st
import os
import requests
import time
import random
import zipfile
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. CONFIGURATION: STRICT BLACK & WHITE THEME ---
st.set_page_config(page_title="Searcher Journal", layout="wide", page_icon="⚫")

st.markdown("""
    <style>
    /* IMPORT FONT: COURIER PRIME (Monospace Murni) */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

    /* --- GLOBAL VARIABLES: ONLY BLACK AND WHITE --- */
    :root {
        --ink: #000000;
        --paper: #ffffff;
    }

    /* --- BASE LAYOUT --- */
    .stApp {
        background-color: var(--paper);
        color: var(--ink);
        font-family: 'Courier Prime', monospace;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3, h4, h5, h6, p, div, label, span, .stMarkdown, .stCode {
        font-family: 'Courier Prime', monospace !important;
        color: var(--ink) !important;
    }

    h1 {
        border: 4px solid var(--ink);
        padding: 20px;
        text-align: center;
        text-transform: uppercase;
        font-weight: 900;
        background-color: var(--paper);
        margin-bottom: 40px;
        box-shadow: 10px 10px 0px var(--ink); /* Hard Shadow Hitam */
    }

    h3, .stCaption {
        text-transform: uppercase;
        font-weight: bold;
        border-bottom: 2px solid var(--ink);
        padding-bottom: 5px;
    }

    /* --- INPUT FIELDS (NO GREY) --- */
    /* Input Box Normal */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: var(--paper) !important;
        color: var(--ink) !important;
        border: 3px solid var(--ink) !important;
        border-radius: 0px !important;
        font-weight: bold;
        caret-color: var(--ink); /* Kursor Hitam */
    }
    
    /* Input Box Focus (Inversi Warna) */
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        background-color: var(--ink) !important;
        color: var(--paper) !important;
        border-color: var(--ink) !important;
    }

    /* --- DROPDOWN (SELECTBOX) --- */
    .stSelectbox > div > div {
        background-color: var(--paper) !important;
        color: var(--ink) !important;
        border: 3px solid var(--ink) !important;
        border-radius: 0px;
    }
    .stSelectbox svg {
        fill: var(--ink) !important;
    }
    /* Dropdown Options List */
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: var(--paper) !important;
        border: 3px solid var(--ink) !important;
    }
    li[role="option"]:hover {
        background-color: var(--ink) !important;
        color: var(--paper) !important;
    }

    /* --- BUTTONS (HARD INTERACTION) --- */
    .stButton>button {
        width: 100%;
        background-color: var(--paper);
        color: var(--ink) !important;
        border: 3px solid var(--ink);
        border-radius: 0px;
        font-weight: 900;
        text-transform: uppercase;
        padding: 15px 24px;
        transition: all 0.0s; /* No fade, instant switch */
        box-shadow: 6px 6px 0px var(--ink);
    }
    
    /* HOVER: INVERT COLORS (Black BG, White Text) */
    .stButton>button:hover {
        background-color: var(--ink);
        color: var(--paper) !important;
        border-color: var(--ink);
        box-shadow: 2px 2px 0px var(--ink);
        transform: translate(4px, 4px);
    }
    
    .stButton>button:active {
        background-color: var(--ink);
        color: var(--paper) !important;
        transform: translate(6px, 6px);
        box-shadow: none;
    }

    /* --- DOWNLOAD BUTTONS --- */
    [data-testid="stDownloadButton"] > button {
        background-color: var(--paper);
        color: var(--ink) !important;
        border: 2px dashed var(--ink); /* Garis Putus-putus Hitam */
        border-radius: 0px;
        font-family: 'Courier Prime', monospace;
        font-weight: bold;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background-color: var(--ink);
        color: var(--paper) !important;
        border-style: solid;
    }

    /* --- COMPONENTS & UTILS --- */
    .stCode {
        border: 2px solid var(--ink);
        background-color: var(--paper) !important;
        border-radius: 0px;
    }
    
    /* Progress Bar (Make it Solid Black) */
    .stProgress > div > div > div > div {
        background-color: var(--ink) !important;
    }
    .stProgress > div > div {
        background-color: var(--paper) !important;
        border: 2px solid var(--ink);
        border-radius: 0px;
    }

    /* Alerts / Toasts */
    .stAlert {
        background-color: var(--paper);
        border: 3px solid var(--ink);
        color: var(--ink);
        border-radius: 0px;
    }
    
    /* Hiding Streamlit Branding */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC: ARCHIVE & ZIP ENGINE ---

def create_zip_archive(folder_path):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, arcname=file)
    return zip_buffer

def run_research_acquisition(subject, quota, base_path, index_mode):
    # --- 1. CONFIGURATION ---
    query_bank = {
        "NO SITE FILTER": [f'"{subject}" filetype:pdf'], 
        "ALL INDEX": [
            f'site:scholar.google.com "{subject}" filetype:pdf',
            f'site:sciencedirect.com "{subject}" filetype:pdf',
            f'"{subject}" filetype:pdf site:.edu',
            f'"{subject}" filetype:pdf site:.ac.id'
        ],
        # ... (opsi lainnya tetap sama)
    }

    selected_queries = query_bank.get(index_mode, [f'"{subject}" filetype:pdf'])
    
    # Setup Driver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    found_urls = set()
    total_downloaded = 0
    potential_discoveries = 0 # Counter untuk notice total temuan
    
    progress_bar = st.progress(0)
    status_indicator = st.empty()
    discovery_notice = st.empty() # Placeholder untuk info total temuan

    target_dir = os.path.join(base_path, subject.lower().replace(" ", "_"))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # --- 2. LOGIKA AKUISISI ---
    for q in selected_queries:
        if total_downloaded >= quota: break
        
        # Loop Pagination (0 hingga 20+ halaman untuk mengejar quota besar)
        for page in range(0, 30): 
            if total_downloaded >= quota: break
            
            start_val = page * 10
            url = f"https://www.google.com/search?q={q}&start={start_val}"
            
            try:
                driver.get(url)
                time.sleep(random.uniform(6, 12)) # Keamanan audit: Jeda lebih lama
                
                elements = driver.find_elements(By.TAG_NAME, "a")
                links = [e.get_attribute("href") for e in elements if e.get_attribute("href")]
                
                # Filter PDF
                page_pdfs = [l for l in links if ".pdf" in l.lower() and "google" not in l.lower()]
                
                if not page_pdfs: break 
                
                # Update Discovery Notice (Menghitung total link yang ditemukan)
                potential_discoveries += len(page_pdfs)
                discovery_notice.markdown(f"""
                > **AUDIT NOTICE:**
                > * PDF Links ESTIMASI Download: **{potential_discoveries}**
                > * PDF Successfully Archived: **{total_downloaded}**
                """)

                for link in page_pdfs:
                    if link not in found_urls and total_downloaded < quota:
                        try:
                            # Filter Domain
                            if any(x in link for x in ['facebook', 'twitter', 'youtube']): continue
                            
                            filename = f"DOC_{total_downloaded+1:03d}_{subject[:10].upper()}.pdf"
                            file_path = os.path.join(target_dir, filename)
                            
                            r = requests.get(link, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
                            
                            if r.status_code == 200 and 'pdf' in r.headers.get('Content-Type', '').lower():
                                with open(file_path, 'wb') as f:
                                    f.write(r.content)
                                
                                found_urls.add(link)
                                total_downloaded += 1
                                
                                # Update UI
                                status_indicator.text(f"PROCESS DATA: {total_downloaded}/{quota}")
                                progress_bar.progress(total_downloaded / quota)
                        except:
                            continue
            except Exception:
                break 

    driver.quit()
    return total_downloaded, target_dir

# --- 3. USER INTERFACE (STRICT B&W) ---

st.title("Searcher Journal")
st.markdown("<div style='text-align: center; border: 2px solid black; padding: 10px; margin-bottom: 30px; font-weight: bold;'>Author: AndreXyz</div>", unsafe_allow_html=True)

col_input1, col_input2 = st.columns([3, 1])

with col_input1:
    st.markdown("**TARGET KEYWORD**")
    subject_input = st.text_input("Subject Keyword", placeholder="INPUT DATA...", label_visibility="collapsed")

with col_input2:
    st.markdown("**QUOTA**")
    # Max_value dihilangkan atau diset sangat tinggi (misal: 10.000)
    quota_input = st.number_input("File Quota", min_value=1, value=100, label_visibility="collapsed")

# --- DROPDOWN PARAMETERS ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("**PROTOCOL SELECTION**")
index_options = [
    "NO SITE FILTER",
    "ALL INDEX",
    "SCOPUS", # Tambahan baru
    "GOOGLE SCHOLAR",
    "DOAJ",
    "SINTA",
    "EDU DOMAINS",
    "AC.ID DOMAINS"
]
selected_index = st.selectbox("Select Database Protocol", index_options, label_visibility="collapsed")

# Define Base Path
base_path = os.path.join(os.getcwd(), "research_downloads")

st.markdown("<br>", unsafe_allow_html=True)
start_btn = st.button("PROCESS")

# --- 4. EXECUTION ---

if start_btn:
    if not subject_input:
         st.error("ERROR: INPUT FIELD VOID.")
    else:
        st.markdown("<div style='border-top: 4px solid black; margin-top: 20px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        st.info("STATUS: ACTIVE. OBSERVE EXTERNAL WINDOW.")
        
        with st.spinner(f"SEARCHING: {subject_input.upper()}..."):
            count, final_path = run_research_acquisition(subject_input, quota_input, base_path, selected_index)
        
        if count > 0:
            st.success(f"COMPLETE. {count} UNITS ARCHIVED.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- ZIP DOWNLOADER ---
            st.markdown("### BULK EXPORT")
            zip_buffer = create_zip_archive(final_path)
            
            st.download_button(
                label="[DOWNLOAD .ZIP ARCHIVE]",
                data=zip_buffer.getvalue(),
                file_name=f"ARCHIVE_{subject_input.replace(' ', '_').upper()}.zip",
                mime="application/zip",
            )
            
            # --- FILE LIST ---
            st.markdown("### ARCHIVE MANIFEST")
            
            files = sorted(os.listdir(final_path))
            if files:
                for file_name in files:
                    if file_name.endswith(".pdf"):
                        col_a, col_b = st.columns([4, 1])
                        with col_a:
                            st.code(f"{file_name}")
                        with col_b:
                            file_path = os.path.join(final_path, file_name)
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label="RETRIEVE",
                                    data=f,
                                    file_name=file_name,
                                    mime="application/pdf",
                                    key=file_name
                                )
        else:
            st.error("RESULT: 0 UNITS FOUND.")

# --- FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; border-top: 2px solid #000000; padding-top: 15px;">
    <p style="color: #000000 !important; font-family: 'Courier Prime'; font-weight: bold; font-size: 14px;">
   Thank you.
    </p>
</div>
""", unsafe_allow_html=True)