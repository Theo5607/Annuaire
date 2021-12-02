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

@app.route('/ajout_ok',methods = ['POST'])
def resultat():
  result = request.form
  n = result['nom']
  p = result['prenom']
  nt = result['numero']
  return render_template("resultat.html", nom=n, prenom=p, numero=nt)


def enregistrement_bd(values):
    conn = sqlite3.connect('baseDonnees.db')
    cur = conn.cursor()
    
    cur.execute("INSERT INTO NUMEROS (id, nom, prenom) VALUES (?, ?, ?)", (values[0], values[1], values[2]))
    conn.commit()
    
    cur.close()
    conn.close()

app.run(port=5000)
