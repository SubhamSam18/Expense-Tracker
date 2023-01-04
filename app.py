from flask import Flask,render_template,jsonify
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
    return render_template('index.html')


#create
@app.route("/create/<string:name>&<int:id>",methods=["GET","POST"]) 
def create_node(name,id):
    
    with driver.session() as session:
        map={"name":name,"id":id}
        session.run("CREATE (n:Employee{NAME: $name,ID:$id})",map)
        x="Node created!"
        print(type(x))
        return x

#read
@app.route("/read",methods=['GET','POST'])
def get_nodes():
    # print("Hello read tab")
    # with driver.session() as session:
    #     # map={"name":name}
    #     # print(name)
    #     result = session.run("MATCH (n) RETURN n.NAME as NAME , n.ID as ID")
    #     print(result.data())
    #     data=result.data()
    #     # # mystring=' '.join(map(str,data))
    #     print("jtuu python",type((jsonify(data))))
    #     # print(session.run("MATCH (n) RETURN n"),'asihdas')
    #     return (jsonify(data))
    query="""MATCH (n) RETURN n.NAME as NAME , n.ID as ID"""
    result = session.run(query)
    data=result.data()
    return (jsonify(data))


@app.route("/update/<string:name>&<string:new_name>",methods=['GET','POST'])
def update_nodes(name,new_name):

    with driver.session() as session:
        map={"name":name,"new_name":new_name}
        query="""MATCH (n:Employee) where n.NAME=$name  SET n.NAME=$new_name """
        session.run(query,map)
        # data=result.data()
        return "Node Updated"
    
@app.route("/delete/<string:name>",methods=['GET','POST'])
def delete(name):
    with driver.session() as session:
        map={"name":name}
        query="""MATCH (n:Employee) where n.NAME=$name  delete n """
        session.run(query,map)
        return "Node Deleted"

if __name__=="__main__":
    app.run(debug=True,port=5050)