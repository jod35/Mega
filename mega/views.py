from mega import app,db
from flask import render_template,url_for,request,flash,redirect
from mega.models import User,Admin
from flask_login import login_user,current_user,logout_user,login_required
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt(app)

@app.route('/home')
def Home():
   return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def Login():
   if current_user.is_authenticated:
      return redirect('/home')


   if request.method=='POST':
      username=request.form.get('username')
      password_candidate=request.form.get('password')
      admin=Admin.query.filter_by(username=username).first()

      if admin and bcrypt.check_password_hash(admin.password,password_candidate):
         login_user(admin)
         return redirect('/home')
   return render_template('login.html')

@app.route('/')
@login_required
def index():
    employees=User.query.all()
    return render_template('index.html',employees=employees)

@app.route('/view')
@login_required
def ViewEmployees():

    employees=User.query.all()
    return render_template('employees.html',employees=employees)

@app.route('/addemp',methods=['GET', 'POST'])
@login_required
def AddEmployee():
    employees=User.query.all()
    if request.method=='POST':
        name=request.form.get('name')
        age=request.form.get('age')
        salary=request.form.get('salary')
        gender=request.form.get('gender')

        new_emp=User(name=name,age=age,salary=salary,gender=gender)
        try:
            db.session.add(new_emp)
            db.session.commit()
            flash('New employee added')
            return redirect('/')        
        except:
            flash('Please fill in correctly')
            return redirect('/addemp')
    return render_template('index.html')


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


@app.route('/deleteadmin/<int:id>',methods=['POST','GET'])
def DeleteAdmin(id):
    admin_to_delete=Admin.query.get_or_404(id)
    db.session.delete(admin_to_delete)
    db.session.commit()
    flash('Employee deleted successfully')
    return redirect('/admin')
  
@app.route('/admin',methods=['GET', 'POST'])
@login_required
def AdminDash():
  
    if request.method=='POST':       
        name=request.form.get('username')
        password=request.form.get('password')
        passwd=bcrypt.generate_password_hash(password)
        new_admin=Admin(username=name,password=passwd)
        try:
             db.session.add(new_admin)
             db.session.commit()
             flash('New Admin User %s Added Successfully!!'%name)
             return redirect('/admin')
        except:
             flash('Please fill in correctly')
    return render_template('admin.html')
       
@app.route('/users')
@login_required
def Users():
    users=Admin.query.all()
    return render_template('user.html',users=users)
    
@app.route('/logout')
def LogOut():
   logout_user()
   return redirect('/home')


@app.route('/updateadmin/<int:id>',methods=['GET', 'POST'])
def UpdateAdmin(id):
    admin=Admin.query.get_or_404(id)
    if request.method=='POST':
        admin.username=request.form.get('username')
        password=request.form.get('password')
        phash=bcrypt.generate_password_hash(password)
        admin.password=phash
        try:
            db.session.commit()
            flash('Info updated successfully')
            return redirect('/users')
        except :
            flash('Update failed')
            return redirect('/users')
    else:
        return render_template('updateadmin.html',admin=admin)


