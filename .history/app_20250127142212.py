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
                    (nom, adresse, date_naissance, age, statut, occupation, numero_personnel, numero_etablissement,
                     nom_conjoint, occupation_conjoint, numero_tel_conjoint, numero_etablissement_conjoint,
                     date_naissance_conjoint, age_conjoint)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (data.get('nom'), data.get('adresse'), data.get('dateNaissance'),
                  data.get('age'), data.get('statut'), data.get('occupation'),
                  data.get('numeroPersonnel'), data.get('numeroEtablissement'),
                  data.get('nomConjoint'), data.get('occupationConjoint'),
                  data.get('numeroTelConjoint'), data.get('numeroEtablissementConjoint'),
                  data.get('dateNaissanceConjoint'), data.get('ageConjoint')))
        
        patient_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'patient_id': patient_id}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/liste_patients')
def liste_patients():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('SELECT id, nom, date_naissance, statut FROM patients')
    patients = c.fetchall()
    conn.close()
    
    patients_list = [{'id': p[0], 'nom': p[1], 'date_naissance': p[2], 'statut': p[3]} for p in patients]
    return render_template('liste_patients.html', patients=patients_list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/afficher_patient/<int:patient_id>')
def afficher_patient(patient_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('''SELECT nom, adresse, date_naissance, age, statut, occupation, 
                 numero_personnel, numero_etablissement, nom_conjoint, occupation_conjoint,
                 numero_tel_conjoint, numero_etablissement_conjoint, date_naissance_conjoint,
                 age_conjoint, ddr, dpa, cycle, duree, g, a, t, e, p, muit, type_contraception,
                 commentaire_type, duree_contraception, commentaire_duree, derniere_utilisation,
                 commentaire_derniere_utilisation
                 FROM patients WHERE id = ?''', (patient_id,))
    patient = c.fetchone()
    conn.close()
    
    if patient:
        patient_info = {
            'nom': patient[0],
            'adresse': patient[1],
            'date_naissance': patient[2],
            'age': patient[3],
            'statut': patient[4],
            'occupation': patient[5],
            'numero_personnel': patient[6],
            'numero_etablissement': patient[7],
            'nom_conjoint': patient[8],
            'occupation_conjoint': patient[9],
            'numero_tel_conjoint': patient[10],
            'numero_etablissement_conjoint': patient[11],
            'date_naissance_conjoint': patient[12],
            'age_conjoint': patient[13],
            'ddr': patient[14],
            'dpa': patient[15],
            'cycle': patient[16],
            'duree': patient[17],
            'g': patient[18],
            'a': patient[19],
            't': patient[20],
            'e': patient[21],
            'p': patient[22],
            'muit': patient[23],
            'type_contraception': patient[24],
            'commentaire_type': patient[25],
            'duree_contraception': patient[26],
            'commentaire_duree': patient[27],
            'derniere_utilisation': patient[28],
            'commentaire_derniere_utilisation': patient[29]
        }
        return render_template('afficher_patient.html', patient=patient_info)
        
            'dpa': form_data['dpa'],
            'cycle': form_data['cycle'],
            'duree': form_data['duree'],
            'g': form_data['g'],
            'a': form_data['a'],
            't': form_data['t'],
            'e': form_data['e'],
            'p': form_data['p'],
            'muit': form_data['muit'],
            'type_contraception': form_data['type'],
            'commentaire_type': form_data['commentaireType'],
            'duree_contraception': form_data['dureeContraception'],
            'commentaire_duree': form_data['commentaireDuree'],
            'derniere_utilisation': form_data['derniereUtilisation'],
            'commentaire_derniere_utilisation': form_data['commentaireDerniereUtilisation']
        }
        return render_template('afficher_patient.html', patient=patient_info)
    else:
        return "Patient non trouvé", 404

@app.route('/archives')
def archives():
    return render_template('archives.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)