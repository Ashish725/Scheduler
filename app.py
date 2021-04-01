from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ashish.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
class Bhulakad(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title =  db.Column(db.String(200), nullable=False)
    desc =  db.Column(db.String(500), nullable=False)
    date_created= db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route('/',methods=['GET', 'POST'])

def hello_world():
    if request.method=='POST':
        title= request.form['title']
        desc= request.form['desc']
        work= Bhulakad(title =title,desc=desc)
        db.session.add(work)
        db.session.commit()

    
    allwork = Bhulakad.query.all()
    print (allwork)
    return render_template('index.html',allwork= allwork)
 


@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title= request.form['title']
        desc= request.form['desc']
        allwork =Bhulakad.query.filter_by(sno=sno).first()
        allwork.title= title
        allwork.desc= desc
        db.session.add(allwork)
        db.session.commit()
        return redirect('/')
    allwork =Bhulakad.query.filter_by(sno=sno).first()
    return render_template('update.html',allwork= allwork)
    


@app.route('/delete/<int:sno>')
def delete(sno):
    allwork =Bhulakad.query.filter_by(sno=sno).first()
    db.session.delete(allwork)
    db.session.commit()
    return redirect("/")     

if __name__=="__main__":
    app.run(debug=True)