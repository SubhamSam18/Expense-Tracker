from flask import Flask,render_template,jsonify,request
from neo4j import GraphDatabase, basic_auth

DATABASE_USERNAME = 'neo4j'
DATABASE_PASSWORD = '12345'
DATABASE_URL = 'bolt://localhost:7687'

driver = GraphDatabase.driver(
  DATABASE_URL,
  auth=basic_auth(DATABASE_USERNAME, DATABASE_PASSWORD))


# driver.close()
# print(driver.verify_connectivity(),"asdhasidaskdasdasda")
print(DATABASE_USERNAME,DATABASE_PASSWORD,DATABASE_URL)

session=driver.session()


app = Flask(__name__)

@app.route('/')
def home():
    query="""MATCH (n) RETURN n"""
    result = session.run(query)
    data=result.data()
    print(data)
    return render_template('index.html',totaldata=data)


@app.route('/update/<string:name>&<int:age>&<int:weight>')
def updatePage(name,age,weight):
    map={"name":name,"age":age,"weight":weight}
    print(map)
    return render_template('index.html',map=map)



#create 
@app.route("/create",methods=["GET","POST"]) 
def create_node():
    
    with driver.session() as session:
        uname = request.form['name']
        age=request.form['age']
        weight=request.form['weight']
        print(uname)
        map={"name":uname , "age":age , "weight":weight}
        session.run("CREATE (n:Employee{NAME: $name,age:$age,weight:$weight})",map)
        # x="Node created!"
        # # print(type(x))
        # return x

        query="""MATCH (n) RETURN n"""
        result = session.run(query)
        data=result.data()
        print(data)
        return render_template('index.html',totaldata=data)


#read
@app.route("/read",methods=['GET'])
def get_nodes():

    query="""MATCH (n) RETURN n.NAME as NAME , n.ID as ID"""
    result = session.run(query)
    data=result.data()
    return (jsonify(data))



#read single node
@app.route("/getSNode",methods=['GET'])
def get_single_node():
    x = request.args.get("NAME")
    # print(x)
    map={"x":x}
    query="""MATCH (n:Employee) WHERE n.NAME=$x RETURN n.NAME """
    # query="""MATCH (n) RETURN n.NAME as NAME , n.ID as ID"""
    result = session.run(query,map)
    data=result.data()
    print(data)
    return (jsonify(data))



#update
@app.route("/update/<string:name>",methods=['GET','POST'])
def update_nodes(name):

    with driver.session() as session:
        uname = request.form['name']
        age=request.form['age']
        weight=request.form['weight']
        map={"new_name":uname,"age":age,"weight":weight,"name":name}
        query="""MATCH (n:Employee) where n.NAME=$name SET n.NAME=$new_name,n.age=$age,n.weight=$weight """
        session.run(query,map)
        # data=result.data()
        query="""MATCH (n) RETURN n"""
        result = session.run(query)
        data=result.data()
        print(data)
        return render_template('index.html',totaldata=data)
    
    
#delete
@app.route("/delete/<string:name>",methods=['GET','POST'])
def delete(name):
    with driver.session() as session:
        map={"name":name}
        query="""MATCH (n:Employee) where n.NAME=$name  delete n """
        session.run(query,map)
        query="""MATCH (n) RETURN n"""
        result = session.run(query)
        data=result.data()
        print(data)
        return render_template('index.html',totaldata=data)

if __name__=="__main__":
    app.run(debug=True,port=5050)