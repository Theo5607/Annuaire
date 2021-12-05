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

@app.route('/recherche_resultats')
def recherche_resultats():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  recherche_bd((n, p, nt))

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
    for i in range(3):
      if value(i)!='':
        if i==0:
          cur.execute("SELECT name, prenom, numero FROM NUMEROS WHERE nom = ?",(values[0],))
          mdp_sing=cur.fetchall()
        elif i==1:
          
    
    cur.close()
    conn.close()

app.run(port=5000)
