from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from models import db, Patient
import os
from sqlalchemy import or_

app = Flask(__name__)

# SQLite Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'clinic.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', title='Formulaire de Surveillance')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        form_data = request.form.to_dict()
        
        # Create new patient record
        patient = Patient(
            nom=form_data.get('nom'),
            age=form_data.get('age'),
            adresse=form_data.get('adresse'),
            date_naissance=datetime.strptime(form_data.get('dateNaissance', ''), '%Y-%m-%d').date() if form_data.get('dateNaissance') else None,
            statut=form_data.get('statut'),
            occupation=form_data.get('occupation'),
            numero_personnel=form_data.get('numeroPersonnel'),
            numero_etablissement=form_data.get('numeroEtablissement'),
            
            # Conjoint information
            nom_conjoint=form_data.get('nomConjoint'),
            occupation_conjoint=form_data.get('occupationConjoint'),
            numero_tel_conjoint=form_data.get('numeroTelConjoint'),
            numero_etablissement_conjoint=form_data.get('numeroEtablissementConjoint'),
            date_naissance_conjoint=datetime.strptime(form_data.get('dateNaissanceConjoint', ''), '%Y-%m-%d').date() if form_data.get('dateNaissanceConjoint') else None,
            
            # Store JSON data
            antecedents_medicaux=request.form.getlist('antecedents_medicaux'),
            antecedents_heredo=request.form.getlist('antecedents_heredo'),
            nutrition_counseling=request.form.getlist('nutrition_counseling'),
            examen_physique=request.form.getlist('examen_physique'),
            immunisation_tests=request.form.getlist('immunisation_tests')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({"message": "Formulaire soumis avec succès"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/search_patients')
def search_patients():
    query = request.args.get('query', '')
    filter_type = request.args.get('filter', 'all')
    
    # Base query
    base_query = Patient.query
    
    # Apply time filter
    now = datetime.utcnow()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
        base_query = base_query.filter(Patient.date_creation >= start_date)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
        base_query = base_query.filter(Patient.date_creation >= start_date)
    elif filter_type == 'year_plus':
        start_date = now - timedelta(days=365)
        base_query = base_query.filter(Patient.date_creation <= start_date)
    
    # Apply name search if query exists
    if query:
        base_query = base_query.filter(
            or_(
                Patient.nom.ilike(f'%{query}%')
            )
        )
    
    # Get results
    patients = base_query.order_by(Patient.date_creation.desc()).all()
    
    # Format results
    results = [patient.to_dict() for patient in patients]
    
    # Get counts for each filter
    counts = {
        'all': Patient.query.count(),
        'week': Patient.query.filter(Patient.date_creation >= now - timedelta(days=7)).count(),
        'month': Patient.query.filter(Patient.date_creation >= now - timedelta(days=30)).count(),
        'year_plus': Patient.query.filter(Patient.date_creation <= now - timedelta(days=365)).count()
    }
    
    return jsonify({
        'patients': results,
        'counts': counts,
        'total_results': len(results)
    })

@app.route('/archives')
def archives():
    patients = Patient.query.order_by(Patient.date_creation.desc()).all()
    return render_template('archives.html', title='Archives', records=[patient.to_dict() for patient in patients])

@app.route('/patient/<int:patient_id>')
def patient_details(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patient_details.html', patient=patient)

@app.route('/patient/<int:id>/delete', methods=['POST'])
def delete_patient(id):
    try:
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"success": True, "message": "Patient supprimé avec succès"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/patient/<int:id>/edit', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        try:
            data = request.json
            patient.nom = data.get('nom', patient.nom)
            patient.age = data.get('age', patient.age)
            patient.adresse = data.get('adresse', patient.adresse)
            patient.telephone = data.get('telephone', patient.telephone)
            patient.statut = data.get('statut', patient.statut)
            patient.antecedents = data.get('antecedents', patient.antecedents)
            patient.date_modification = datetime.utcnow()
            
            db.session.commit()
            return jsonify({"success": True, "patient": patient.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    return jsonify(patient.to_dict())

@app.route('/patient/<int:id>/pdf')
def get_patient_pdf(id):
    patient = Patient.query.get_or_404(id)
    return jsonify(patient.to_dict())

if __name__ == '__main__':
    app.run(debug=True)