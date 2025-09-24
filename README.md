# StreamEvents

Aplicació Django per gestionar esdeveniments i usuaris
(extensible): base educativa amb bones practiques
(entorns, estructura, separació de templates/static,
etc.). Opcionalment es pot integrar MongoDB (via djongo)
més endavant.

## ✨ Objectius
- Practicar un projecte Django modular.
- Treballar amb un usuari personalitzat (app users).
- Organitzar templates, estàtics i media correctament.
- Introduir fitxers d'entorn (.env) i bones practiques
Git.
- Preparar el terreny per a futures funcionalitats (API,
auth avançada, etc.).

## 🧱 Stack Principal
- Python 3.13
- Django 5.x
- SQLite (per defecte) / MongoDB (opcional via Djongo)
- HTML, CSS i JS (templates i estàtics)
- Git & GitHub (control de versions)

## 📂 Estructura Simplificada
streamevents/
│── config/              # Configuració principal (settings, urls, etc.)
│── users/               # App personalitzada d'usuaris
│── templates/           # Plantilles globals (base.html, layouts, etc.)
│── static/              # Fitxers estàtics (css, js, img)
│── media/               # Pujades d’usuari (IGNORAT al Git)
│── fixtures/            # (Opcional) JSON amb dades d'exemple
│── seeds/               # (Opcional) Scripts per omplir dades
│── requirements.txt     # Dependències del projecte
│── .env                 # Variables d’entorn (privat)
│── env.example          # Exemple d’entorn (sense secrets)
│── README.md            # Documentació del projecte

## ✅ Requisits previs
- Python 3.13 instal·lat
- Git instal·lat
- Entorn virtual creat (`python -m venv venv`)

## 🚀 Instal·lació ràpida
```bash
# Clonar el repositori
git clone https://github.com/jasonokoro10/streamevents.git
cd streamevents

# Activar l'entorn virtual
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# Instal·lar dependències
pip install -r requirements.txt

# Migracions i superusuari
python manage.py migrate
python manage.py createsuperuser

---

### 7. Variables d'entorn
```markdown
## 🔐 Variables d'entorn (env.example)
Crea un fitxer `.env` amb informació sensible. Exemple:

```env
DEBUG=True
SECRET_KEY=canvia_aqui_la_clau
DATABASE_URL=sqlite:///db.sqlite3
# O opcional per MongoDB:
# DATABASE_URL=mongodb://localhost:27017/streamevents_db

---

### 8. Superusuari
```markdown
## 👤 Superusuari
Per accedir al panell d’administració:

```bash
python manage.py createsuperuser

---

### 9. Migrar a MongoDB
```markdown
## 🗃️ Migrar a MongoDB (opcional futur)
- Instal·lar `djongo` i `pymongo`
- Canviar `settings.py` → `ENGINE = 'djongo'`
- Configurar `CLIENT` amb `mongodb://localhost:27017`

---

## 🛠️ Comandes útils
- Arrencar el servidor: `python manage.py runserver`
- Crear migracions: `python manage.py makemigrations`
- Aplicar migracions: `python manage.py migrate`
- Proves: `python manage.py test`

---

## 💾 Fixtures (exemple)
Per carregar dades inicials:
```bash
python manage.py loaddata fixtures/exemple.json

---

### 12. Seeds
```markdown
## 🌱 Seeds (exemple d'script)
Exemple: `seeds/create_groups.py`

```python
from django.contrib.auth.models import Group

def run():
    Group.objects.get_or_create(name="Organitzadors")
    Group.objects.get_or_create(name="Participants")
