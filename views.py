from flask import Flask, render_template, request
import sqlite3

#Création de la base de données avec la table NUMEROS
conn = sqlite3.connect('baseDonnees.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS NUMEROS(id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TXT, numero TXT)")
conn.commit()

cur.close()
conn.close()

#Initialisation de l'app Flask
app = Flask(__name__)

#Page d'accueil de l'annuaire
@app.route('/')
def index():
  return render_template('index.html')

#Page d'ajout de contacts
@app.route('/ajout')
def ajout():
    return render_template("ajout.html")

#Page de recherche de contacts
@app.route('/recherche')
def recherche():
  return render_template("recherche.html")

#Page de confirmation d'ajout de contact
@app.route('/ajout_ok',methods = ['POST'])
def ajout_ok():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  enregistrement_bd((n, p, nt))
  return render_template("ajout_ok.html", nom=n, prenom=p, numero=nt)

#Page des résultats de la recherche qui renvoie la liste des contacts trouvés
@app.route('/recherche_resultats',methods = ['POST'])
def recherche_resultats():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  liste_contacts=recherche_bd((n, p, nt))[0]
  return render_template("recherche_resultats.html", liste_c=liste_contacts)

#Page de la liste des contacts
@app.route('/liste_contacts')
def liste_contacts():
    return render_template("liste_contacts.html", data=recup_donnees())

#Page de la modification d'un contact
@app.route('/modification',methods = ['POST'])
def modification():
  result = request.form
  id_c = result['id_c']
  return render_template("modification.html", id_contact=id_c)

#Page de confirmation de modification d'un contact
@app.route('/modif_ok',methods = ['POST'])
def modif_ok():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  id_c = result['id_c']
  modif_contact(id_c, (n, p, nt))
  return render_template("modif_ok.html")

#Page de confirmation de supression d'un contact, avec des input type radio oui ou non
@app.route('/suppr_confirmation',methods = ['POST'])
def suppr_confirmation():
    result = request.form
    id_c = result['id_c']
    return render_template("suppr_confirmation.html", id_contact=id_c)
  
#Page de suppression d'un contact
@app.route('/suppr_contact',methods = ['POST'])
def suppr_contact():
  result = request.form
  id_c = result['id_c']
  choix = result['choix']
  #Si le choix sur la page précédente était oui, on supprime le contact
  if choix=="oui":
    suppr_contact(id_c)
    return render_template("suppr_ok.html")
  #Sinon on renvoie l'utilisateur à la page d'accueil
  else:
    return render_template("index.html")

#Fonctions base de données

def enregistrement_bd(values):
    """
    Fonction qui prend en paramètre un tuple de 3 valeurs, puis qui les enregistre dans la base de données
    """
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("INSERT INTO NUMEROS (nom, prenom, numero) VALUES (?, ?, ?)", (values[0], values[1], "/"+values[2]))
    conn.commit()
    
    cur.close()
    conn.close()

def recherche_bd(values):
    """
    Fonction qui prend en paramètre un tuple de 3 valeurs, puis qui renvoie les tuples de données correspondant de la base de données
    """
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    data=[]
    cur.execute("SELECT id, nom, prenom, numero FROM NUMEROS WHERE nom = ? OR prenom = ? OR numero = ?",(values[0], values[1], "/"+values[2]))
    data.append(cur.fetchall())
    
    cur.close()
    conn.close()
    
    return data

def modif_contact(id_c, values):
    """
    Fonction qui prend en paramètre un entier correspondant à un id d'un contact de la base de données et un tuple de 3 valeurs,
    puis qui modifie ce contact par rapport au tuple
    """
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("UPDATE NUMEROS SET nom = ?, prenom = ?, numero = ? WHERE id = ?", (values[0], values[1], "/"+values[2], id_c[0]))
    conn.commit()
    
    cur.close()
    conn.close()

def suppr_contact(id_c):
    """
    Fonction qui prend en paramètre un entier correspondant à l'id d'un contact, puis qui supprime ce contact de la base de données
    """
    print(id_c)
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("DELETE FROM NUMEROS WHERE id = ?", (id_c,))
    conn.commit()
    
    cur.close()
    conn.close()

def recup_donnees():
    """
    Fonction qui renvoie toutes les données de la base de données sous la forme d'une liste de tuples
    """
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    cur.execute("SELECT id, nom, prenom, numero FROM NUMEROS")

    return cur.fetchall()

#Lancement de l'application Flask, à l'URL : http://localhost:5000
app.run(port=5000)
