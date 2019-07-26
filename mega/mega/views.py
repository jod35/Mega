from mega import app,db
from flask import render_template,url_for,request,flash,redirect
from mega.models import User,Admin
from flask_login import login_required,login_manager
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt(app)


@app.route('/login')
def Login():
   return render_template('login.html')


@app.route('/')

def index():
    employees=User.query.all()
    return render_template('index.html',employees=employees)

@app.route('/view')
def ViewEmployees():
    employees=User.query.all()
    return render_template('employees.html',employees=employees)

@app.route('/addemp',methods=['GET', 'POST'])
def AddEmployee():
    if request.method=='POST':
        name=request.form.get('name')
        age=request.form.get('age')
        salary=request.form.get('salary')
        gender=request.form.get('gender')

        new_emp=User(name=name,age=age,salary=salary,gender=gender)
        db.session.add(new_emp)
        db.session.commit()
        flash('New employee added')
        return redirect('/')

@app.route('/update/<int:id>',methods=['GET', 'POST'])
def Update(id):
    emp=User.query.get_or_404(id)
    if request.method=='POST':
        emp.name=request.form.get('name')
        emp.age=request.form.get('age')
        emp.salary=request.form.get('salary')
        emp.gender=request.form.get('gender')
        try:
            db.session.commit()
            flash('Info updated successfully')
            return redirect('/view')
        except :
            flash('Update failed')
            return redirect('/view')
    else:
        return render_template('update.html',emp=emp)

@app.route('/delete/<int:id>',methods=['POST','GET'])
def Delete(id):
    emp_to_delete=User.query.get_or_404(id)
    db.session.delete(emp_to_delete)
    db.session.commit()
    flash('Employee deleted successfully')
    return redirect('/view')

@app.route('/admin')
def AdminPa():
    admins=Admin.query.all()
    return render_template('admin.html',admins=admins)
   
  
@app.route('/addadmin',methods=['GET', 'POST'])
def AdminDash():
    name=request.form.get('username')
    password=request.form.get('password')
    passwd=bcrypt.generate_password_hash(password)
    new_admin=Admin(username=name,password=passwd)
    db.session.add(new_admin)
    db.session.commit()
    flash('New Admin User %s Added Successfully!!'%name)
    return redirect('/admin')
       
    
    


