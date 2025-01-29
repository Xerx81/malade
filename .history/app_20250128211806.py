from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def init_db():
    # Remove existing database if it exists
    # if os.path.exists('clinic.db'):
    #     os.remove('clinic.db')
    
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL
                 )''')
    
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
                 problemes_sante_1 TEXT,
                 resultat_1 TEXT,
                 remarques_medicales_1 TEXT,
                 no_2 TEXT,
                 annee_2 TEXT,
                 sexe_2 TEXT,
                 age_gest_2 TEXT,
                 poids_2 TEXT,
                 lieu_acc_2 TEXT,
                 type_acc_2 TEXT,
                 radiation_obstetrique_2 TEXT,
                 remarques_2 TEXT,
                 problemes_sante_2 TEXT,
                 resultat_2 TEXT,
                 remarques_medicales_2 TEXT,
                 no_3 TEXT,
                 annee_3 TEXT,
                 sexe_3 TEXT,
                 age_gest_3 TEXT,
                 poids_3 TEXT,
                 lieu_acc_3 TEXT,
                 type_acc_3 TEXT,
                 radiation_obstetrique_3 TEXT,
                 remarques_3 TEXT,
                 problemes_sante_3 TEXT,
                 resultat_3 TEXT,
                 remarques_medicales_3 TEXT,
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
                 antecedent_hypertension_fam TEXT,
                 remarques_hypertension_fam TEXT,
                 antecedent_diabete_fam TEXT,
                 remarques_diabete_fam TEXT,
                 antecedent_maladie_cardiaque_fam TEXT,
                 remarques_maladie_cardiaque_fam TEXT,
                 antecedent_gemellaire_fam TEXT,
                 remarques_gemellaire_fam TEXT,
                 antecedent_malformation_fam TEXT,
                 remarques_malformation_fam TEXT,
                 antecedent_maladie_genetique_fam TEXT,
                 remarques_maladie_genetique_fam TEXT,
                 produitsLaitiers TEXT,
                 painCereales TEXT,
                 fruitsLegumes TEXT,
                 sourcesProteiniques TEXT,
                 tabagisme TEXT,
                 alcoolisme TEXT,
                 stupefiants TEXT,
                 medicaments TEXT,
                 travail TEXT,
                 exercice TEXT,
                 rapportSexuel TEXT,
                 complicationsGrossesse TEXT,
                 soinsDentaires TEXT,
                 allaitementMaternel TEXT,
                 classePrenatale TEXT,
                 tete_cou_thyroide TEXT,
                 dents TEXT,
                 thorax TEXT,
                 seins TEXT,
                 systeme_cardiovasculaire TEXT,
                 abdomen TEXT,
                 bassin TEXT,
                 vulve TEXT,
                 vagin TEXT,
                 col TEXT,
                 uterus TEXT,
                 anus TEXT,
                 varicosites TEXT,
                 observations TEXT,
                 risques_identifies TEXT,
                 immunisation TEXT,
                 serologie_rubeole TEXT,
                 hbs_ag TEXT,
                 syphilis TEXT,
                 hb TEXT,
                 gs TEXT,
                 hiv TEXT,
                 remarque TEXT,
                 date DATE,
                 poids TEXT,
                 age_gestationnel TEXT,
                 hu TEXT,
                 pres_post TEXT,
                 bdcf TEXT,
                 ta TEXT,
                 urine_pr_glu TEXT,
                 risque TEXT,
                 commentaire_lab_med TEXT,
                 date_accouchement DATE,
                 poids_mere TEXT,
                 ta_mere TEXT,
                 albuminurie TEXT,
                 retour_couches TEXT,
                 allaitement TEXT,
                 dystocie TEXT,
                 etat_enfant_naissance TEXT,
                 sexe_enfant TEXT,
                 apgar TEXT,
                 observations_enfant TEXT,

                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
             )''')
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/info_patient')
def info_patient():
    return render_template('info_patient.html')

@app.route('/save_patient', methods=['POST'])
def save_patient():
    try:
        data = request.form
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400

        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        
        # Debug: Print table info
        c.execute("PRAGMA table_info(patients)")
        columns = c.fetchall()
        print("=== Database Schema ===")
        print(f"Total columns in schema: {len(columns)}")
        for col in columns:
            print(f"Column: {col[1]}, Type: {col[2]}")
        
        # Debug: Print values being inserted
        values = [data.get('nom'), data.get('adresse'), data.get('dateNaissance'), data.get('age'),
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
                 data.get('remarques_1'), data.get('problemes_sante_1'), data.get('resultat_1'), data.get('remarques_medicales_1'),
                 data.get('no_2'), data.get('annee_2'), data.get('sexe_2'),
                 data.get('age_gest_2'), data.get('poids_2'), data.get('lieu_acc_2'), data.get('type_acc_2'),
                 data.get('radiation_obstetrique_2'), data.get('remarques_2'), data.get('problemes_sante_2'), data.get('resultat_2'), data.get('remarques_medicales_2'),
                 data.get('no_3'), data.get('annee_3'),
                 data.get('sexe_3'), data.get('age_gest_3'), data.get('poids_3'), data.get('lieu_acc_3'),
                 data.get('type_acc_3'), data.get('radiation_obstetrique_3'), data.get('remarques_3'), data.get('problemes_sante_3'), data.get('resultat_3'), data.get('remarques_medicales_3'),
                 data.get('maladies_renales'), data.get('remarques_renales'),
                 data.get('problemes_cardiaques'), data.get('remarques_cardiaques'),
                 data.get('hypertension_arterielle'), data.get('remarques_hypertension'),
                 data.get('diabete'), data.get('remarques_diabete'),
                 data.get('infection'), data.get('remarques_infection'),
                 data.get('maladie_thyroide'), data.get('remarques_thyroide'),
                 data.get('transfusion'), data.get('remarques_transfusion'),
                 data.get('chirurgie'), data.get('remarques_chirurgie'),
                 data.get('herpes'), data.get('remarques_herpes'),
                 data.get('antecedent_hypertension_fam'), data.get('remarques_hypertension_fam'),
                 data.get('antecedent_diabete_fam'), data.get('remarques_diabete_fam'),
                 data.get('antecedent_maladie_cardiaque_fam'), data.get('remarques_maladie_cardiaque_fam'),
                 data.get('antecedent_gemellaire_fam'), data.get('remarques_gemellaire_fam'),
                 data.get('antecedent_malformation_fam'), data.get('remarques_malformation_fam'),
                 data.get('antecedent_maladie_genetique_fam'), data.get('remarques_maladie_genetique_fam'),
                 data.get('produitsLaitiers'), data.get('painCereales'),
                 data.get('fruitsLegumes'), data.get('sourcesProteiniques'),
                 data.get('tabagisme'), data.get('alcoolisme'),
                 data.get('stupefiants'), data.get('medicaments'),
                 data.get('travail'), data.get('exercice'),
                 data.get('rapportSexuel'), data.get('complicationsGrossesse'),
                 data.get('soinsDentaires'), data.get('allaitementMaternel'),
                 data.get('classePrenatale'),
                 data.get('tete_cou_thyroide'),
                 data.get('dents'),
                 data.get('thorax'),
                 data.get('seins'),
                 data.get('systeme_cardiovasculaire'),
                 data.get('abdomen'),
                 data.get('bassin'),
                 data.get('vulve'),
                 data.get('vagin'),
                 data.get('col'),
                 data.get('uterus'),
                 data.get('anus'),
                 data.get('varicosites'),
                 data.get('observations'),
                 data.get('risques_identifies'),
                 data.get('immunisation'),
                 data.get('serologie_rubeole'),
                 data.get('hbs_ag'),
                 data.get('syphilis'),
                 data.get('hb'),
                 data.get('gs'),
                 data.get('hiv'),
                 data.get('remarque'),
                 data.get('date'), data.get('poids'), data.get('age_gestationnel'),
                 data.get('hu'), data.get('pres_post'), data.get('bdcf'),
                 data.get('ta'), data.get('urine_pr_glu'), data.get('risque'),
                 data.get('commentaire_lab_med'), data.get('date_accouchement'),
                 data.get('poids_mere'), data.get('ta_mere'), data.get('albuminurie'),
                 data.get('retour_couches'), data.get('allaitement'), data.get('dystocie'),
                 data.get('etat_enfant_naissance'), data.get('sexe_enfant'), data.get('apgar'),
                 data.get('observations_enfant')]
        
        print("\n=== Values to Insert ===")
        print(f"Number of values: {len(values)}")
        print("Values:", values)
        
        insert_sql = '''INSERT INTO patients 
                    (nom, adresse, date_naissance, age, statut, occupation, numero_personnel, numero_etablissement,
                     nom_conjoint, occupation_conjoint, numero_tel_conjoint, numero_etablissement_conjoint,
                     date_naissance_conjoint, age_conjoint, ddr, dpa, cycle, duree, g, a, t, e, p, muit,
                     type_contraception, commentaire_type, duree_contraception, commentaire_duree, derniere_utilisation,
                     commentaire_derniere_utilisation, saignement, vomissement, fievre, tabac, alcool, radiation,
                     no_1, annee_1, sexe_1, age_gest_1, poids_1, lieu_acc_1, type_acc_1, radiation_obstetrique_1, remarques_1, problemes_sante_1, resultat_1, remarques_medicales_1,
                     no_2, annee_2, sexe_2, age_gest_2, poids_2, lieu_acc_2, type_acc_2, radiation_obstetrique_2, remarques_2, problemes_sante_2, resultat_2, remarques_medicales_2,
                     no_3, annee_3, sexe_3, age_gest_3, poids_3, lieu_acc_3, type_acc_3, radiation_obstetrique_3, remarques_3, problemes_sante_3, resultat_3, remarques_medicales_3,
                     maladies_renales, remarques_renales, problemes_cardiaques, remarques_cardiaques,
                     hypertension_arterielle, remarques_hypertension, diabete, remarques_diabete,
                     infection, remarques_infection, maladie_thyroide, remarques_thyroide,
                     transfusion, remarques_transfusion, chirurgie, remarques_chirurgie,
                     herpes, remarques_herpes, antecedent_hypertension_fam, remarques_hypertension_fam, 
                     antecedent_diabete_fam, remarques_diabete_fam, antecedent_maladie_cardiaque_fam, remarques_maladie_cardiaque_fam,
                     antecedent_gemellaire_fam, remarques_gemellaire_fam, antecedent_malformation_fam, remarques_malformation_fam, 
                     antecedent_maladie_genetique_fam, remarques_maladie_genetique_fam,
                     produitsLaitiers, painCereales, fruitsLegumes, sourcesProteiniques,
                     tabagisme, alcoolisme, stupefiants, medicaments, travail, exercice,
                     rapportSexuel, complicationsGrossesse, soinsDentaires, allaitementMaternel,
                     classePrenatale,
                     tete_cou_thyroide, dents, thorax, seins, systeme_cardiovasculaire, abdomen, bassin, vulve, vagin, col, uterus, anus, varicosites, observations, risques_identifies, immunisation, serologie_rubeole, hbs_ag, syphilis, hb, gs, hiv, remarque,
                     date, poids, age_gestationnel, hu, pres_post, bdcf, ta, urine_pr_glu, risque, commentaire_lab_med,
                     date_accouchement, poids_mere, ta_mere, albuminurie, retour_couches, allaitement, dystocie, etat_enfant_naissance, sexe_enfant, apgar, observations_enfant)'''
                     
        print("\n=== SQL Statement ===")
        # Count the number of columns in the INSERT statement
        columns_in_insert = insert_sql.count(',') + 1
        print(f"Number of columns in INSERT: {columns_in_insert}")
        print(insert_sql)
        
        placeholders = ','.join(['?' for _ in range(len(values))])
        c.execute(insert_sql + f' VALUES ({placeholders})', values)
        
        # Get the ID of the newly inserted patient
        patient_id = c.lastrowid
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'patient_id': patient_id}), 200
    except Exception as e:
        print(f"Error saving patient: {str(e)}")
        # Print the full error traceback for debugging
        import traceback
        traceback.print_exc()
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

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_patient(id):
    try:
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        
        c.execute('DELETE FROM patients WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Patient supprimé avec succès'
        })
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({
            'status': 'failed',
            'message': str(e)
        }), 500
    
@app.route('/update/<int:patient_id>', methods=['GET'])
def update(patient_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM patients WHERE id = ?''', (patient_id,))
    patient = c.fetchone()

    c.execute('PRAGMA table_info(patients)')
    columns = [col[1] for col in c.fetchall()]
    return render_template('update_patient.html', patient=dict(zip(columns, patient)))

@app.route('/update_patient', methods=['POST'])
def update_patient():
    try:
        data = request.form
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400

        patient_id = data.get('patient_id')
        if not patient_id:
            return jsonify({'success': False, 'message': 'Patient ID is required'}), 400

        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()

        c.execute("PRAGMA table_info(patients)")
        columns = c.fetchall()
        print("=== Database Schema ===")
        print(f"Total columns in schema: {len(columns)}")
        for col in columns:
            print(f"Column: {col[1]}, Type: {col[2]}")

        fields = [
            'nom', 'adresse', 'date_naissance', 'age', 'statut', 'occupation', 'numero_personnel', 'numero_etablissement',
            'nom_conjoint', 'occupation_conjoint', 'numero_tel_conjoint', 'numero_etablissement_conjoint',
            'date_naissance_conjoint', 'age_conjoint', 'ddr', 'dpa', 'cycle', 'duree', 'g', 'a', 't', 'e', 'p', 'muit',
            'type_contraception', 'commentaire_type', 'duree_contraception', 'commentaire_duree', 'derniere_utilisation',
            'commentaire_derniere_utilisation', 'saignement', 'vomissement', 'fievre', 'tabac', 'alcool', 'radiation',
            'no_1', 'annee_1', 'sexe_1', 'age_gest_1', 'poids_1', 'lieu_acc_1', 'type_acc_1', 'radiation_obstetrique_1',
            'remarques_1', 'problemes_sante_1', 'resultat_1', 'remarques_medicales_1', 'no_2', 'annee_2', 'sexe_2',
            'age_gest_2', 'poids_2', 'lieu_acc_2', 'type_acc_2', 'radiation_obstetrique_2', 'remarques_2',
            'problemes_sante_2', 'resultat_2', 'remarques_medicales_2', 'no_3', 'annee_3', 'sexe_3', 'age_gest_3',
            'poids_3', 'lieu_acc_3', 'type_acc_3', 'radiation_obstetrique_3', 'remarques_3', 'problemes_sante_3',
            'resultat_3', 'remarques_medicales_3', 'maladies_renales', 'remarques_renales', 'problemes_cardiaques',
            'remarques_cardiaques', 'hypertension_arterielle', 'remarques_hypertension', 'diabete', 'remarques_diabete',
            'infection', 'remarques_infection', 'maladie_thyroide', 'remarques_thyroide', 'transfusion',
            'remarques_transfusion', 'chirurgie', 'remarques_chirurgie', 'herpes', 'remarques_herpes',
            'antecedent_hypertension_fam', 'remarques_hypertension_fam', 'antecedent_diabete_fam',
            'remarques_diabete_fam', 'antecedent_maladie_cardiaque_fam', 'remarques_maladie_cardiaque_fam',
            'antecedent_gemellaire_fam', 'remarques_gemellaire_fam', 'antecedent_malformation_fam',
            'remarques_malformation_fam', 'antecedent_maladie_genetique_fam', 'remarques_maladie_genetique_fam',
            'produitsLaitiers', 'painCereales', 'fruitsLegumes', 'sourcesProteiniques', 'tabagisme', 'alcoolisme',
            'stupefiants', 'medicaments', 'travail', 'exercice', 'rapportSexuel', 'complicationsGrossesse',
            'soinsDentaires', 'allaitementMaternel', 'classePrenatale', 'tete_cou_thyroide', 'dents', 'thorax',
            'seins', 'systeme_cardiovasculaire', 'abdomen', 'bassin', 'vulve', 'vagin', 'col', 'uterus', 'anus',
            'varicosites', 'observations', 'risques_identifies', 'immunisation', 'serologie_rubeole', 'hbs_ag',
            'syphilis', 'hb', 'gs', 'hiv', 'remarque', 'date', 'poids', 'age_gestationnel', 'hu', 'pres_post', 'bdcf',
            'ta', 'urine_pr_glu', 'risque', 'commentaire_lab_med', 'date_accouchement', 'poids_mere', 'ta_mere',
            'albuminurie', 'retour_couches', 'allaitement', 'dystocie', 'etat_enfant_naissance', 'sexe_enfant',
            'apgar', 'observations_enfant'
        ]

        set_clause = ', '.join([f"{field} = ?" for field in fields])
        values = [data.get(field) for field in fields]
        values.append(patient_id) 

        print("\n=== Values for Update ===")
        print(f"Number of values: {len(values)}")
        print("Values:", values)

        update_sql = f"""UPDATE patients SET {set_clause} WHERE id = ?"""
        print("\n=== SQL Statement ===")
        print(update_sql)

        c.execute(update_sql, values)
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Patient record updated successfully'}), 200
    except Exception as e:
        print(f"Error updating patient: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        
        try:
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        if check_password_hash(user[3], current_password):
            try:
                if new_password:
                    hashed_password = generate_password_hash(new_password)
                    c.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?',
                             (username, email, hashed_password, session['user_id']))
                else:
                    c.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                             (username, email, session['user_id']))
                
                conn.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile'))
            except sqlite3.IntegrityError:
                flash('Ce nom d  utilisateur ou cet email est deja utilisé.', 'error')
        else:
            flash('Mot de passe actuel incorrect.', 'error')
    
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/show')
def showpatient():
    return render_template('affichage_patients2.html')

@app.route('/afficher_patient/<int:patient_id>')
def afficher_patient(patient_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    
    # Get all columns from the patients table
    c.execute('''SELECT * FROM patients WHERE id = ?''', (patient_id,))
    patient = c.fetchone()
    
    # Get column names
    c.execute('PRAGMA table_info(patients)')
    columns = [col[1] for col in c.fetchall()]
    
    conn.close()
    
    if patient:
        # Create a dictionary with all patient information
        patient_info = dict(zip(columns, patient))
        return render_template('afficher_patient.html', patient=patient_info)
    else:
        return "Patient non trouvé", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)