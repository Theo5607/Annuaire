from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect('baseDonnees.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS NUMEROS(id INT, nom TEXT, prenom TXT, numero INT)")
conn.commit()

cur.close()
conn.close()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/ajout')
def ajout():
    return render_template("ajout.html")

@app.route('/recherche')
def recherche():
  return render_template("recherche.html")

@app.route('/ajout_ok',methods = ['POST'])
def ajout_ok():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  enregistrement_bd((n, p, nt))
  return render_template("ajout_ok.html", nom=n, prenom=p, numero=nt)

@app.route('/recherche_resultats',methods = ['POST'])
def recherche_resultats():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  liste_contacts=recherche_bd((n, p, nt))[0]
  return render_template("recherche_resultats.html", liste_c=liste_contacts)

@app.route('/liste_contacts')
def liste_contacts():
    return render_template("liste_contacts.html", data=recup_donnees())

@app.route('/modification',methods = ['POST'])
def modification():
  result = request.form
  id_c = result['id_c']
  return render_template("modification.html", id_contact=id_c)

@app.route('/modif_ok',methods = ['POST'])
def modif_ok():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  id_c = result['id_c']
  modif_contact(id_c, (n, p, nt))
  return render_template("modif_ok.html")

@app.route('/suppr_contact',methods = ['POST'])
def suppr_contact():
    result = request.form
    id_c = result['id_c']
    suppr_contact(id_c)
    return render_template("suppr_ok.html")

#fonctions base de données

def enregistrement_bd(values):
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("INSERT INTO NUMEROS (nom, prenom, numero) VALUES (?, ?, ?)", (values[0], values[1], values[2]))
    conn.commit()
    
    cur.close()
    conn.close()

def recherche_bd(values):
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    data=[]
    cur.execute("SELECT nom, prenom, numero FROM NUMEROS WHERE nom = ? OR prenom = ? OR numero = ?",(values[0], values[1], values[2]))
    data.append(cur.fetchall())
    
    cur.close()
    conn.close()
    
    return data

def modif_contact(id_c, values):
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("UPDATE NUMEROS SET nom = ?, prenom = ?, numero = ? WHERE id = ?", (values[0], values[1], values[2], id_c[0]))
    conn.commit()
    
    cur.close()
    conn.close()

def suppr_contact(id_c):
    print(id_c)
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("DELETE FROM NUMEROS WHERE id = ?", (id_c,))
    conn.commit()
    
    cur.close()
    conn.close()

def recup_donnees():
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    cur.execute("SELECT id, nom, prenom, numero FROM NUMEROS")

    return cur.fetchall()
    
app.run(port=5000)
