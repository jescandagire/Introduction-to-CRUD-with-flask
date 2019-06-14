from flask import Flask,request,render_template,jsonify,url_for, redirect
import pymysql

app = Flask(__name__)

#creating a connection to the mysql database created in xampp using the pymysql connector
def db_con():
        db = 'mydb'
        con = pymysql.connect(database=db,user="root",password="",host="localhost")
        con.autocommit(True)
        cursor = con.cursor()
        return (cursor)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

'''
    creating a route to the register function to enable registration of the user after clicking
    on the link in the index.html file. it is going to have both the post and get methods, the post
    for registering and the get will be used during editting the details. Have to create variables 
    for each field on the form and pass the data entered in the form to them using the form attribute
    from the request class and put the column name as used in the database created. redirect and url_for 
    are used when you need to link to a function. the statement of the definition of the "id"variable is
    picking the hidden id and return the respective data for it ''' 

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        cursor =db_con()
        first_name = request.form['firstName']
        email= request.form['email']
        add_user = "INSERT INTO MyUsers(firstName, email) VALUES (%s, %s)"
        cursor.execute(add_user, (first_name,email))
        cursor.close()
        return redirect(url_for('fetchall'))
    else:
        if request.args.get('id'):
            id= request.args.get('id')
            cursor =db_con()
            cursor.execute("SELECT * FROM myusers WHERE id = {}".format(id) )
            data = cursor.fetchone()
            return render_template('form.html', data=data)
        else:
            return render_template('form.html')

''' 
    creating a route for the function that will return the data from the database 
    to the table in the formTable.html. need to create a cursor to the connection to the database,
    a variable for the selecting of the data from the mysql database. this will retun a render to 
    the formTable displaying all the data fetched from the database'''


@app.route('/users', methods=['GET','POST'])
def fetchall():
    cursor =db_con()
    cursor.execute("SELECT * FROM myusers")
    data = cursor.fetchall()
    cursor.close()
    '''if data is None:
        return jsonify({'message':'Bad Request!'})
    else:
        return jsonify(data) #this returns the structure of the data being stored'''
    return render_template('formTable.html', message = request.args.get('Successfully Registered Users'), data=data)


''''
    creating a route to the edit user function, it will be a post method and need to 
    create a connection to the database, creating variables for the features to be 
    editted as well as the id that is to be used to identify the intended user,
    create a variable for the update method in mysql, execute the cursor connection 
    but redirect the finished work to the table which is accessed through the fetchall function '''


@app.route('/edit_user', methods=['POST', 'GET'])
def edit_user():
    if request.method == 'POST':
        cursor =db_con()
        first_name = request.form['firstName']
        email = request.form['email']
        id = request.form['id']
        update_user = "UPDATE MyUsers SET firstName = '{}' , email = '{}' WHERE id='{}'".format(first_name,email,id)
        cursor.execute(update_user)
        cursor.close()
        return redirect(url_for('fetchall'))
    else:
        return("this is not a post request")
            
'''
    creating a route to the delete function, its more like the edit function but for this i
    don't need to return a form and i will only need to match the user with the id so its what
    i have to initialize and use "args" instead of "form" since its a GET request '''

    
@app.route('/delete', methods=['POST','GET'])
def delete_user():
     if request.method == 'GET':
        cursor =db_con()
        id = request.args['id']
        delete_user = "DELETE FROM  MyUsers WHERE id='{}'".format(id)
        cursor.execute(delete_user)
        cursor.close()
        return redirect(url_for('fetchall'))
     else:
        return("this is not a GET request")

   

if __name__ == "__main__": 
    app.run(debug=True)