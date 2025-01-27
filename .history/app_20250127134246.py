from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def init_db():
    # Remove existing database if it exists
    if os.path.exists('clinic.db'):
        os.remove('clinic.db')
    
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nom TEXT,
                 adresse TEXT,
                 date_naissance TEXT,
                 age INTEGER,
                 statut TEXT,
                 occupation TEXT,
                 numero_personnel TEXT,
                 numero_etablissement TEXT,
                 nom_conjoint TEXT,
                 occupation_conjoint TEXT,
                 numero_tel_conjoint TEXT,
                 numero_etablissement_conjoint TEXT,
                 date_naissance_conjoint TEXT,
                 age_conjoint INTEGER,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
             )''')

    conn.commit()
    conn.close()

@app.route('/info_patient')
def info_patient():
    return render_template('info_patient.html')

@app.route('/save_patient', methods=['POST'])
def save_patient():
    try:
        data = request.form
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        
        c.execute('''INSERT INTO patients 
                    (nom, adresse, date_naissance, age, statut, occupation, numeroPersonnel, numeroEtablissement,
                     nom_conjoint, occupation_conjoint, numeroTelConjoint, numeroEtablissementConjoint,
                     date_naissance_conjoint, age_conjoint)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (data.get('nom'), data.get('adresse'), data.get('dateNaissance'),
                  data.get('age'), data.get('statut'), data.get('occupation'),
                  data.get('numeroPersonnel'), data.get('numeroEtablissement'),
                  data.get('nomConjoint'), data.get('occupationConjoint'),
                  data.get('numeroTelConjoint'), data.get('numeroEtablissementConjoint'),
                  data.get('dateNaissanceConjoint'), data.get('ageConjoint')))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Patient enregistré avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/archives')
def archives():
    return render_template('archives.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)