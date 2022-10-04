from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, EmployeeModel

import mysql

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/TSWRDC"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root#123@localhost/ANISOL"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'MySecretKey'
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/' )
def index():
    return redirect('/employees')

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        new_employee = EmployeeModel(name=name, age=age, position=position)
        db.session.add(new_employee)
        db.session.commit()
        flash(f'New employee {name} created successfully !!!')
        return redirect('/employees')
 
@app.route('/employees')
def RetrieveDataList():
    employees = EmployeeModel.query.all()
    return render_template('index.html', employees = employees)

'''
@app.route('/employee/<int:id>')
def RetrieveSingleEmployee(id):
    employee = EmployeeModel.query.filter_by(id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id = {id} does not exist"
'''

@app.route('/update',methods = ['GET','POST'])
def update():
    print('update FORM: {}'.format(request.form))
    if request.method == 'POST':
        existing_employee = EmployeeModel.query.filter_by(id=request.form['id']).first()
        if existing_employee:
            existing_employee.name = request.form['name']
            existing_employee.age = request.form['age']
            existing_employee.position = request.form['position']
            db.session.commit()
            flash(f'{existing_employee} details updated successfully !!!')
            return redirect('/employees')
        else:
            return f"Employee with id = {id} Does nit exist"
    return redirect('/employees')

@app.route('/delete/<int:emp_id>', methods=['GET','POST'])
def delete(emp_id):
    print(f'rrr: {request.method}')
    if request.method == 'GET':
        existing_employee = EmployeeModel.query.filter_by(id=emp_id).first()
        if existing_employee:
            db.session.delete(existing_employee)
            db.session.commit()
            flash(f'{existing_employee} deleted successfully !!!')
            return redirect('/employees')
        else:
            return f"Employee with id = {id} Does nit exist"
    return redirect('/employees')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
