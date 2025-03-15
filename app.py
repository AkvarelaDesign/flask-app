from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Nastavení SQLite databáze
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skolky.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definice tabulky pro školky
class Skolka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(200), nullable=False)
    telefon = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    web = db.Column(db.String(200), nullable=True)

# První vytvoření databázové tabulky
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    skolky = Skolka.query.all()  # Načtení všech školek z databáze
    return render_template('index.html', skolky=skolky)

@app.route('/naplnit')
def naplnit_db():
    # Seznam školek, které chceme přidat
    seznam_skol = [
        {"nazev": "Mateřská škola Sluníčko", "telefon": "+420123456789", "email": "info@slunicko.cz", "web": "http://www.slunicko.cz"},
        {"nazev": "Mateřská škola Pohádka", "telefon": "+420987654321", "email": "info@pohadka.cz", "web": "http://www.pohadka.cz"},
        {"nazev": "Mateřská škola Beruška", "telefon": "+420606606606", "email": "info@beruska.cz", "web": "http://www.beruska.cz"},
    ]
    
    # Přidání do databáze
    for skolka_data in seznam_skol:
        skolka = Skolka(**skolka_data)
        db.session.add(skolka)
    
    db.session.commit()
    return "Databáze byla naplněna školkami! 🎉"

if __name__ == '__main__':
    app.run(debug=True)
