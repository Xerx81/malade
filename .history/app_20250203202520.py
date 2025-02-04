from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

# Centralize patient fields
PATIENT_FIELDS = [
    'nom', 'adresse', 'dateNaissance', 'age', 'statut', 'occupation', 'numeroPersonnel',
    'numeroEtablissement', 'nomConjoint', 'occupationConjoint', 'numeroTelConjoint',
    'numeroEtablissementConjoint', 'dateNaissanceConjoint', 'ageConjoint', 'ddr', 'dpa',
    'cycle', 'duree', 'g', 'a', 't', 'e', 'p', 'mult', 'type', 'commentaireType',
    'dureeContraception', 'commentaireDuree', 'derniereUtilisation', 'commentaireDerniereUtilisation',
    'saignement', 'vomissement', 'fievre', 'tabac', 'alcool', 'radiation', 'no_1', 'annee_1', 'sexe_1',
    'age_gest_1', 'poids_1', 'lieu_acc_1', 'type_acc_1', 'radiation_obstetrique_1', 'remarques_1',
    'problemes_sante_1', 'resultat_1', 'remarques_medicales_1', 'no_2', 'annee_2', 'sexe_2', 'age_gest_2',
    'poids_2', 'lieu_acc_2', 'type_acc_2', 'radiation_obstetrique_2', 'remarques_2', 'problemes_sante_2',
    'resultat_2', 'remarques_medicales_2', 'no_3', 'annee_3', 'sexe_3', 'age_gest_3', 'poids_3',
    'lieu_acc_3', 'type_acc_3', 'radiation_obstetrique_3', 'remarques_3', 'problemes_sante_3', 'resultat_3',
    'remarques_medicales_3', 'maladies_renales', 'remarques_renales', 'problemes_cardiaques',
    'remarques_cardiaques', 'hypertension_arterielle', 'remarques_hypertension', 'diabete',
    'remarques_diabete', 'infection', 'remarques_infection', 'maladie_thyroide', 'remarques_thyroide',
    'transfusion', 'remarques_transfusion', 'chirurgie', 'remarques_chirurgie', 'herpes', 'remarques_herpes',
    'antecedent_hypertension_fam', 'remarques_hypertension_fam', 'antecedent_diabete_fam',
    'remarques_diabete_fam', 'antecedent_maladie_cardiaque_fam', 'remarques_maladie_cardiaque_fam',
    'antecedent_gemellaire_fam', 'remarques_gemellaire_fam', 'antecedent_malformation_fam',
    'remarques_malformation_fam', 'antecedent_maladie_genetique_fam', 'remarques_maladie_genetique_fam',
    'produitsLaitiers', 'painCereales', 'fruitsLegumes', 'sourcesProteiniques', 'tabagisme', 'alcoolisme',
    'stupefiants', 'medicaments', 'travail', 'exercice', 'rapportSexuel', 'complicationsGrossesse',
    'soinsDentaires', 'allaitementMaternel', 'classePrenatale', 'tete_cou_thyroide', 'dents', 'thorax',
    'seins', 'systeme_cardiovasculaire', 'abdomen', 'bassin', 'taille', 'vulve', 'vagin', 'col', 'uterus', 'anus',
    'varicosites', 'observations', 'risques_identifies', 'toxoplasmose', 'herpes1', 'herpes2', 'hpv', 'ehb', 'serologie_rubeole', 'hbs_ag',
    'syphilis', 'hb', 'gs', 'hiv', 'remarque', 'date', 'poids', 'age_gestationnel', 'hu', 'pres_post',
    'bdcf', 'ta', 'urine_pr_glu', 'risque', 'commentaire_lab_med', 'date_accouchement', 'poids_mere',
    'ta_mere', 'albuminurie', 'retour_couches', 'allaitement', 'dystocie', 'etat_enfant_naissance',
    'sexe_enfant', 'apgar', 'observations_enfant', 'payment', 'montant_paye', 'mode_paiement'
]

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def init_db():
    # Uncomment the next two lines to remove an existing database (for development only)
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
    # Note that the patients table has an extra column "created_at" after "id"
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ''' + ',\n'.join([f"{field} TEXT" for field in PATIENT_FIELDS]) + '''
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

def generate_insert_sql(table_name, fields):
    columns = ', '.join(fields)
    placeholders = ', '.join(['?' for _ in fields])
    return f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

def generate_update_sql(table_name, fields):
    set_clause = ', '.join([f"{field} = ?" for field in fields])
    return f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

def get_form_data(form_data, fields):
    return [form_data.get(field) for field in fields]

@app.route('/save_patient', methods=['POST'])
def save_patient():
    try:
        data = request.form
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400

        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()

        # Generate SQL dynamically without including created_at
        insert_sql = generate_insert_sql('patients', PATIENT_FIELDS)
        values = get_form_data(data, PATIENT_FIELDS)

        # Debugging
        print("\n=== Values to Insert ===")
        print(f"Number of values: {len(values)}")
        print("Values:", values)

        c.execute(insert_sql, values)
        patient_id = c.lastrowid
        conn.commit()
        conn.close()

        flash('Patient ajouté avec succès!', 'success')
        return redirect(url_for('liste_patients'))

    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()
        flash("Erreur lors de l'ajout du patient.", 'error')
        return redirect(url_for('liste_patients'))

@app.route('/liste_patients')
def liste_patients():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    # Note: using camelCase column names to match PATIENT_FIELDS
    c.execute('SELECT id, nom, dateNaissance, age, numeroPersonnel, statut, created_at FROM patients')
    patients = c.fetchall()
    conn.close()
    patients_list = [{
        'id': p[0],
        'nom': p[1],
        'dateNaissance': p[2],
        'age': p[3],
        'numeroPersonnel': p[4],
        'statut': p[5],
        'created_at': p[6]
    } for p in patients]
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
def update_patient_form(patient_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = c.fetchone()
    conn.close()
    if patient:
        # The table columns are: id, created_at, then PATIENT_FIELDS.
        patient_info = dict(zip(['id', 'created_at'] + PATIENT_FIELDS, patient))
        return render_template('update_patient.html', patient=patient_info)
    else:
        return "Patient non trouvé", 404

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

        # Build UPDATE SQL for the PATIENT_FIELDS only (leaving created_at unchanged)
        update_sql = generate_update_sql('patients', PATIENT_FIELDS)
        values = get_form_data(data, PATIENT_FIELDS) + [patient_id]

        # Debugging
        print("\n=== Values for Update ===")
        print(f"Number of values: {len(values)}")
        print("Values:", values)

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
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    
    # Total number of patients
    c.execute('SELECT COUNT(*) FROM patients')
    total_patients = c.fetchone()[0]
    
    # Patients added today
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT COUNT(*) FROM patients WHERE DATE(created_at) = ?', (today,))
    patients_today = c.fetchone()[0]
    
    # Active patients (assuming active patients are those added in the last 30 days)
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    c.execute('SELECT COUNT(*) FROM patients WHERE created_at >= ?', (thirty_days_ago,))
    active_patients = c.fetchone()[0]
    
    # Fetch recent patients
    c.execute('SELECT id, nom, date_naissance, age, statut, created_at FROM patients ORDER BY created_at DESC LIMIT 10')
    patients = c.fetchall()
    conn.close()
    
    patients_list = [{
    'id': p[0],
    'nom': p[1],
    'dateNaissance': p[2],
    'age': p[3],
    'numeroPersonnel': p[4],
    'statut': p[5],
    'created_at': p[6]
    } for p in patients]
    
    return render_template('dashboard.html',
                           patients=patients_list,
                           total_patients=total_patients,
                           patients_today=patients_today,
                           active_patients=active_patients)

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
            except sqlite3.IntegrityError:
                flash('Ce nom d\'utilisateur ou cet email est déjà utilisé.', 'error')
        else:
            flash('Mot de passe actuel incorrect.', 'error')
        conn.close()
        return redirect(url_for('profile'))
    
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Optionally, you may want to require login on the index as well.
@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/show')
def showpatient():
    return render_template('affichage_patients2.html')

@app.route('/afficher_patient/<int:patient_id>')
def afficher_patient(patient_id):
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = c.fetchone()
    conn.close()
    if patient:
        # Correct the key mapping to include created_at
        patient_info = dict(zip(['id', 'created_at'] + PATIENT_FIELDS, patient))
        return render_template('afficher_patient.html', patient=patient_info)
    else:
        return "Patient non trouvé", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
