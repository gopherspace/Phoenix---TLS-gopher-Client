import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import ssl
import urllib.parse
import configparser
import os
import threading
import json
import base64

# Moderne UI-Bibliothek
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# ScrolledText direkt aus den Widgets importieren (verhindert Warning & NameError)
from ttkbootstrap.scrolled import ScrolledText 

from tkinter import filedialog

# Das Phoenix-Logo im Base64-Format (Minimalistischer Feuer-Vogel)
PHOENIX_LOGO = "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"


# --- Konfigurations-Management ---
CONFIG_FILE = 'config.ini'
CONFIG_SECTION = 'Settings'
DEFAULT_URL = "gopher://gopherspace.de/"

# Globale Referenzen für das Satelliten-Fenster
inspector_window = None
inspector_text = None
inspector_timer = None  # Speichert die ID der Verzögerung
current_inspector_url = "" # Verhindert Daten-Salat bei schnellem Wechsel

# Language
LANG_FILE = 'phoenix.language'
LANG_DATA = {}      # Hält alle geladenen Sprachen
CURR_LANG_CODE = 'EN' # Standard-Fallback

# Speicher für die geladenen UI-Erweiterungen
current_enhanced_data = {} 

def trigger_enhanced_engine(host, port, path, scheme):
    def worker():
        global current_enhanced_data
        
        clean_path = path[2:] if len(path) > 2 else ""
        if not clean_path.startswith('/'):
            clean_path = '/' + clean_path
            
        style_url = f"{scheme}://{host}:{port}/0{clean_path}enhanced.experience"
        
        raw = fetch_binary_raw(style_url)
        if raw:
            try:
                # Dekodieren
                decoded_data = raw.decode('utf-8', errors='replace').strip()
                
                # Falls die Datei mit \n.\n oder \n. endet, wird es abgeschnitten.
                if decoded_data.endswith('\n.'):
                    decoded_data = decoded_data[:-2].strip()
                elif decoded_data.endswith('.'):
                    # Sicherheitscheck: Wenn der letzte Charakter ein Punkt ist 
                    # und davor ein Zeilenumbruch war
                    decoded_data = decoded_data[:-1].strip()

                current_enhanced_data = json.loads(decoded_data)
                # print(f"DEBUG: JSON erfolgreich geladen: {current_enhanced_data}")
                
                # UI-Refresh triggern
                root.after(0, lambda: fetch_gopher_data(is_history_navigation=True))
            except Exception as e:
                # print(f"DEBUG: JSON Parsing Fehler: {e}")
                # Wir geben das rohe Ergebnis aus, um zu sehen, was gestört hat
                # print(f"DEBUG: Rohdaten waren: {decoded_data}")
                current_enhanced_data = {"active": False}
        else:
            current_enhanced_data = {"active": False}

    threading.Thread(target=worker, daemon=True).start()


# Theme

def change_theme(theme_name):
    """Wechselt das UI-Theme mit Fehlerabsicherung."""
    try:
        style.theme_use(theme_name)
        save_config(None, None, theme_name)
        
        # Phoenix-Maße wiederherstellen (da theme_use diese zurücksetzt)
        result_area.text.config(
            width=80,
            padx=150,
            pady=30
        )
        
        # Secure-Style für die Adressleiste anpassen
        is_dark = style.theme.type == 'dark'
        secure_bg = "#1a3a2a" if is_dark else "#e6ffed"
        style.configure("Secure.TEntry", fieldbackground=secure_bg)
        
        # Button-Text aktualisieren
        theme_btn.config(text=f"{theme_name.capitalize()}")
        
    except Exception as e:
        print(f"Theme-Fehler: {theme_name} ist nicht verfügbar. Fallback auf Yeti.")
        # Sicherheits-Fallback, falls ein Name falsch geschrieben wurde
        style.theme_use("yeti")



# --- Globale Konstanten & Icons ---
# --- Phoenix Icon Set 2025 ---
# Ein einheitliches, minimalistisches Set für den PHOENIX Client
TYPE_ICONS = {
    '0': '📄 ',  # Textdatei
    'd': '📄 ',  # Dokument (PDF, DOC) -> Wie gewünscht identisch mit Text
    '1': '📁 ',  # Gopher-Menü (Ordner)
    '7': '🔍 ',  # Suche / Query
    'g': '🖼 ',  # Bild (GIF)
    'I': '🖼 ',  # Bild (Allgemein)
    'j': '🖼 ',  # JPEG (Erweiterung)
    '9': '💾 ',  # Binärdatei (Download)
    '5': '📦 ',  # Archivdatei (Zip, Tar, etc.)
    'h': '🌐 ',  # Web-Link (HTML / HTTP)
    'U': '🔗 ',  # Gopher+ URL (Umleitung)
    's': '🔊 ',  # Audio-Datei
    'p': '🎬 ',  # Video-Datei
    '4': '💾 ',  # Binärdatei Mac BinHex-Datei (Download)
}

def load_languages():
    global LANG_DATA, CURR_LANG_CODE
    
    # 1. Versuch: JSON laden
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, 'r', encoding='utf-8') as f:
                LANG_DATA = json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der JSON: {e}")

    # 2. Fallback: Falls JSON leer oder fehlerhaft, EN hart im Code hinterlegen
    if not LANG_DATA:
        LANG_DATA = {
            "EN": {
                "name": "English",
                "ui_load": "Load",
                "ui_bookmarks": "★ Bookmarks",
                "ui_status_ready": "Ready",
                "search_title": "Search Query",
                "msg_net_error": "Network Error"
            }
        }
    
    # 3. Sprache aus config.ini lesen
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        CURR_LANG_CODE = config.get(CONFIG_SECTION, 'language', fallback='EN')
        
    # Sicherstellen, dass der Code auch in den geladenen Daten existiert
    if CURR_LANG_CODE not in LANG_DATA:
        CURR_LANG_CODE = list(LANG_DATA.keys())[0]

def build_lang_menu():
    lang_menu.delete(0, tk.END)
    for code, data in LANG_DATA.items():
        # Jede Sprache aus der JSON wird hier ein Menüeintrag
        lang_menu.add_command(
            label=data.get('name', code), 
            command=lambda c=code: change_language(c)
        )

def change_language(code):
    global CURR_LANG_CODE
    CURR_LANG_CODE = code
    lang_btn.config(text=code)
    save_config(lang_code=code)
    apply_language() 
    
def apply_language():
    """Aktualisiert alle UI-Elemente basierend auf dem gewählten Sprach-Code."""
    
    # Haupt-Navigation
    # Hinweis: Ich nutze get_text(key), um sicher auf die JSON-Daten zuzugreifen
    load_btn.config(text=get_text('ui_load'))
    bm_btn.config(text=get_text('ui_bookmarks'))
    status_label.config(text=get_text('ui_status_ready'))
    
    # Lesezeichen-Menü neu aufbauen (da sich dort die festen Einträge ändern)
    refresh_bookmark_menu()
    
    # Sprach-Menü Button (zeigt immer das aktuelle Kürzel)
    lang_btn.config(text=CURR_LANG_CODE)
    
    # Falls der Inspector offen ist, Titel aktualisieren
    if inspector_window and inspector_window.winfo_exists():
        inspector_window.title(get_text('ins_title'))


def get_text(key):
    """Hilfsfunktion: Holt den Text für den aktuellen Key."""
    return LANG_DATA.get(CURR_LANG_CODE, {}).get(key, f"[{key}]")


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if CONFIG_SECTION in config and 'last_url' in config[CONFIG_SECTION]:
            return config[CONFIG_SECTION]['last_url']
    return DEFAULT_URL

def save_config(url=None, lang_code=None, theme=None):
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    if CONFIG_SECTION not in config:
        config[CONFIG_SECTION] = {}
        
    if url: config[CONFIG_SECTION]['last_url'] = url
    if lang_code: config[CONFIG_SECTION]['language'] = lang_code
    if theme: config[CONFIG_SECTION]['theme'] = theme
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)



def show_client_info():
    """Zeigt Client-Details im Phoenix Inspector an."""
    # Ich nutze die bestehende update_inspector Logik, um das Fenster zu öffnen
    update_inspector("Phoenix Internal", is_plus=False, item_type="ℹ")
    
    # Inhalt des Inspektors überschreiben
    inspector_text.config(state=tk.NORMAL)
    inspector_text.delete('1.0', tk.END)
    
    info_text = (
        "PHOENIX - TLS Gopher+ CLIENT INFORMATION\n"
        "_______________________________________________________________\n\n"
        "Name:\tPhoenix | TLS Gopher+ Client\n"
        "Version:\t1.1.7 (Build 2025-Rev1)\n"
        f"{get_text('info_author')}:\tRené Gabel (gopherspace.de)\n" # Label übersetzt
		"Engineering:\tAI-assisted by Google Gemini\n"
        f"{get_text('info_last_change')}:\t22. Dezember 2025\n\n"                # Label übersetzt
        "_______________________________________________________________\n"
		"\n"
        "Features:\n\n"
        "* TLS/gophers Support\n"
		"* Bookmark management\n"
        "* Gopher+ Metadata Support\n"
		"* enhanced:eXperience Support\n"
		"* Dynamic Theme Engine (12 designs)\n"
        "* Internationalization Support (8 languages)\n"
        "_______________________________________________________________\n"
        "\n"
        "License:\n\n"
        "* MIT License & CC BY-NC 4.0\n"
		"* Copyright (c) 2025 René Gabel/gopherspace.de\n"
		"* Full license text available in the LICENSE.txt file in the program folder.\n"
    )
    
    inspector_text.insert(tk.END, info_text)
    inspector_text.config(state=tk.DISABLED)


# ---- Download-Management ---

from tkinter import filedialog

def start_binary_download(url):
    """Startet einen binären Download mit Dateiauswahl-Dialog."""
    parsed = urllib.parse.urlparse(url)
    # Extrahiere den Dateinamen aus dem Pfad (z.B. bild.gif)
    default_name = os.path.basename(parsed.path) or "datei.bin"
    
    # Nutzer nach Speicherort fragen
    save_path = filedialog.asksaveasfilename(
        initialfile=default_name,
        title="Phoenix - " + get_text('ui_save_as'),
        parent=root
    )
    
    if not save_path:
        return # Abbruch durch Nutzer

    def dl_worker():
        # Status auf "Laden" setzen - nutzt jetzt get_text
        root.after(0, lambda: status_label.config(text=get_text('ui_status_downloading'), bootstyle="warning"))
        
        # Rohdaten über die bereits existierende Funktion holen
        data = fetch_binary_raw(url)
        
        if data:
            try:
                with open(save_path, 'wb') as f:
                    f.write(data)
                # Erfolgsmeldung übersetzt
                root.after(0, lambda: messagebox.showinfo("Phoenix Download", f"{get_text('msg_save_success')}:\n{save_path}"))
            except Exception as e:
                # Fehlermeldung beim Speichern übersetzt
                root.after(0, lambda: messagebox.showerror("Phoenix", f"{get_text('msg_save_err')}:\n{e}"))
        else:
            # Netzwerkfehler übersetzt
            root.after(0, lambda: messagebox.showerror("Phoenix", get_text('msg_net_error')))
        
        # Status zurücksetzen - nutzt jetzt get_text
        root.after(0, lambda: status_label.config(text=get_text('ui_status_ready'), bootstyle="success"))


# --- Lesezeichen-Management ---
BOOKMARKS_FILE = 'phoenix.bookmark'

def load_bookmarks():
    """Lädt die Lesezeichen aus der JSON-Datei."""
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            # Interner Log auf Englisch/Deutsch oder nutzt msg_net_error
            print(f"Error loading bookmarks: {e}")
            return []
    return []

def save_bookmark(name, url, item_type):
    """Speichert ein neues Lesezeichen in der JSON-Datei."""
    bookmarks = load_bookmarks()
    if not any(b['url'] == url for b in bookmarks):
        bookmarks.append({"name": name, "url": url, "type": item_type})
        try:
            with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(bookmarks, f, indent=4)
            return True
        except Exception as e:
            # ÜBERSETZT: "Speichern fehlgeschlagen"
            messagebox.showerror("Phoenix", f"{get_text('msg_save_err')}: {e}")
            return False
    return False

def delete_bookmark(index):
    """Löscht ein Lesezeichen anhand seines Index in der JSON-Liste."""
    bookmarks = load_bookmarks()
    if 0 <= index < len(bookmarks):
        del bookmarks[index]
        try:
            with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(bookmarks, f, indent=4)
            refresh_bookmark_menu()
            return True
        except Exception as e:
            # ÜBERSETZT: "Löschen fehlgeschlagen"
            messagebox.showerror("Phoenix", f"{get_text('msg_del_err')}: {e}")
    return False

def open_bookmark_manager():
    """Öffnet ein separates Fenster zum Verwalten (Löschen) der Lesezeichen."""
    manager = tk.Toplevel(root)
    # ÜBERSETZT: "Phoenix - Lesezeichen verwalten"
    manager.title(get_text('bm_title'))
    manager.geometry("500x350")
    manager.attributes('-topmost', True)

    lb = tk.Listbox(manager, font=("Segoe UI", 10), selectmode=tk.SINGLE)
    lb.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def reload_list():
        lb.delete(0, tk.END)
        for b in load_bookmarks():
            lb.insert(tk.END, f"★ {b['name']} ({b['url']})")
    
    reload_list()

    def do_delete():
        selection = lb.curselection()
        if selection:
            idx = selection[0]
            if delete_bookmark(idx):
                reload_list()
        else:
            # ÜBERSETZT: "Bitte erst ein Lesezeichen auswählen."
            messagebox.showwarning("Phoenix", get_text('msg_select_bm'))

    btn_frame = ttk.Frame(manager)
    btn_frame.pack(fill=tk.X, pady=10)
    
    # ÜBERSETZT: "Ausgewähltes löschen" und "Schließen"
    ttk.Button(btn_frame, text=get_text('bm_delete'), bootstyle="danger", command=do_delete).pack(side=tk.RIGHT, padx=20)
    ttk.Button(btn_frame, text=get_text('bm_close'), bootstyle="secondary", command=manager.destroy).pack(side=tk.RIGHT)

def refresh_bookmark_menu():
    """Aktualisiert das Dropdown-Menü in der Phoenix-Navigationsleiste."""
    try:
        bookmark_menu.delete(0, tk.END)
        bookmarks = load_bookmarks()
        
        if not bookmarks:
            bookmark_menu.add_command(label=get_text('bm_none'), state=tk.DISABLED)
        else:
            for b in bookmarks:
                bookmark_menu.add_command(
                    label=f"★ {b['name']}", 
                    command=lambda u=b['url']: navigate_to_gopher_item(u)
                )
        
        bookmark_menu.add_separator()
        bookmark_menu.add_command(label=get_text('bm_add_current'), command=add_current_to_bookmarks)
        bookmark_menu.add_command(label=get_text('bm_manage'), command=open_bookmark_manager)
    except NameError:
        pass


def add_current_to_bookmarks():
    """Fragt Namen ab und speichert die aktuelle URL (Internationalisiert)."""
    url = url_entry.get()
    if not url: 
        # ÜBERSETZT: "Keine URL vorhanden."
        messagebox.showwarning("Phoenix", get_text('msg_no_url'))
        return
    
    # ÜBERSETZT: "Lesezeichen hinzufügen" und "Name für dieses Lesezeichen:"
    name = simpledialog.askstring(get_text('ui_add_bm_title'), get_text('ui_add_bm_prompt'), parent=root)
    if name:
        item_type = url.split('#')[1] if '#' in url else '1'
        if save_bookmark(name, url, item_type):
            refresh_bookmark_menu()
        else:
            # ÜBERSETZT: "Lesezeichen existiert bereits."
            messagebox.showinfo("Phoenix", get_text('msg_bm_exists'))


# --- Netzwerk-Logik ---
DEFAULT_PORT_GOPHER = 70
DEFAULT_PORT_GOPHERS = 777
TIMEOUT = 5

def show_cert_in_inspector():
    """Zeigt die Details des aktuellen TLS-Zertifikats im Inspektor an."""
    global last_cert_data
    
    if not last_cert_data:
        # ÜBERSETZT: "Keine TLS-Zertifikatsdaten verfügbar."
        messagebox.showinfo("Phoenix", get_text('ins_no_cert'))
        return

    # Inspektor vorbereiten - Titel wird in update_inspector/apply_language gesetzt
    update_inspector(url_entry.get(), is_plus=False, item_type="🔒") 
    
    inspector_text.config(state=tk.NORMAL)
    inspector_text.delete('1.0', tk.END)
    
    # ÜBERSETZT: "🔒 TLS-ZERTIFIKATS-DETAILS"
    inspector_text.insert(tk.END, f"{get_text('ins_cert_title')}\n")
    inspector_text.insert(tk.END, "_"*60 + "\n\n")
    
    # --- UNIVERSAL ISSUER & SUBJECT PARSER ---
    def flatten_rdn(rdn_data):
        d = {}
        for rdn in rdn_data:
            for key, value in rdn:
                d[key] = value
        return d

    issuer_dict = flatten_rdn(last_cert_data.get('issuer', []))
    subject_dict = flatten_rdn(last_cert_data.get('subject', []))
    
    # Bestimmung des freundlichen Namens (Organisation vor CommonName)
    # Nutzt get_text für "Unbekannt"
    friendly_issuer = issuer_dict.get('organizationName', issuer_dict.get('commonName', 'Unknown'))
    common_name = subject_dict.get('commonName', 'Unknown')
    
    # Anzeige im Inspektor mit übersetzten Labels
    # f-Strings nutzen get_text für die Labels "Ausgestellt für", "Aussteller" etc.
    inspector_text.insert(tk.END, f"{get_text('ins_issued_to')}:\t{common_name}\n")
    inspector_text.insert(tk.END, f"{get_text('ins_issuer')}:\t{friendly_issuer}\n")
    inspector_text.insert(tk.END, f"{get_text('ins_valid_until')}:\t{last_cert_data.get('notAfter', 'Unknown')}\n")
    
    # Seriennummer
    serial = last_cert_data.get('serialNumber', 'N/A')
    inspector_text.insert(tk.END, f"{get_text('ins_serial')}:\t{serial}\n")
    
    # ÜBERSETZT: "Status: Die Verbindung ist verschlüsselt."
    inspector_text.insert(tk.END, f"\n{get_text('ins_encrypted')}\n")
    inspector_text.config(state=tk.DISABLED)



def fetch_binary_raw(url):
    """Lädt Rohdaten (Bilder/Binär) ohne UTF-8 Dekodierung."""
    parsed = urllib.parse.urlparse(url) # Hier heißt die Variable 'parsed'
    host = parsed.hostname
    port = parsed.port or (777 if parsed.scheme == 'gophers' else 70)
    
    # Typ-Präfix abschneiden (z.B. /g/bild.gif -> bild.gif)
    selector = (parsed.path[2:] if len(parsed.path) > 2 else "")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        if parsed.scheme == 'gophers':
            sock = ssl.create_default_context().wrap_socket(sock, server_hostname=host)
        
        sock.connect((host, port))
        sock.sendall(f"{selector}\r\n".encode('utf-8'))
        
        chunks = []
        while True:
            data = sock.recv(8192)
            if not data: break
            chunks.append(data)
        sock.close()
        return b"".join(chunks)
    except:
        return None



def fetch_gopher_plus_metadata(url):
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    port = parsed.port or (777 if parsed.scheme == 'gophers' else 70)
    selector = (parsed.path[2:] if len(parsed.path) > 2 else "")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0) 
        if parsed.scheme == 'gophers':
            sock = ssl.create_default_context().wrap_socket(sock, server_hostname=host)
        
        sock.connect((host, port))
        sock.sendall(f"{selector}\t!\r\n".encode('utf-8'))
        
        chunks = []
        while True:
            data = sock.recv(8192)
            if not data:
                break
            chunks.append(data)
        
        sock.close()
        
        full_response = b"".join(chunks).decode('utf-8', errors='replace')
        
        lines = []
        for line in full_response.splitlines():
            line = line.strip()
            if line == "." or not line:
                continue
            lines.append(line)
            
        # ÜBERSETZT: "Gopher+ Block ist leer oder ungültig."
        return "\n".join(lines) if lines else get_text('msg_plus_empty')
    except Exception as e:
        # ÜBERSETZT: "Fehler beim Abruf"
        return f"{get_text('msg_net_error')}: {str(e)}"



def update_inspector(url, is_plus, item_type):
    global inspector_window, inspector_text, current_inspector_url
    
    if not url: return
    current_inspector_url = url

    # Fenster-Management (Erstellen/Prüfen)
    if inspector_window is None or not inspector_window.winfo_exists():
        inspector_window = tk.Toplevel(root)
        inspector_window.title(get_text('ins_title'))
        inspector_window.geometry("600x450") # Höhe für Bilder optimiert
        
        st_container = ScrolledText(inspector_window, padding=10, autohide=True)
        st_container.pack(fill=tk.BOTH, expand=True)
        
        # Erst hier wird die Variable erstellt...
        inspector_text = st_container.text
        # ...und erst DANACH darf sie konfiguriert werden:
        inspector_text.config(font=("Consolas", 10), tabs=(150, 'left'))

    # Vorbereitung des Textfeldes
    inspector_text.config(state=tk.NORMAL)
    inspector_text.delete('1.0', tk.END)
    
    # Bildreferenz löschen (Memory Management)
    if hasattr(inspector_text, 'image_ref'): 
        del inspector_text.image_ref
    
    # Header-Informationen anzeigen
    inspector_text.insert(tk.END, f"URL: {url}\n")
    inspector_text.insert(tk.END, f"TYP: {item_type}\n")
    inspector_text.insert(tk.END, "_"*70 + "\n")
    
    # --- LOGIK A: BILD-VORSCHAU ---
    if item_type in ['g', 'I', 'j', 'p', '9']:
        inspector_text.insert(tk.END, get_text('ins_loading_img') + "\n")
        def img_worker(target_url):
            raw_data = fetch_binary_raw(target_url)
            if raw_data and current_inspector_url == target_url:
                try:
                    import base64
                    b64_data = base64.b64encode(raw_data).decode('ascii')
                    photo = tk.PhotoImage(data=b64_data)
                    def show_img():
                        if inspector_window and inspector_window.winfo_exists():
                            inspector_text.config(state=tk.NORMAL)
                            inspector_text.insert(tk.END, "\n")
                            inspector_text.image_create(tk.END, image=photo)
                            inspector_text.image_ref = photo 
                            inspector_text.config(state=tk.DISABLED)
                    root.after(0, show_img)
                except:
                    root.after(0, lambda: inspector_text.insert(tk.END, f"\n[{get_text('msg_format_err')}]\n"))
        threading.Thread(target=img_worker, args=(url,), daemon=True).start()

    # --- LOGIK B: GOPHER+ METADATEN ---
    if is_plus:
        inspector_text.insert(tk.END, "\n" + get_text('ins_loading_meta') + "\n")
        def meta_worker(target_url):
            meta_data = fetch_gopher_plus_metadata(target_url)
            if current_inspector_url == target_url:
                def update_ui():
                    if inspector_window and inspector_window.winfo_exists():
                        inspector_text.config(state=tk.NORMAL)
                        inspector_text.insert(tk.END, "\n" + meta_data)
                        inspector_text.config(state=tk.DISABLED)
                root.after(0, update_ui)
        threading.Thread(target=meta_worker, args=(url,), daemon=True).start()
    
    # --- LOGIK C: FALLBACK ---
    elif item_type not in ['g', 'I']:
        inspector_text.insert(tk.END, get_text('ins_type_0'))

    inspector_text.config(state=tk.DISABLED)

def handle_gopher_request(url):
    if isinstance(url, list): url = url[0]
    parsed_url = urllib.parse.urlparse(url)
    scheme = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port or (DEFAULT_PORT_GOPHERS if scheme == 'gophers' else DEFAULT_PORT_GOPHER)
    
    if parsed_url.path and len(parsed_url.path) >= 2:
        item_type = parsed_url.path[1]
    else:
        item_type = parsed_url.fragment if parsed_url.fragment else '1'

    selector = (parsed_url.path[2:] if len(parsed_url.path) > 2 else "")
    
    if scheme not in ['gopher', 'gophers']:
        messagebox.showerror("Phoenix", get_text('msg_bad_protocol'))
        return None

    # --- INITIALISIERUNG DER SICHERHEITS-VARIABLEN ---
    security_status = "none"
    cert_data = None
        
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        
        if scheme == 'gophers':
            try:
                # STUFE 1: Streng (Grün)
                context = ssl.create_default_context()
                conn = context.wrap_socket(sock, server_hostname=host)
                conn.connect((host, port))
                security_status = "secure"
            except (ssl.SSLCertVerificationError, ssl.SSLError):
                # STUFE 2: Locker (Gelb) bei selbstsignierten/abgelaufenen Zertifikaten
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(TIMEOUT)
                context = ssl._create_unverified_context()
                conn = context.wrap_socket(sock, server_hostname=host)
                conn.connect((host, port))
                security_status = "warning"
            
            # --- ROBUSTER ZERTIFIKATS-ABRUF FÜR PORTABLE PYTHON ---
            try:
                # Versuch 1: Standard-Abfrage (funktioniert bei 'secure')
                cert_data = conn.getpeercert()
                
                # Versuch 2: Falls leer (bei 'warning'), baue ich ein Info-Paket manuell
                # Dies verhindert Fehler, da 'DER_cert_to_dict' in deinem Python fehlt
                if not cert_data:
                    # Prüfen, ob technisch eine TLS-Verbindung besteht
                    cipher = conn.cipher()
                    if cipher:
                        cert_data = {
                            'subject': [[['commonName', host]]],
                            'issuer': [[['commonName', 'Self-signed Certificate']]],
                            'notAfter': f'Aktiv ({cipher[1]})'
                        }
            except Exception:
                cert_data = None
        else:
            # STUFE 3: Unverschlüsselt (Blau/Grau)
            conn = sock
            conn.connect((host, port))
        
        request_data = selector
        if parsed_url.query:
            request_data = f"{selector}\t{urllib.parse.unquote(parsed_url.query)}"
        
        conn.sendall((request_data + "\r\n").encode('utf-8'))
        
        response_bytes = b""
        while True:
            data = conn.recv(4096)
            if not data: break
            response_bytes += data
        
        # Rückgabe von 7 Werten für die Phoenix-UI
        return response_bytes.decode('utf-8', errors='replace'), scheme, host, port, item_type, security_status, cert_data

    except Exception as e:
        messagebox.showerror(get_text('msg_net_error'), f"Error: {e}")
        return None





# --- GUI Logik ---
history = []
history_index = -1


def ask_for_query(base_url):
    # Bewährter Hack für die Breite
    query = simpledialog.askstring(
        get_text('search_title'), 
        get_text('search_prompt') + " " * 50 + "\n", 
        parent=root
    )
    if query:
        # Ich säubere den Suchbegriff, lasse die Leerzeichen aber als ECHTE Leerzeichen
        search_term = query.strip()
        
        # Ich nehme die Basis-URL (alles vor einem eventuellen ? oder #)
        base = base_url.split('#')[0].split('?')[0]
        
        # Ich baue die URL mit einem Fragezeichen, aber OHNE Prozent-Kodierung für den Suchbegriff
        # So bleibt "gopher tls" im URL-String als "gopher tls" erhalten
        final_url = f"{base}?{search_term}"
        
        navigate_to_gopher_item(final_url)


def navigate_to_gopher_item(url):
    # url kann eine Liste oder ein String sein
    clean_url = url[0] if isinstance(url, list) else url.split('#')[0]
    
    url_entry.delete(0, tk.END)
    url_entry.insert(0, clean_url)
    
    # Variable muss clean_url sein
    if clean_url.lower().startswith("gophers://"):
        url_entry.configure(style="Secure.TEntry")
    else:
        url_entry.configure(style="TEntry")
        
    fetch_gopher_data(False)



def go_back():
    global history_index
    if history_index > 0:
        history_index -= 1
        new_url = history[history_index]
        # Falls URL als Liste gespeichert wurde, erstes Element nehmen
        new_url_str = new_url[0] if isinstance(new_url, list) else new_url
        
        url_entry.delete(0, tk.END)
        url_entry.insert(0, new_url_str)
        
        if str(new_url_str).lower().startswith("gophers://"):
            url_entry.configure(style="Secure.TEntry")
        else:
            url_entry.configure(style="TEntry")
            
        fetch_gopher_data(True)

def display_text_file(raw_data):
    """Zeigt Gopher-Typ 0 (Text) ohne jegliche Zeilen-Manipulation an."""
    txt = result_area.text
    txt.config(state=tk.NORMAL)
    txt.delete('1.0', tk.END)
    
    # Gopher-Server senden am Ende oft einen Punkt auf einer neuen Zeile: \r\n.\r\n
    # Ich entferne NUR dieses Ende-Signal, falls es existiert.
    if raw_data.endswith("\r\n.\r\n"):
        clean_data = raw_data[:-5]
    elif raw_data.endswith("\n.\n"):
        clean_data = raw_data[:-3]
    else:
        clean_data = raw_data


    # Keine Schleife (for line in lines), kein line[1:] !
    txt.insert(tk.END, clean_data)
    
    txt.config(state=tk.DISABLED)
    status_label.config(text="Dokument view", bootstyle="info")

def parse_gopher_menu(raw_data, current_scheme, current_host, current_port):
    global current_enhanced_data
    
    txt = result_area.text
    txt.config(state=tk.NORMAL)
    txt.delete('1.0', tk.END)
    
    # 1. MARKER-CHECK
    MARKER = "enhanced:experience"
    if MARKER in raw_data.lower() and not current_enhanced_data:
        p = urllib.parse.urlparse(url_entry.get())
        trigger_enhanced_engine(current_host, current_port, p.path, current_scheme)
    
    # 2. STYLE-TAGS KONFIGURATION
    link_color = style.colors.primary
    txt.tag_configure("link", foreground=link_color, underline=False)
    
    # Phoenix Styles (Header, Divider, Accent)
    txt.tag_configure("phx_header", font=("Consolas", 11, "bold"), foreground=style.colors.primary)
    txt.tag_configure("phx_divider", font=("Consolas", 11), foreground=style.colors.secondary)
    txt.tag_configure("phx_accent", font=("Consolas", 11, "bold"), foreground=style.colors.info)
    txt.tag_configure("phx_warning", foreground=style.colors.warning, font=("Consolas", 11, "bold"))
    txt.tag_configure("phx_success", foreground=style.colors.success, font=("Consolas", 11, "bold"))
    txt.tag_configure("phx_comment", foreground="#8b949e", font=("Consolas", 11, "italic"))
    txt.tag_configure("phx_danger", foreground=style.colors.danger, font=("Consolas", 11, "bold"))
    txt.tag_configure("phx_info", foreground=style.colors.info, font=("Consolas", 11))
    txt.tag_configure("phx_secondary", foreground=style.colors.secondary, font=("Consolas", 11))
    txt.tag_configure("phx_inverse", background=style.colors.primary, foreground=style.colors.bg)
    
    txt.tag_bind("link", "<Enter>", lambda _: txt.config(cursor="hand2"))
    txt.tag_bind("link", "<Leave>", lambda _: txt.config(cursor=""))
    
    lines = raw_data.splitlines()
    has_plus = False

    for row_idx, line in enumerate(lines):
        if not line or line.strip() == ".": continue
        
        # 3. STYLE-MAPPING (JSON)
        applied_tags = []
        if current_enhanced_data and "rules" in current_enhanced_data:
            rule = current_enhanced_data["rules"].get(str(row_idx))
            if rule == "header": applied_tags.append("phx_header")
            elif rule == "divider": applied_tags.append("phx_divider")
            elif rule == "accent": applied_tags.append("phx_accent")
            elif rule == "warning": applied_tags.append("phx_warning")
            elif rule == "success": applied_tags.append("phx_success")
            elif rule == "comment": applied_tags.append("phx_comment")
            elif rule == "danger": applied_tags.append("phx_danger")     
            elif rule == "info": applied_tags.append("phx_info")         
            elif rule == "secondary": applied_tags.append("phx_secondary") 
            elif rule == "inverse": applied_tags.append("phx_inverse")   


        item_type = line[0]
        content = line[1:]
        parts = content.split('\t')

        if len(parts) >= 3:
            # FEHLERBEHEBUNG: Korrekte Zuweisung der Listen-Elemente
            display_text = parts[0]
            selector = parts[1]
            item_host = parts[2]
            
            try: item_port = int(parts[3]) if len(parts) > 3 else current_port
            except: item_port = current_port
            
            is_plus = len(parts) > 4 and '+' in parts[4]
            if is_plus: has_plus = True

            link_scheme = current_scheme if item_host.lower() == current_host.lower() else "gopher"
            if not selector.startswith('/'): selector = '/' + selector
            target_url = f"{link_scheme}://{item_host}:{item_port}/{item_type}{selector}"
            
            if item_type == 'i':
                if "phx_divider" in applied_tags:
                    txt.insert(tk.END, "─" * 60 + "\n", applied_tags)
                else:
                    # ZENTRIERUNG RETTEN: Leerzeichen und Text getrennt stylen
                    leading_spaces = display_text[:len(display_text) - len(display_text.lstrip())]
                    actual_text = display_text.lstrip()
                    txt.insert(tk.END, leading_spaces) # In Standard-Consolas
                    txt.insert(tk.END, actual_text + "\n", tuple(applied_tags)) # Im Style
            
            elif item_type in '017gdI954hUspj': 
                tag = f"link_{hash(target_url)}"
                txt.tag_configure(tag, foreground=link_color)
                icon = TYPE_ICONS.get(item_type, '• ')
                
                leading_spaces = display_text[:len(display_text) - len(display_text.lstrip())]
                actual_text = display_text.lstrip()
                
                txt.insert(tk.END, icon + leading_spaces) 
                txt.insert(tk.END, actual_text + (" [+]" if is_plus else "") + "\n", (tag, "link") + tuple(applied_tags))
                
                # Bindings für Inspector & Klick
                def on_enter(e, u=target_url, p=is_plus, t=item_type):
                    if not (e.state & 0x0001): return 
                    if 'inspector_timer' in globals() and inspector_timer:
                        root.after_cancel(inspector_timer)
                    globals()['inspector_timer'] = root.after(10, lambda: update_inspector(u, p, t))
                def on_leave(e):
                    if 'inspector_timer' in globals() and inspector_timer:
                        root.after_cancel(inspector_timer)
                
                txt.tag_bind(tag, "<Enter>", on_enter)
                txt.tag_bind(tag, "<Leave>", on_leave)

                if item_type == '7':
                    txt.tag_bind(tag, "<Button-1>", lambda e, u=target_url: ask_for_query(u))
                elif item_type in 'hU':
                    import webbrowser
                    txt.tag_bind(tag, "<Button-1>", lambda e, u=target_url: webbrowser.open(u))
                elif item_type in '954dgIsp':
                    txt.tag_bind(tag, "<Button-1>", lambda e, u=target_url: start_binary_download(u))
                else:
                    txt.tag_bind(tag, "<Button-1>", lambda e, u=target_url: navigate_to_gopher_item(u))
            else:
                txt.insert(tk.END, f"({item_type}) {display_text}\n", applied_tags)
        else:
            # ZENTRIERUNG RETTEN für reine Infozeilen (Construction Text)
            # Ich nehme den content (alles nach dem 'i')
            leading_spaces = content[:len(content) - len(content.lstrip())]
            actual_text = content.lstrip()
            txt.insert(tk.END, leading_spaces) # Leerzeichen in Consolas
            txt.insert(tk.END, actual_text + "\n", tuple(applied_tags)) # Text im Style

    status_label.config(text="Gopher+" if has_plus else "Gopher0", bootstyle="success" if has_plus else "secondary")
    txt.config(state=tk.DISABLED)





def fetch_gopher_data(is_history_navigation=False):
    global history, history_index, last_cert_data, current_enhanced_data
    current_url = url_entry.get()
    if not current_url: return
    
    clean_url_string = current_url.split('#')[0]
    
    # Style-Reset nur bei echter Neu-Navigation
    if not is_history_navigation:
        current_enhanced_data = {}
        save_config(clean_url_string)

    res = handle_gopher_request(clean_url_string)
    if res:
        raw_data, current_scheme, current_host, current_port, item_type, sec_status, cert_info = res
        last_cert_data = cert_info 

        # Sicherheits-UI (Schloss & Farbe)
        if sec_status == "secure":
            security_btn.configure(bootstyle="success")
            url_entry.configure(style="Secure.TEntry")
        elif sec_status == "warning":
            security_btn.configure(bootstyle="warning")
            url_entry.configure(style="TEntry")
        else:
            security_btn.configure(bootstyle="secondary")
            url_entry.configure(style="TEntry")

        # Phoenix-Weiche
        if item_type == '0':
            display_text_file(raw_data)
        else:
            parse_gopher_menu(raw_data, current_scheme, current_host, current_port)
            
        # Historie
        if not is_history_navigation:
            if not history or history[history_index] != clean_url_string:
                history = history[:history_index + 1] + [clean_url_string]
                history_index = len(history) - 1
        
        back_btn.config(state=tk.NORMAL if history_index > 0 else tk.DISABLED)






# --- GUI Setup mit ttkbootstrap ---
style = ttk.Style(theme="yeti") # Themes: flatly, darkly, superhero, morph, cosmo, lumen, pulse, yeti
# --- Erstellt ein spezielles grünes Design für das Eingabefeld --- 
style.configure("Secure.TEntry", fieldbackground="#e6ffed")

root = style.master
# --- Phoenix-Icon setzen --- 
try:
    # Ich erstelle ein PhotoImage aus den Base64-Daten
    icon_img = tk.PhotoImage(data=PHOENIX_LOGO)
    root.iconphoto(True, icon_img)
except Exception as e:
    print(f"Icon konnte nicht geladen werden: {e}")

root.title("Phoenix - TLS Gopher+ Client")
root.geometry("1100x850")

# --- Header --- 
hdr_frame = ttk.Frame(root, padding=10)
hdr_frame.pack(fill=X)

back_btn = ttk.Button(hdr_frame, text="", command=go_back, bootstyle="outline-primary")
back_btn.pack(side=LEFT, padx=5)

url_entry = ttk.Entry(hdr_frame, font=("Segoe UI", 11))

# --- Das Sicherheits-Schloss (Links neben der Adressleiste) --- 
security_btn = ttk.Button(hdr_frame, text="🔒", width=3, bootstyle="secondary", command=show_cert_in_inspector)
security_btn.pack(side=tk.LEFT, padx=(5, 0))
url_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
url_entry.insert(0, load_config())
url_entry.bind("<Return>", lambda e: fetch_gopher_data())

load_btn = ttk.Button(hdr_frame, text=get_text('ui_load'), command=fetch_gopher_data, bootstyle="outline-primary")
load_btn.pack(side=LEFT, padx=5)

# --- Lesezeichen-Menü (Dropdown) ---
bm_btn = ttk.Menubutton(hdr_frame, text=get_text('ui_bookmarks'), bootstyle="outline-primary")
bm_btn.pack(side=LEFT, padx=5)

# --- Theme-Umschalter --- 
theme_btn = ttk.Menubutton(hdr_frame, text="Theme", bootstyle="outline-primary", width=12)
theme_btn.pack(side=tk.LEFT, padx=5)

theme_menu = tk.Menu(theme_btn, tearoff=0)
theme_btn["menu"] = theme_menu

# --- Diese Namen sind intern bei ttkbootstrap fest hinterlegt --- 
available_themes = [
    "yeti", "flatly", "lumen", "sandstone", "minty", "pulse",  # Hell
    "darkly", "superhero", "solar", "cyborg", "vapor", "morph" # Dunkel
]


for t_name in available_themes:
    theme_menu.add_command(
        label=t_name.capitalize(), 
        command=lambda t=t_name: change_theme(t)
    )


# --- Sprach-Umschalter (Dropdown) --- 
lang_btn = ttk.Menubutton(hdr_frame, text=CURR_LANG_CODE, bootstyle="outline-primary", width=3)
lang_btn.pack(side=tk.LEFT, padx=5)

lang_menu = tk.Menu(lang_btn, tearoff=0)
lang_btn["menu"] = lang_menu

# --- Info Button --- 
info_btn = ttk.Button(hdr_frame, text="ℹ", width=3, bootstyle="outline-primary", command=show_client_info)
info_btn.pack(side=LEFT, padx=5)

bookmark_menu = tk.Menu(bm_btn, tearoff=0)
bm_btn["menu"] = bookmark_menu

# --- Das Menü beim Start einmalig mit den JSON-Daten füllen --- 
root.after(200, refresh_bookmark_menu)


status_label = ttk.Label(hdr_frame, text=get_text('ui_status_ready'), font=("Helvetica", 9, "bold"), padding=5)
status_label.pack(side=RIGHT)

# --- Inhaltsbereich (ScrolledText von ttkbootstrap) --- 
# Hier bleibt width=100 für die Gopher-Konformität erhalten
# Ich nutze einen Frame als Container, um die Breite zu erzwingen
container = ttk.Frame(root)
container.pack(fill=tk.Y, expand=True) # Container wächst nur in die Höhe

result_area = ScrolledText(container, padding=20, autohide=True)
result_area.pack(fill=tk.Y, expand=True) # Textbereich füllt die Höhe des Containers

# --- Hier wird die Breite auf exakt 100 Zeichen FIXIERT --- 
result_area.text.config(font=("Consolas", 11))


def on_closing():
    save_config(url_entry.get().split('#')[0])
    root.destroy()

# --- Vor der Sprach-Initialisierung das Theme laden --- 
config = configparser.ConfigParser()
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)
    saved_theme = config.get(CONFIG_SECTION, 'theme', fallback='yeti')
    # Ich rufe change_theme auf, um auch die Textfarben zu setzen
    # Da dies vor dem Hauptfenster passiert, nutze ich after()
    root.after(0, lambda: change_theme(saved_theme))

# --- 1. Sprachen laden --- 
load_languages()

# --- 2. Sprach-Menü dynamisch aufbauen (der "Klu") --- 
build_lang_menu()

# --- 3. Texte initial setzen --- 
apply_language()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.after(100, fetch_gopher_data)
root.after(200, refresh_bookmark_menu)
root.mainloop()
