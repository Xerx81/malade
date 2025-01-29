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
                 ddr TEXT,
                 dpa TEXT,
                 cycle TEXT,
                 duree TEXT,
                 g TEXT,
                 a TEXT,
                 t TEXT,
                 e TEXT,
                 p TEXT,
                 muit TEXT,
                 type_contraception TEXT,
                 commentaire_type TEXT,
                 duree_contraception TEXT,
                 commentaire_duree TEXT,
                 derniere_utilisation TEXT,
                 commentaire_derniere_utilisation TEXT,
                 saignement TEXT,
                 vomissement TEXT,
                 fievre TEXT,
                 tabac TEXT,
                 alcool TEXT,
                 radiation TEXT,
                 no_1 TEXT,
                 annee_1 TEXT,
                 sexe_1 TEXT,
                 age_gest_1 TEXT,
                 poids_1 TEXT,
                 lieu_acc_1 TEXT,
                 type_acc_1 TEXT,
                 radiation_obstetrique_1 TEXT,
                 remarques_1 TEXT,
                 no_2 TEXT,
                 annee_2 TEXT,
                 sexe_2 TEXT,
                 age_gest_2 TEXT,
                 poids_2 TEXT,
                 lieu_acc_2 TEXT,
                 type_acc_2 TEXT,
                 radiation_obstetrique_2 TEXT,
                 remarques_2 TEXT,
                 no_3 TEXT,
                 annee_3 TEXT,
                 sexe_3 TEXT,
                 age_gest_3 TEXT,
                 poids_3 TEXT,
                 lieu_acc_3 TEXT,
                 type_acc_3 TEXT,
                 radiation_obstetrique_3 TEXT,
                 remarques_3 TEXT,
                 maladies_renales TEXT,
                 remarques_renales TEXT,
                 problemes_cardiaques TEXT,
                 remarques_cardiaques TEXT,
                 hypertension_arterielle TEXT,
                 remarques_hypertension TEXT,
                 diabete TEXT,
                 remarques_diabete TEXT,
                 infection TEXT,
                 remarques_infection TEXT,
                 maladie_thyroide TEXT,
                 remarques_thyroide TEXT,
                 transfusion TEXT,
                 remarques_transfusion TEXT,
                 chirurgie TEXT,
                 remarques_chirurgie TEXT,
                 herpes TEXT,
                 remarques_herpes TEXT,
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
                     date_naissance_conjoint, age_conjoint, ddr, dpa, cycle, duree, g, a, t, e, p, muit,
                     type_contraception, commentaire_type, duree_contraception, commentaire_duree, derniere_utilisation,
                     commentaire_derniere_utilisation, saignement, vomissement, fievre, tabac, alcool, radiation,
                     no_1, annee_1, sexe_1, age_gest_1, poids_1, lieu_acc_1, type_acc_1, radiation_obstetrique_1, remarques_1,
                     no_2, annee_2, sexe_2, age_gest_2, poids_2, lieu_acc_2, type_acc_2, radiation_obstetrique_2, remarques_2,
                     no_3, annee_3, sexe_3, age_gest_3, poids_3, lieu_acc_3, type_acc_3, radiation_obstetrique_3, remarques_3,
                     maladies_renales, remarques_renales, problemes_cardiaques, remarques_cardiaques,
                     hypertension_arterielle, remarques_hypertension, diabete, remarques_diabete,
                     infection, remarques_infection, maladie_thyroide, remarques_thyroide,
                     transfusion, remarques_transfusion, chirurgie, remarques_chirurgie,
                     herpes, remarques_herpes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data.get('nom'), data.get('adresse'), data.get('dateNaissance'), data.get('age'),
                     data.get('statut'), data.get('occupation'), data.get('numeroPersonnel'), data.get('numeroEtablissement'),
                     data.get('nomConjoint'), data.get('occupationConjoint'), data.get('numeroTelConjoint'),
                     data.get('numeroEtablissementConjoint'), data.get('dateNaissanceConjoint'), data.get('ageConjoint'),
                     data.get('ddr'), data.get('dpa'), data.get('cycle'), data.get('duree'), 
                     data.get('g'), data.get('a'), data.get('t'), data.get('e'), data.get('p'), data.get('muit'),
                     data.get('type'), data.get('commentaireType'), data.get('dureeContraception'),
                     data.get('commentaireDuree'), data.get('derniereUtilisation'),
                     data.get('commentaireDerniereUtilisation'), data.get('saignement'), data.get('vomissement'),
                     data.get('fievre'), data.get('tabac'), data.get('alcool'), data.get('radiation'),
                     data.get('no_1'), data.get('annee_1'), data.get('sexe_1'), data.get('age_gest_1'),
                     data.get('poids_1'), data.get('lieu_acc_1'), data.get('type_acc_1'), data.get('radiation_obstetrique_1'),
                     data.get('remarques_1'), data.get('no_2'), data.get('annee_2'), data.get('sexe_2'),
                     data.get('age_gest_2'), data.get('poids_2'), data.get('lieu_acc_2'), data.get('type_acc_2'),
                     data.get('radiation_obstetrique_2'), data.get('remarques_2'), data.get('no_3'), data.get('annee_3'),
                     data.get('sexe_3'), data.get('age_gest_3'), data.get('poids_3'), data.get('lieu_acc_3'),
                     data.get('type_acc_3'), data.get('radiation_obstetrique_3'), data.get('remarques_3'),
                     data.get('maladies_renales'), data.get('remarques_renales'),
                     data.get('problemes_cardiaques'), data.get('remarques_cardiaques'),
                     data.get('hypertension_arterielle'), data.get('remarques_hypertension'),
                     data.get('diabete'), data.get('remarques_diabete'),
                     data.get('infection'), data.get('remarques_infection'),
                     data.get('maladie_thyroide'), data.get('remarques_thyroide'),
                     data.get('transfusion'), data.get('remarques_transfusion'),
                     data.get('chirurgie'), data.get('remarques_chirurgie'),
                     data.get('herpes'), data.get('remarques_herpes')))

        patient_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'patient_id': patient_id}), 200
    except Exception as e:
        print(f"Error saving patient: {str(e)}")  
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
                 commentaire_derniere_utilisation, saignement, vomissement, fievre, tabac, alcool,
                 radiation, no_1, annee_1, sexe_1, age_gest_1, poids_1, lieu_acc_1, type_acc_1,
                 radiation_obstetrique_1, remarques_1, no_2, annee_2, sexe_2, age_gest_2, poids_2,
                 lieu_acc_2, type_acc_2, radiation_obstetrique_2, remarques_2, no_3, annee_3, sexe_3,
                 age_gest_3, poids_3, lieu_acc_3, type_acc_3, radiation_obstetrique_3, remarques_3,
                 maladies_renales, remarques_renales, problemes_cardiaques, remarques_cardiaques,
                 hypertension_arterielle, remarques_hypertension, diabete, remarques_diabete,
                 infection, remarques_infection, maladie_thyroide, remarques_thyroide,
                 transfusion, remarques_transfusion, chirurgie, remarques_chirurgie,
                 herpes, remarques_herpes
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
            'commentaire_derniere_utilisation': patient[29],
            'saignement': patient[30],
            'vomissement': patient[31],
            'fievre': patient[32],
            'tabac': patient[33],
            'alcool': patient[34],
            'radiation': patient[35],
            'no_1': patient[36],
            'annee_1': patient[37],
            'sexe_1': patient[38],
            'age_gest_1': patient[39],
            'poids_1': patient[40],
            'lieu_acc_1': patient[41],
            'type_acc_1': patient[42],
            'radiation_obstetrique_1': patient[43],
            'remarques_1': patient[44],
            'no_2': patient[45],
            'annee_2': patient[46],
            'sexe_2': patient[47],
            'age_gest_2': patient[48],
            'poids_2': patient[49],
            'lieu_acc_2': patient[50],
            'type_acc_2': patient[51],
            'radiation_obstetrique_2': patient[52],
            'remarques_2': patient[53],
            'no_3': patient[54],
            'annee_3': patient[55],
            'sexe_3': patient[56],
            'age_gest_3': patient[57],
            'poids_3': patient[58],
            'lieu_acc_3': patient[59],
            'type_acc_3': patient[60],
            'radiation_obstetrique_3': patient[61],
            'remarques_3': patient[62],
            'maladies_renales': patient[63],
            'remarques_renales': patient[64],
            'problemes_cardiaques': patient[65],
            'remarques_cardiaques': patient[66],
            'hypertension_arterielle': patient[67],
            'remarques_hypertension': patient[68],
            'diabete': patient[69],
            'remarques_diabete': patient[70],
            'infection': patient[71],
            'remarques_infection': patient[72],
            'maladie_thyroide': patient[73],
            'remarques_thyroide': patient[74],
            'transfusion': patient[75],
            'remarques_transfusion': patient[76],
            'chirurgie': patient[77],
            'remarques_chirurgie': patient[78],
            'herpes': patient[79],
            'remarques_herpes': patient[80]
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