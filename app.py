from flask import Flask,render_template,jsonify,request
from neo4j import GraphDatabase, basic_auth
from uuid import uuid4
from flask import Flask, redirect, url_for
import os
from dotenv import load_dotenv
load_dotenv()


DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_URL = os.environ.get("DATABASE_URL")

driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, DATABASE_PASSWORD))


# driver.close()
# print(driver.verify_connectivity(),"asdhasidaskdasdasda")
# print(DATABASE_USERNAME,DATABASE_PASSWORD,DATABASE_URL)

#Aura DB
# uri = "neo4j+s://76eec648.databases.neo4j.io"
# user = "<Username for Neo4j Aura instance>"
# password = "<Password for Neo4j Aura instance>"
# app = App(uri, user, password)

session=driver.session()


app = Flask(__name__)

@app.route('/')
def home():
    query="""MATCH (n) RETURN n"""
    result = session.run(query)
    data=result.data()
    print(data)
    return render_template('index.html',totaldata=data)


@app.route('/update/<string:desc>&<string:amount>&<string:date>&<string:ID>')
def updatePage(desc,amount,date,ID):
    map={"desc":desc,"amount":amount,"date":date,"ID":ID}
    # print(map)
    return render_template('index.html',map=map)



#create 
@app.route("/create",methods=["GET","POST"]) 
def create_node():
    
    with driver.session() as session:
        desc = request.form['desc']
        amount=request.form['amount']
        date=request.form['date']
        # print(desc)

        # bit_size = 32
        uid = str(uuid4())
        print(uid)
        # id = uuid.uuid1().int & (1<<64)-1
        # id = id & (1<<64)-1
        # print(id)

        map={"id":uid,"desc":desc , "amount":amount,"date":date}
        session.run("CREATE (n:Expense{ID:$id,Desc: $desc,Amount:$amount,Date:$date})",map)
        query="""MATCH (n) RETURN n"""
        result = session.run(query)
        data=result.data()
        # print(data)
        return redirect(url_for('home'))

#read
@app.route("/read",methods=['GET'])
def get_nodes():

    query="""MATCH (n) RETURN n.Desc as desc , n.Amount as amount , n.Date as date"""
    result = session.run(query)
    data=result.data()
    return (jsonify(data))

#update
@app.route("/updatenode/<string:ID>",methods=['GET','POST'])
def update_nodes(ID):
    with driver.session() as session:
        Desc = request.form['desc']
        Amount=request.form['amount']
        Date=request.form['date']
        map={"descr":Desc,"amt":Amount,"newdate":Date,"ID":ID}
        query="""MATCH (n:Expense) where n.ID=$ID SET n.Desc=$descr,n.Amount=$amt,n.Date=$newdate"""
        session.run(query,map)
        # data=result.data()
        query="""MATCH (n) RETURN n"""
        result = session.run(query)
        data=result.data()
        print(data)

        return redirect(url_for('home'))
    
    
#delete
@app.route("/delete/<string:ID>",methods=['GET','POST'])
def delete(ID):
    with driver.session() as session:
        map={"id":ID}
        query="""MATCH (n:Expense) where n.ID=$id delete n """
        session.run(query,map)
        query="""MATCH (n) RETURN n"""
        result = session.run(query)
        data=result.data()
        print(data)
        # return render_template('index.html',totaldata=data)
        return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=5050)