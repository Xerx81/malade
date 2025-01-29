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
        data = request.get_json()
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
                 data.get('herpes'), data.get('remarques_herpes')]
        
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
                     herpes, remarques_herpes)'''
                     
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

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Formulaire de Surveillance de la Grossesse</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <script>
    function calculerAge(dateNaissance, cibleId) {
      const naissance = new Date(dateNaissance);
      const aujourdHui = new Date();
      let age = aujourdHui.getFullYear() - naissance.getFullYear();
      const mois = aujourdHui.getMonth() - naissance.getMonth();
      if (mois < 0 || (mois === 0 && aujourdHui.getDate() < naissance.getDate())) {
        age--;
      }
      document.getElementById(cibleId).value = age;
    }

    function afficherMessageEtReinitialiser() {
      const message = document.getElementById("message");
      message.classList.remove("hidden");
      setTimeout(() => {
        message.classList.add("hidden");
        document.getElementById("formulaire").reset();
        document.getElementById("infoConjoint").classList.add("hidden");
      }, 3000);
    }

    function gererStatutMatrimonial(valeur) {
      const infoConjoint = document.getElementById("infoConjoint");
      if (valeur === "Mariée" || valeur === "Concubine" || valeur === "En couple") {
        infoConjoint.classList.remove("hidden");
      } else {
        infoConjoint.classList.add("hidden");
      }
    }

    function calculerDPA(ddr, cibleId) {
      if (!ddr) return;
      const dateDDR = new Date(ddr);
      const dpa = new Date(dateDDR.setDate(dateDDR.getDate() + 280));
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const moisRestants = Math.floor((dpa - new Date()) / (1000 * 60 * 60 * 24 * 30.44));
      document.getElementById(cibleId).value = `${dpa.toLocaleDateString('fr-FR', options)} (${moisRestants} mois)`;
    }
    function ajouterLigne() {
      const tableBody = document.querySelector("tbody");
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="border px-4 py-2"><input type="date" class="w-full border rounded px-3 py-2"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Poids"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Âge gestationnel"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="HU"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Prés/Post"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="BDCF"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="TA"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Urine Pr/Glu"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Risque"></td>
        <td class="border px-4 py-2">
          <textarea class="w-full border rounded px-3 py-2 h-16" placeholder="Commentaire Lab/Med"></textarea>
        </td>`;
      tableBody.appendChild(row);
    }
  </script>
</head>
<body class="bg-gray-100">
    <!-- Navbar -->
    <nav class="bg-blue-600 text-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo et titre -->
          <div class="flex items-center">
            <span class="text-2xl font-bold italic tracking-wide">Clinique Dr ADRIEN Laur&eacute;</span>
          </div>
          <!-- Navigation -->
          <div class="flex items-center space-x-4">
            <button id="animatedButton" class="bg-white text-blue-600 px-4 py-2 rounded-lg shadow-md border border-blue-600 hover:bg-blue-50 transition">
              Archives
            </button>
            <button id="profileButton" class="bg-white text-green-600 px-4 py-2 rounded-lg shadow-md border border-green-600 hover:bg-green-50 transition">
              Profil
            </button>
          </div>
        </div>
      </div>
    </nav>
  
    <!-- Scripts GSAP -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script>
      // Animation pour le bouton "Liste"
      const btn = document.getElementById('animatedButton');
      btn.onmouseenter = () => gsap.to(btn, { scale: 1.1, boxShadow: '0px 10px 20px rgba(0, 0, 255, 0.3)', duration: 0.3 });
      btn.onmouseleave = () => gsap.to(btn, { scale: 1, boxShadow: '0px 4px 6px rgba(0, 0, 255, 0.15)', duration: 0.3 });
      btn.onclick = () => (location.href = 'liste.html');
  
      // Animation pour le bouton "Profil"
      const profileBtn = document.getElementById('profileButton');
      profileBtn.onmouseenter = () => gsap.to(profileBtn, { scale: 1.1, boxShadow: '0px 10px 20px rgba(0, 128, 0, 0.3)', duration: 0.3 });
      profileBtn.onmouseleave = () => gsap.to(profileBtn, { scale: 1, boxShadow: '0px 4px 6px rgba(0, 128, 0, 0.15)', duration: 0.3 });
      profileBtn.onclick = () => alert('Redirection vers le profil');
    </script>
  
  <!-- Formulaire -->
  <div class="max-w-4xl mx-auto my-10 bg-white p-8 rounded-lg shadow">
    <h2 class="text-xl font-semibold italic text-center mb-4">Formulaire de Surveillance de la Grossesse</h2>

    <form id="formulaire" onsubmit="event.preventDefault(); afficherMessageEtReinitialiser();">
      <!-- Informations sur le patient -->
      <fieldset class="mb-6 border border-gray-300 rounded p-4">
        <legend class="text-lg font-medium">Informations sur la Patiente</legend>

        <div class="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label for="nom" class="block text-sm font-medium">Nom complet</label>
            <input type="text" id="nom" name="nom" class="w-full border rounded px-3 py-2" required>
          </div>

          <div>
            <label for="adresse" class="block text-sm font-medium">Adresse</label>
            <input type="text" id="adresse" name="adresse" class="w-full border rounded px-3 py-2" required>
          </div>

          <div>
            <label for="dateNaissance" class="block text-sm font-medium">Date de Naissance</label>
            <input type="date" id="dateNaissance" name="dateNaissance" class="w-full border rounded px-3 py-2" onchange="calculerAge(this.value, 'age')" required>
          </div>

          <div>
            <label for="age" class="block text-sm font-medium">Âge</label>
            <input type="number" id="age" name="age" class="w-full border rounded px-3 py-2" readonly>
          </div>

          <div>
            <label for="statut" class="block text-sm font-medium">Statut Matrimonial</label>
            <select id="statut" name="statut" class="w-full border rounded px-3 py-2" onchange="gererStatutMatrimonial(this.value)" required>
              <option value="">-- Sélectionnez --</option>
              <option value="Célibataire">Célibataire</option>
              <option value="Mariée">Mariée</option>
              <option value="Divorcée">Divorcée</option>
              <option value="Veuve">Veuve</option>
              <option value="Concubine">Concubine</option>
              <option value="En couple">En couple</option>
            </select>
          </div>

          <div>
            <label for="occupation" class="block text-sm font-medium">Occupation</label>
            <input type="text" id="occupation" name="occupation" class="w-full border rounded px-3 py-2">
          </div>

          <div>
            <label for="numeroPersonnel" class="block text-sm font-medium">Numéro Personnel</label>
            <input type="text" id="numeroPersonnel" name="numeroPersonnel" class="w-full border rounded px-3 py-2">
          </div>

          <div>
            <label for="numeroEtablissement" class="block text-sm font-medium">Numéro Bureau</label>
            <input type="text" id="numeroEtablissement" name="numeroEtablissement" class="w-full border rounded px-3 py-2">
          </div>
        </div>
      </fieldset>

      <!-- Informations sur le conjoint -->
      <fieldset id="infoConjoint" class="mb-6 border border-gray-300 rounded p-4 hidden">
        <legend class="text-lg font-medium">Informations sur le Conjoint</legend>

        <div class="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label for="nomConjoint" class="block text-sm font-medium">Nom et Prénom du Conjoint</label>
            <input type="text" id="nomConjoint" name="nomConjoint" class="w-full border rounded px-3 py-2">
          </div>

          <div>
            <label for="occupationConjoint" class="block text-sm font-medium">Occupation du Conjoint</label>
            <input type="text" id="occupationConjoint" name="occupationConjoint" class="w-full border rounded px-3 py-2">
          </div>

          <div>
            <label for="numeroTelConjoint" class="block text-sm font-medium">Numéro de Téléphone du Conjoint</label>
            <input type="text" id="numeroTelConjoint" name="numeroTelConjoint" class="w-full border rounded px-3 py-2">
          </div>

          <div>
            <label for="numeroEtablissementConjoint" class="block text-sm font-medium">Numéro Bureau</label>
            <input type="text" id="numeroEtablissementConjoint" name="numeroEtablissementConjoint" class="w-full border rounded px-3 py-2">
          </div>

          <div>
            <label for="dateNaissanceConjoint" class="block text-sm font-medium">Date de Naissance du Conjoint</label>
            <input type="date" id="dateNaissanceConjoint" name="dateNaissanceConjoint" class="w-full border rounded px-3 py-2" onchange="calculerAge(this.value, 'ageConjoint')">
          </div>

          <div>
            <label for="ageConjoint" class="block text-sm font-medium">Âge du Conjoint</label>
            <input type="number" id="ageConjoint" name="ageConjoint" class="w-full border rounded px-3 py-2" readonly>
          </div>
        </div>
      </fieldset>

 <!-- Résumé de la Grossesse -->
 <div class="mb-6 border border-gray-300 rounded p-4">
    <h3 class="text-lg font-medium text-center mb-4">Résumé de la Grossesse</h3>
    
    <!-- Histoire Menstruelle -->
    <div class="mb-4">
      <h4 class="font-medium mb-2">Histoire Menstruelle (Antécédents menstruels)</h4>
      <div class="grid grid-cols-2 gap-4">
        <div class="flex items-center gap-4">
            <div class="w-1/2">
              <label for="ddr" class="block text-sm font-medium">DDR</label>
              <input type="date" id="ddr" name="ddr" class="w-full border rounded px-3 py-2" onchange="calculerDPA(this.value, 'dpa')">
            </div>
            <div class="w-1/2">
              <label for="dpa" class="block text-sm font-medium">DPA</label>
              <input type="text" id="dpa" name="dpa" class="w-full border rounded px-3 py-2" readonly>
            </div>
          </div>
          
          <script>
            function calculerDPA(ddr, cibleId) {
              if (!ddr) return;
              const dpa = new Date(new Date(ddr).setDate(new Date(ddr).getDate() + 280));
              const options = { year: 'numeric', month: 'long', day: 'numeric' };
              document.getElementById(cibleId).value = `${dpa.toLocaleDateString('fr-FR', options)} (${Math.max(0, Math.floor((dpa - new Date()) / (1000 * 60 * 60 * 24 * 30.44)))} mois restants)`;
            }
          </script>
          

        <div>
          <label for="cycle" class="block text-sm font-medium">Cycle</label>
          <select id="cycle" name="cycle" class="w-full border rounded px-3 py-2">
            <option value="">-- Sélectionnez --</option>
            <option value="Régulier">Régulier</option>
            <option value="Irrégulier">Irrégulier</option>
          </select>
        </div>

        <div>
          <label for="duree" class="block text-sm font-medium">Durée</label>
          <input type="text" id="duree" name="duree" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="g" class="block text-sm font-medium">G</label>
          <input type="text" id="g" name="g" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="a" class="block text-sm font-medium">A</label>
          <input type="text" id="a" name="a" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="t" class="block text-sm font-medium">T</label>
          <input type="text" id="t" name="t" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="e" class="block text-sm font-medium">E</label>
          <input type="text" id="e" name="e" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="p" class="block text-sm font-medium">P</label>
          <input type="text" id="p" name="p" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="muit" class="block text-sm font-medium">Muit</label>
          <input type="text" id="muit" name="muit" class="w-full border rounded px-3 py-2">
        </div>
      </div>
    </div>
    <hr class="my-6 border-gray-400">
    <!-- Contraception -->
    <div class="mb-4">
      <h4 class="font-medium mb-2">Contraception</h4>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="type" class="block text-sm font-medium">Type</label>
          <input type="text" id="type" name="type" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="commentaireType" class="block text-sm font-medium">Commentaire</label>
          <input type="text" id="commentaireType" name="commentaireType" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="duree" class="block text-sm font-medium">Durée</label>
          <input type="text" id="dureeContraception" name="dureeContraception" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="commentaireDuree" class="block text-sm font-medium">Commentaire</label>
          <input type="text" id="commentaireDuree" name="commentaireDuree" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="derniereUtilisation" class="block text-sm font-medium">Dernière Utilisation</label>
          <input type="text" id="derniereUtilisation" name="derniereUtilisation" class="w-full border rounded px-3 py-2">
        </div>

        <div>
          <label for="commentaireDerniereUtilisation" class="block text-sm font-medium">Commentaire</label>
          <input type="text" id="commentaireDerniereUtilisation" name="commentaireDerniereUtilisation" class="w-full border rounded px-3 py-2">
        </div>
      </div>
    </div>
    <hr class="my-6 border-gray-400">
    <!-- Histoire de la Grossesse -->
    <div>
        <h4 class="font-medium mb-2">Histoire de la Grossesse (Antécédents de grossesse)</h4>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="saignement" class="block text-sm font-medium">Saignement</label>
            <select id="saignement" name="saignement" class="w-full border rounded px-3 py-2">
              <option value="" disabled selected>Sélectionner</option>
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>
      
          <div>
            <label for="vomissement" class="block text-sm font-medium">Vomissement</label>
            <select id="vomissement" name="vomissement" class="w-full border rounded px-3 py-2">
              <option value="" disabled selected>Sélectionner</option>
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>
      
          <div>
            <label for="fievre" class="block text-sm font-medium">Fièvre</label>
            <select id="fievre" name="fievre" class="w-full border rounded px-3 py-2">
              <option value="" disabled selected>Sélectionner</option>
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>
      
          <div>
            <label for="tabac" class="block text-sm font-medium">Tabac</label>
            <select id="tabac" name="tabac" class="w-full border rounded px-3 py-2">
              <option value="" disabled selected>Sélectionner</option>
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>
      
          <div>
            <label for="alcool" class="block text-sm font-medium">Alcool</label>
            <select id="alcool" name="alcool" class="w-full border rounded px-3 py-2">
              <option value="" disabled selected>Sélectionner</option>
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>
      
          <div>
            <label for="radiation" class="block text-sm font-medium">Radiation</label>
            <select id="radiation" name="radiation" class="w-full border rounded px-3 py-2">
              <option value="" disabled selected>Sélectionner</option>
              <option value="Oui">Oui</option>
              <option value="Non">Non</option>
            </select>
          </div>
        </div>
      </div>
      
      <hr class="my-6 border-gray-400">
       <!-- Histoire Obstétrique -->
       <div class="mb-6">
        <h4 class="font-medium mb-2">Histoire Obstétrique</h4>
        <div class="overflow-x-auto">
          <table class="min-w-full table-auto border border-gray-300">
            <thead>
              <tr class="bg-gray-100">
                <th class="border px-4 py-2">No.</th>
                <th class="border px-4 py-2">Année</th>
                <th class="border px-4 py-2">Sexe</th>
                <th class="border px-4 py-2">Âge gest.</th>
                <th class="border px-4 py-2">Poids</th>
                <th class="border px-4 py-2">Lieu d'acc.</th>
                <th class="border px-4 py-2">Type d'acc.</th>
                <th class="border px-4 py-2">Radiation</th>
                <th class="border px-4 py-2">Remarques</th>
              </tr>
            </thead>
            <tbody>
              <!-- Rangées dynamiques -->
              <tr>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
              </tr>
              <tr>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
              </tr>
              <tr>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
                <td class="border px-4 py-4"><input type="text" class="w-full border-none"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- Histoire Médicale -->
      <div class="mb-6 border border-gray-300 rounded p-4">
        <h3 class="text-lg font-medium text-center mb-4">Histoire Médicale</h3>

        <!-- Antécédents Médicaux -->
        <div class="mb-4">
          <h4 class="font-medium mb-2">Antécédents Médicaux</h4>
          <table class="w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                <th class="border border-gray-300 px-4 py-2">Problèmes de santé</th>
                <th class="border border-gray-300 px-4 py-2">O/N</th>
                <th class="border border-gray-300 px-4 py-2">Remarques</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Maladies rénales</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Problèmes cardiaques</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Hypertension artérielle</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Diabète</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Infection</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Maladie de la Thyroïde</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Transfusion</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Chirurgie</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Herpès</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
            </tbody>
          </table>
        </div>
        <hr class="my-6 border-gray-400">
        <!-- Antécédents Hérédo-Collatéraux -->
        <div>
          <h4 class="font-medium mb-2">Antécédents Hérédo-Collatéraux (Antécédents médicaux familiaux)</h4>
          <table class="w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                <th class="border border-gray-300 px-4 py-2">Les antécédents familiaux</th>
                <th class="border border-gray-300 px-4 py-2">O/N</th>
                <th class="border border-gray-300 px-4 py-2">Commentaires</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Hypertension</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Diabètes</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Maladie cardiaque</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Gémellaire</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Malformation</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
              <tr>
                <td class="border border-gray-300 px-4 py-2">Maladie génétique</td>
                <td class="border border-gray-300 px-4 py-2">
                  <select class="w-full border rounded">
                    <option disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                    <option value="Inconnu">Inconnu</option>
                  </select>
                </td>
                <td class="border border-gray-300 px-4 py-2"><input type="text" class="w-full border rounded"></td>
              </tr>
            </tbody>
        </table>
      </div>

      <hr style="border: 1px solid #ddd; margin: 20px 0;">
      <!-- Nutrition-Counseling -->
      <div class="mb-6 border border-gray-300 rounded p-4">
        <h3 class="text-lg font-medium text-center mb-4">Nutrition-Counseling</h3>

        <!-- Conseils Nutritionnels -->
        <div class="mb-4">
          <h4 class="font-medium mb-2">Conseils Nutritionnels</h4>
          <table class="table-auto w-full border border-gray-300">
            <thead>
              <tr class="bg-gray-200">
                <th class="border px-4 py-2">Liste des groupes d'aliments</th>
                <th class="border px-4 py-2">O/N</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="border px-4 py-2">Produits laitiers</td>
                <td class="border px-4 py-2">
                  <select id="produitsLaitiers" name="produitsLaitiers" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Pain et céréales</td>
                <td class="border px-4 py-2">
                  <select id="painCereales" name="painCereales" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Fruits et légumes</td>
                <td class="border px-4 py-2">
                  <select id="fruitsLegumes" name="fruitsLegumes" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Sources protéiniques</td>
                <td class="border px-4 py-2">
                  <select id="sourcesProteiniques" name="sourcesProteiniques" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <hr class="my-6 border-gray-400">
        <!-- Sujet de Counseling -->
        <div class="mb-4">
          <h4 class="font-medium mb-2">Sujet de Counseling</h4>
          <table class="table-auto w-full border border-gray-300">
            <thead>
              <tr class="bg-gray-200">
                <th class="border px-4 py-2">Plan nutritionnel</th>
                <th class="border px-4 py-2">O/N</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="border px-4 py-2">Tabagisme</td>
                <td class="border px-4 py-2">
                  <select id="tabagisme" name="tabagisme" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Alcoolisme</td>
                <td class="border px-4 py-2">
                  <select id="alcoolisme" name="alcoolisme" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Les stupéfiants</td>
                <td class="border px-4 py-2">
                  <select id="stupefiants" name="stupefiants" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Les médicaments</td>
                <td class="border px-4 py-2">
                  <select id="medicaments" name="medicaments" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Travail</td>
                <td class="border px-4 py-2">
                  <select id="travail" name="travail" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Exercice</td>
                <td class="border px-4 py-2">
                  <select id="exercice" name="exercice" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Rapport Sexuel</td>
                <td class="border px-4 py-2">
                  <select id="rapportSexuel" name="rapportSexuel" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Complications de la grossesse</td>
                <td class="border px-4 py-2">
                  <select id="complicationsGrossesse" name="complicationsGrossesse" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Soins Dentaires</td>
                <td class="border px-4 py-2">
                  <select id="soinsDentaires" name="soinsDentaires" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Allaitement maternel</td>
                <td class="border px-4 py-2">
                  <select id="allaitementMaternel" name="allaitementMaternel" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
              <tr>
                <td class="border px-4 py-2">Classe Prénatale</td>
                <td class="border px-4 py-2">
                  <select id="classePrenatale" name="classePrenatale" class="w-full border rounded px-2 py-1">
                    <option value="" disabled selected>Sélectionner</option>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

   <!-- Examen Physique Initiale -->
   <div class="mb-6 border border-gray-300 rounded p-6">
    <h3 class="text-lg font-medium text-center mb-4">Examen Physique Initiale</h3>

    <!-- Tableau 1 -->
    <table class="table-auto w-full border border-gray-300 mb-4">
      <thead>
        <tr class="bg-gray-200">
          <th class="border px-4 py-2">Organes</th>
          <th class="border px-4 py-2">Poids et Commentaires</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="border px-4 py-2">Tête, cou, thyroïde</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Dents</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Thorax</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Seins</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Système Cardio-Vasculaire</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Abdomen</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
      </tbody>
    </table>
<!-- Tableau 2 -->
<table class="table-auto w-full border border-gray-300 mb-4">
  <thead>
    <tr class="bg-gray-200">
      <th class="border px-4 py-2">Structure osseuse</th>
      <th class="border px-4 py-2"> Observation et commentaire</th>
    </tr>
  </thead>
  <tbody>

    <tr>
      <td class="border px-4 py-2">Bassin</td>
      <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
    </tr>

  </tbody>
</table>

    <!-- Tableau 4 -->
    <table class="table-auto w-full border border-gray-300 mb-4">
      <thead>
        <tr class="bg-gray-200">
          <th class="border px-4 py-2">Organes</th>
          <th class="border px-4 py-2"> Taille et Commentaires</th>
        </tr>
      </thead>
      <tbody>

        <tr>
          <td class="border px-4 py-2">Vulve</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Vagin</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Col</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Utérus</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Anus</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
        <tr>
          <td class="border px-4 py-2">Varicosités</td>
          <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-2 py-1"></td>
        </tr>
      </tbody>
    </table>
    <hr class="my-6 border-gray-400">
    <!-- Observations -->
    <div class="mb-4">
      <h4 class="font-medium mb-2">Observations</h4>
      <textarea class="w-full border rounded px-3 py-2 h-24"></textarea>
    </div>

    <!-- Risques identifiés -->
    <div>
      <h4 class="font-medium mb-2">Risques identifiés : Allergie - Médication</h4>
      <textarea class="w-full border rounded px-3 py-2 h-16"></textarea>
    </div>
  </div>

      <!-- Immunisation et Tests -->
      <div class="mb-6 border border-gray-300 rounded p-6">
        <h3 class="text-lg font-medium text-center mb-4">Immunisation et Tests</h3>
        <table class="table-auto w-full border border-gray-300">
          <thead>
            <tr class="bg-gray-200">
              <th class="border px-4 py-2">Test</th>
              <th class="border px-4 py-2">Résultat</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="border px-4 py-2">Immunisation</td>
              <td class="border px-4 py-2">
                <input type="text" class="w-full border rounded px-2 py-1" placeholder="Résultat">
              </td>
            </tr>
            <tr>
              <td class="border px-4 py-2">Sérologie Rubéole</td>
              <td class="border px-4 py-2">
                <input type="text" class="w-full border rounded px-2 py-1" placeholder="Résultat">
              </td>
            </tr>
            <tr>
              <td class="border px-4 py-2">HBs Ag</td>
              <td class="border px-4 py-2">
                <input type="text" class="w-full border rounded px-2 py-1" placeholder="Résultat">
              </td>
            </tr>
            <tr>
              <td class="border px-4 py-2">Syphilis</td>
              <td class="border px-4 py-2">
                <select id="syphilis" name="syphilis" class="w-full border rounded px-2 py-1">
                  <option value="" disabled selected>Sélectionner</option>
                  <option value="Oui">Oui</option>
                  <option value="Non">Non</option>
                </select>
              </td>
            </tr>
            <tr>
              <td class="border px-4 py-2">Hb</td>
              <td class="border px-4 py-2">
                <input type="text" class="w-full border rounded px-2 py-1" placeholder="Résultat">
              </td>
            </tr>
            <tr>
              <td class="border px-4 py-2">GS</td>
              <td class="border px-4 py-2">
                <select id="gs" name="gs" class="w-full border rounded px-2 py-1">
                  <option value="" disabled selected>Sélectionner</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
              </td>
            </tr>
            <tr>
              <td class="border px-4 py-2">HIV</td>
              <td class="border px-4 py-2">
                <select id="hiv" name="hiv" class="w-full border rounded px-2 py-1">
                  <option value="" disabled selected>Sélectionner</option>
                  <option value="Oui">Oui</option>
                  <option value="Non">Non</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Remarque -->
        <div class="mt-6">
          <h4 class="font-medium mb-2">Remarque</h4>
          <textarea class="w-full border rounded px-3 py-2 h-24"></textarea>
        </div>
      </div>


<!-- Visites Subséquentes -->
<div class="mb-6 border border-gray-300 rounded p-6 overflow-x-auto">
  <h3 class="text-lg font-medium text-center mb-4">Visites Subséquentes</h3>
  <table class="table-auto w-full border border-gray-300">
    <thead>
      <tr class="bg-gray-200">
        <th class="border px-8 py-3">Date</th>
        <th class="border px-8 py-3">Poids</th>
        <th class="border px-8 py-3">Âge gestationnel</th>
        <th class="border px-8 py-3">HU</th>
        <th class="border px-8 py-3">Prés/Post</th>
        <th class="border px-8 py-3">BDCF</th>
        <th class="border px-8 py-3">TA</th>
        <th class="border px-8 py-3">Urine Pr/Glu</th>
        <th class="border px-8 py-3">Risque</th>
        <th class="border px-8 py-3">Commentaire Lab/Med</th>
      </tr>
    </thead>
    <tbody id="table-body">
      <!-- Ligne initiale -->
      <tr>
        <td class="border px-4 py-2"><input type="date" class="w-full border rounded px-3 py-2"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Poids"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Âge gestationnel"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="HU"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Prés/Post"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="BDCF"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="TA"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Urine Pr/Glu"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Risque"></td>
        <td class="border px-4 py-2">
          <textarea class="w-full border rounded px-3 py-2 h-16" placeholder="Commentaire Lab/Med"></textarea>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Script corrigé pour ajouter des lignes -->
  <script>
    function ajouterLigne() {
      const tableBody = document.getElementById("table-body");

      if (!tableBody) {
        console.error("Erreur : corps de la table non trouvé !");
        return;
      }

      // Création d'une nouvelle ligne
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="border px-4 py-2"><input type="date" class="w-full border rounded px-3 py-2"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Poids"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Âge gestationnel"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="HU"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Prés/Post"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="BDCF"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="TA"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Urine Pr/Glu"></td>
        <td class="border px-4 py-2"><input type="text" class="w-full border rounded px-3 py-2" placeholder="Risque"></td>
        <td class="border px-4 py-2">
          <textarea class="w-full border rounded px-3 py-2 h-16" placeholder="Commentaire Lab/Med"></textarea>
        </td>`;
      
      // Ajout de la ligne au tableau
      tableBody.appendChild(row);
    }
  </script>

  <!-- Bouton pour ajouter une ligne -->
  <button onclick="ajouterLigne()" class="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md shadow hover:bg-blue-700">
    Ajouter une ligne
  </button>
</div>


  <!-- Bouton de soumission -->
  <button type="submit" class="bg-blue-600 text-white px-6 py-2 rounded-md shadow hover:bg-blue-700">Enregistrer</button>
</form>

<!-- Message de confirmation -->
<div id="message" class="hidden mt-4 p-4 bg-green-100 text-green-800 rounded-md">
  <span class="font-medium">Succès :</span> Le formulaire a été enregistré avec succès !
</div>
</div>
</body>
</html>


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

@app.route('/archives')
def archives():
    return render_template('archives.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)