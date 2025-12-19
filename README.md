# 🖱️ ClickVite - Auto Clicker

Un auto-clicker moderne et élégant avec interface graphique dark/purple. Simple, rapide et efficace.

## ✨ Fonctionnalités

- ⚡ **Vitesse réglable** - De 1 à 50 clics par seconde
- 🎯 **Types de clics** - Gauche, droit ou milieu
- ⌨️ **Hotkey personnalisable** - Démarre/arrête avec n'importe quelle touche
- 📊 **Compteur en temps réel** - Suivi du nombre de clics
- 🎨 **Interface moderne** - Thème dark purple élégant
- 🚀 **Ultra-rapide** - Optimisé pour des performances maximales

## 📥 Installation rapide

### Option 1 : Utiliser l'exécutable (Recommandé)

1. Télécharge `ClickVite.exe` depuis la partie **Créer l'exécutable toi-même**
2. Double-clique sur l'exe
3. C'est tout ! Aucune installation requise ni python ✅

> **Note :** Si Windows Defender bloque l'exe, clique sur "Plus d'infos" puis "Exécuter quand même". C'est normal pour les applications non signées.

### Option 2 : Lancer depuis le code source

**Prérequis :**
- Python 3.11+
- pip

**Installation :**
1. Clone le repo 
`git clone https://github.com/iSreaK/ClickVite.git`
`cd ClickVite`

2. Installe les dépendances
`pip install -r requirements.txt`

3. Lance l'application
`python autoclicker.py`

## 🎮 Comment l'utiliser

1. **Configure la vitesse** avec le slider (1-50 CPS)
2. **Choisis le type de clic** : Gauche, Droit ou Milieu
3. **Définis ta hotkey** en cliquant sur "Change" puis appuie sur une touche
4. **Lance l'auto-clicker** :
   - Clique sur le bouton **START**, ou
   - Appuie sur ta hotkey (F6 par défaut)
5. **Positionne ta souris** où tu veux cliquer
6. **Arrête quand tu veux** avec ta hotkey ou le bouton STOP

## 🛠️ Créer l'exécutable toi-même

### Si tu veux compiler l'exe :

1. Installe PyInstaller
`pip install pyinstaller`

2. Crée l'exécutable
`python -m PyInstaller --onefile --windowed --icon=icon.ico ClicVite.py`

**Ton exe sera dans le dossier dist/**

## 📦 Technologies utilisées

- **CustomTkinter** - Interface graphique moderne
- **PyAutoGUI** - Automatisation des clics
- **Pynput** - Écoute des hotkeys
- **Pillow** - Gestion des icônes

## 🎯 Cas d'usage

- Automatisation de tâches répétitives
- Tests d'applications
- Jeux qui nécessitent des clics répétés
- Farming de ressources

## ⚠️ Avertissement

Cet outil est destiné à des fins éducatives et d'automatisation légitimes. L'utilisation d'auto-clickers peut être interdite dans certains jeux ou applications en ligne. Utilise-le de manière responsable et conforme aux conditions d'utilisation des services que tu utilises.

## 📝 Licence

MIT License - Libre d'utilisation