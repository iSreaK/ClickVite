import customtkinter as ctk
import pyautogui
import threading
from pynput import keyboard
import time

# CRUCIAL : Désactiver le délai de PyAutoGUI
pyautogui.PAUSE = 0

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("ClickVite")
        self.root.geometry("480x800")
        self.root.resizable(False, False)
        
        self.is_running = False
        self.click_count = 0
        self.current_hotkey = None
        self.hotkey_display = "F6"
        self.capturing_key = False
        
        # Couleurs purple theme moderne
        self.colors = {
            "bg": "#0f0f1e",
            "card": "#1a1a2e",
            "card_hover": "#252537",
            "primary": "#9d4edd",
            "primary_hover": "#b565ff",
            "accent": "#e0aaff",
            "text": "#ffffff",
            "text_secondary": "#b8b8c8",
            "success": "#00f5a0",
            "danger": "#ff006e",
            "border": "#2d2d45"
        }
        
        # Hiérarchie typographique unifiée
        self.fonts = {
            "title": ctk.CTkFont(size=32, weight="bold"),          # Titre principal
            "card_title": ctk.CTkFont(size=13, weight="bold"),     # Titres de cartes
            "value": ctk.CTkFont(size=48, weight="bold"),          # Valeurs principales (CPS)
            "counter": ctk.CTkFont(size=32, weight="bold"),        # Compteur (réduit)
            "label": ctk.CTkFont(size=11),                         # Labels/sous-textes
            "button": ctk.CTkFont(size=14, weight="bold"),         # Texte des boutons
            "button_large": ctk.CTkFont(size=18, weight="bold"),   # Bouton START/STOP
            "display": ctk.CTkFont(size=20, weight="bold"),        # Affichage hotkey (réduit)
            "info": ctk.CTkFont(size=10)                           # Info footer
        }
        
        ctk.set_appearance_mode("dark")
        self.root.configure(bg=self.colors["bg"])
        
        # Créer le background
        self.create_background()
        
        # Interface
        self.create_ui()
        
        # Setup hotkey listener après l'UI
        self.setup_hotkey_listener()
        
    def create_background(self):
        """Crée un fond dégradé"""
        canvas = ctk.CTkCanvas(self.root, width=480, height=800, 
                               bg=self.colors["bg"], highlightthickness=0)
        canvas.place(x=0, y=0)
        
        # Gradient simple
        for i in range(800):
            ratio = i / 800
            color = self.interpolate_color("#0a0a14", "#1a1a2e", ratio)
            canvas.create_line(0, i, 480, i, fill=color, width=1)
    
    def interpolate_color(self, color1, color2, ratio):
        """Interpolation entre deux couleurs hex"""
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_ui(self):
        # Container principal
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Inner container
        inner_container = ctk.CTkFrame(main_container, fg_color="transparent")
        inner_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header
        header_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Auto Clicker",
            font=self.fonts["title"],
            text_color=self.colors["accent"]
        )
        title.pack()
        
        # === CARD 1: Speed Control ===
        speed_card = self.create_card(inner_container, "⚡ Speed Control")
        
        self.cps_value_label = ctk.CTkLabel(
            speed_card,
            text="5",
            font=self.fonts["value"],
            text_color=self.colors["primary"]
        )
        self.cps_value_label.pack(pady=(15, 5))
        
        cps_unit = ctk.CTkLabel(
            speed_card,
            text="clicks per second",
            font=self.fonts["label"],
            text_color=self.colors["text_secondary"]
        )
        cps_unit.pack(pady=(0, 15))
        
        self.cps_slider = ctk.CTkSlider(
            speed_card,
            from_=1,
            to=50,
            number_of_steps=49,
            command=self.update_cps_label,
            width=340,
            height=18,
            button_color=self.colors["primary"],
            button_hover_color=self.colors["primary_hover"],
            progress_color=self.colors["primary"],
            fg_color=self.colors["border"]
        )
        self.cps_slider.set(5)
        self.cps_slider.pack(pady=(0, 15))
        
        # === CARD 2: Click Type ===
        click_card = self.create_card(inner_container, "🎯 Click Type")
        
        self.click_type = ctk.CTkSegmentedButton(
            click_card,
            values=["Left", "Right", "Middle"],
            selected_color=self.colors["primary"],
            selected_hover_color=self.colors["primary_hover"],
            unselected_color=self.colors["border"],
            unselected_hover_color=self.colors["card_hover"],
            text_color=self.colors["text"],
            font=self.fonts["button"],
            height=45
        )
        self.click_type.set("Left")
        self.click_type.pack(pady=(15, 15), padx=20, fill="x")
        
        # === CARD 3: Hotkey ===
        hotkey_card = self.create_card(inner_container, "⌨️ Hotkey")
        
        hotkey_container = ctk.CTkFrame(hotkey_card, fg_color="transparent")
        hotkey_container.pack(pady=(15, 15), padx=20, fill="x")
        
        self.hotkey_btn = ctk.CTkButton(
            hotkey_container,
            text=f"{self.hotkey_display}",
            font=self.fonts["display"],
            fg_color=self.colors["border"],
            hover_color=self.colors["card_hover"],
            text_color=self.colors["accent"],
            height=55,  # RÉDUIT à 55px
            corner_radius=12,
            command=self.start_key_capture
        )
        self.hotkey_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        capture_btn = ctk.CTkButton(
            hotkey_container,
            text="Change",
            font=self.fonts["button"],
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            width=100,
            height=55,  # RÉDUIT à 55px
            corner_radius=12,
            command=self.start_key_capture
        )
        capture_btn.pack(side="right")
        
        # === CARD 4: Click Counter ===
        counter_card = self.create_card(inner_container, "📊 Total Clicks")
        
        counter_content = ctk.CTkFrame(counter_card, fg_color="transparent")
        counter_content.pack(pady=(15, 15), padx=20, fill="x")
        
        # Compteur - MÊME HAUTEUR 55px
        counter_display = ctk.CTkFrame(
            counter_content,
            fg_color=self.colors["border"],
            corner_radius=12,
            height=55  # RÉDUIT à 55px
        )
        counter_display.pack(side="left", fill="both", expand=True, padx=(0, 10))
        counter_display.pack_propagate(False)  # Force la hauteur
        
        self.counter_label = ctk.CTkLabel(
            counter_display,
            text="0",
            font=self.fonts["counter"],  # Police réduite à 32px
            text_color=self.colors["accent"]
        )
        self.counter_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Bouton Reset - MÊME HAUTEUR 55px
        reset_btn = ctk.CTkButton(
            counter_content,
            text="RESET",
            font=self.fonts["button"],
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            text_color=self.colors["text"],
            width=100,
            height=55,  # RÉDUIT à 55px
            corner_radius=12,
            command=self.reset_counter
        )
        reset_btn.pack(side="right")
        
        # === Status ===
        status_container = ctk.CTkFrame(
            inner_container,
            fg_color=self.colors["card"],
            corner_radius=15,
            border_width=2,
            border_color=self.colors["border"]
        )
        status_container.pack(fill="x", pady=(0, 12))
        
        status_inner = ctk.CTkFrame(status_container, fg_color="transparent")
        status_inner.pack(pady=15)
        
        self.status_indicator = ctk.CTkLabel(
            status_inner,
            text="●",
            font=ctk.CTkFont(size=18),
            text_color=self.colors["text_secondary"]
        )
        self.status_indicator.pack(side="left", padx=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            status_inner,
            text="Ready",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        self.status_label.pack(side="left")
        
        # === Bouton START ===
        self.start_btn = ctk.CTkButton(
            inner_container,
            text="START",
            font=self.fonts["button_large"],
            fg_color=self.colors["success"],
            hover_color="#00cc80",
            text_color="#000000",
            height=65,
            corner_radius=15,
            command=self.toggle_clicking
        )
        self.start_btn.pack(fill="x", pady=(0, 12))
        
        # Info footer
        self.info_label = ctk.CTkLabel(
            inner_container,
            text=f"Press {self.hotkey_display} anywhere to start/stop",
            font=self.fonts["info"],
            text_color=self.colors["text_secondary"]
        )
        self.info_label.pack()
    
    def create_card(self, parent, title):
        """Crée une carte avec titre"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["card"],
            corner_radius=15,
            border_width=2,
            border_color=self.colors["border"]
        )
        card.pack(fill="x", pady=(0, 12))
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=self.fonts["card_title"],
            text_color=self.colors["text_secondary"]
        )
        title_label.pack(anchor="w", padx=20, pady=(12, 0))
        
        return card
    
    def start_key_capture(self):
        """Démarre la capture de touche"""
        if self.capturing_key:
            return
        
        self.capturing_key = True
        self.hotkey_btn.configure(
            text="Press any key...",
            text_color=self.colors["primary"]
        )
        
        # Stop le listener actuel
        if hasattr(self, 'key_listener') and self.key_listener:
            self.key_listener.stop()
        
        def on_key_press(key):
            if not self.capturing_key:
                return
            
            # Capturer la touche
            try:
                if hasattr(key, 'char') and key.char:
                    captured = key.char.upper()
                    self.current_hotkey = key
                else:
                    key_name = str(key).replace('Key.', '')
                    captured = key_name.upper()
                    self.current_hotkey = key
                
                self.hotkey_display = captured
                self.root.after(0, self.finish_capture)
                
            except Exception as e:
                print(f"Erreur capture: {e}")
        
        # Listener temporaire
        self.temp_listener = keyboard.Listener(on_press=on_key_press)
        self.temp_listener.start()
    
    def finish_capture(self):
        """Termine la capture"""
        self.capturing_key = False
        
        if hasattr(self, 'temp_listener'):
            self.temp_listener.stop()
        
        self.hotkey_btn.configure(
            text=self.hotkey_display,
            text_color=self.colors["accent"]
        )
        
        # Mettre à jour le label info
        self.info_label.configure(text=f"Press {self.hotkey_display} anywhere to start/stop")
        
        print(f"Hotkey définie: {self.current_hotkey}")
        
        # Redémarrer le listener
        self.setup_hotkey_listener()
    
    def setup_hotkey_listener(self):
        """Configure le listener de hotkey"""
        if hasattr(self, 'key_listener') and self.key_listener:
            self.key_listener.stop()
        
        def on_key_press(key):
            if key == self.current_hotkey:
                print(f"Hotkey pressée: {key}")
                self.root.after(0, self.toggle_clicking)
        
        self.key_listener = keyboard.Listener(on_press=on_key_press)
        self.key_listener.start()
        print(f"Listener démarré pour: {self.current_hotkey}")
    
    def update_cps_label(self, value):
        """Met à jour l'affichage des CPS"""
        self.cps_value_label.configure(text=str(int(value)))
    
    def get_button_type(self):
        """Retourne le type de bouton"""
        button_map = {"Left": "left", "Right": "right", "Middle": "middle"}
        return button_map.get(self.click_type.get(), "left")
    
    def toggle_clicking(self):
        """Toggle start/stop"""
        if self.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self):
        """Démarre l'auto-clicker"""
        cps = int(self.cps_slider.get())
        
        self.is_running = True
        self.start_btn.configure(
            text="STOP",
            fg_color=self.colors["danger"],
            hover_color="#cc0057"
        )
        self.status_indicator.configure(text_color=self.colors["success"])
        self.status_label.configure(
            text="Running",
            text_color=self.colors["success"]
        )
        
        self.click_thread = threading.Thread(target=self.click_loop, args=(cps,))
        self.click_thread.daemon = True
        self.click_thread.start()
    
    def click_loop(self, cps):
        """Boucle de clic ultra-rapide"""
        button = self.get_button_type()
        interval = 1.0 / cps
        next_click = time.perf_counter()
        
        while self.is_running:
            current_time = time.perf_counter()
            
            if current_time >= next_click:
                pyautogui.click(button=button)
                self.click_count += 1
                self.root.after(0, self.update_counter)
                next_click += interval
            
            time.sleep(0.0001)
    
    def stop_clicking(self):
        """Arrête l'auto-clicker"""
        self.is_running = False
        self.start_btn.configure(
            text="START",
            fg_color=self.colors["success"],
            hover_color="#00cc80"
        )
        self.status_indicator.configure(text_color=self.colors["text_secondary"])
        self.status_label.configure(
            text="Ready",
            text_color=self.colors["text_secondary"]
        )
    
    def reset_counter(self):
        """Reset le compteur"""
        self.click_count = 0
        self.update_counter()
    
    def update_counter(self):
        """Met à jour le compteur"""
        self.counter_label.configure(text=str(self.click_count))

if __name__ == "__main__":
    root = ctk.CTk()
    app = AutoClicker(root)
    root.mainloop()
