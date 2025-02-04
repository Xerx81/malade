from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    nom = db.Column(db.String(100))
    age = db.Column(db.Integer)
    adresse = db.Column(db.String(200))
    date_naissance = db.Column(db.Date)
    statut = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    numero_personnel = db.Column(db.String(50))
    numero_etablissement = db.Column(db.String(50))
    
    # Conjoint information
    nom_conjoint = db.Column(db.String(100))
    occupation_conjoint = db.Column(db.String(100))
    numero_tel_conjoint = db.Column(db.String(50))
    numero_etablissement_conjoint = db.Column(db.String(50))
    date_naissance_conjoint = db.Column(db.Date)
    
    # Medical history
    antecedents_medicaux = db.Column(db.JSON)
    antecedents_heredo = db.Column(db.JSON)
    nutrition_counseling = db.Column(db.JSON)
    examen_physique = db.Column(db.JSON)
    immunisation_tests = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date_creation': self.date_creation.strftime("%Y-%m-%d %H:%M:%S"),
            'nom': self.nom,
            'age': self.age,
            'statut': self.statut,
            'adresse': self.adresse,
            'occupation': self.occupation
        }
