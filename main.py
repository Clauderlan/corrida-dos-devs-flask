from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import bcrypt
from json import dumps
from flask_cors import CORS, cross_origin

#Precisa instalar os 4 pacotes: clica em packages e digita o nome do pacote
#Flask
#Flask-SQLAlchemy
#Flask-Restful
#Jsonify

# Conectando ao BD exemplo feito em SQLLITE
db_connect = create_engine('sqlite:///sqlite.db')

##Coloca o servidor Web no ar
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False # Não ordernar o JSON
api = Api(app)
cors = CORS(app)


class Users(Resource):

  def get(self):  # Mostra todos os usuários cadastrados no BD
    conn = db_connect.connect()
    query = conn.execute("select id, userName, userbio, useremail, userrankpoints from user")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    #print(result[2]) -> User per User
    return jsonify(result)

  def post(self):  # Inclui no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    userName = request.json['userName']
    userEmail = request.json['userEmail']
    userPassword = request.json['userPassword']
    hashedPass = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())
    userBio = request.json['userBio']
    userRankPoints = request.json['userRankPoints']
    conn.execute(
      "insert into aluno values(null, '{0}','{1}','{2}','{3}','{4}')".format(
        userName, hashedPass.decode('utf8'), userBio, userEmail, userRankPoints))
    query = conn.execute('select id, userName, userbio, useremail, userrankpoints from user order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def patch(self): # Request //-> id, patchAtribute, 
      
      conn = db_connect.connect()
      id = request.json['id']
      patchColumn = request.json['patchColumn']
      valueColumn = request.json['valueColumn']
      conn.execute("update user set {0} = '{1}' where id = '{2}'".format(patchColumn, valueColumn, id))
      #conn.execute("update user set " + patchColumn + "='" + int(userRankPoints) + "' where id =%d " % int(id))
      query = conn.execute("select * from user where id=%d " % int(id))
      result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      return jsonify(result)      
      
  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    userName = request.json['userName']
    userEmail = request.json['userEmail']
    userPassword = request.json['userPassword']
    hashedPass = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())
    userBio = request.json['userBio']
    userRankPoints = request.json['userRankPoints']
    

    conn.execute("update user set username ='" + str(userName) + "', useremail ='" + str(userEmail) + "', userpassword='" + hashedPass.decode("utf8") + "', userbio= '" + str(userBio) + "', userrankPoints= " + str(userRankPoints) + " where id =%d " % int(id))

      
      
    query = conn.execute("select id, userName, userbio, useremail, userrankpoints from user where id=%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class Material(Resource):

  def get(self):  # Mostra todos os usuários cadastrados no BD
    conn = db_connect.connect()
    query = conn.execute("select * from material")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def post(self):  # Inclui no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    materialTitle = request.json['materialTitle']
    materialDescription = request.json['materialDescription']
    materialThumbnailUrl = request.json['materialThumbnailUrl']
    materialDataView = request.json['materialDataView']

    conn.execute(
      "insert into material values(null, '{0}','{1}', '{2}', '{3}')".format(
        materialTitle, materialDescription, materialThumbnailUrl, materialDataView))

    query = conn.execute('select * from material order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    materialId = request.json['materialId']
    materialTitle = request.json['materialTitle']
    materialDescription = request.json['materialDescription']
    materialThumbnailUrl = request.json['materialThumbnailUrl']
    materialDataView = request.json['materialDataView']

    conn.execute("update material set materialtitle ='" + str(materialTitle) +
                 "', materialdescription ='" + str(materialDescription) + "', materialImageURL='" +
                 str(materialThumbnailUrl) + "', materialvisibilityDate='" + str(materialDataView) +
                 "'  where id =%d " % int(materialId))

    query = conn.execute("select * from material where id=%d " % int(materialId))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class Challenges(Resource):

  def get(self):  # Mostra todos os usuários cadastrados no BD
    conn = db_connect.connect()
    query = conn.execute("select * from challenge")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def post(self):  # Inclui no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    challengeTitle = request.json['challengeTitle']
    challengeBio = request.json['challengeBio']
    challengeRequirements = request.json['challengeRequirements']
    challengeDeadline = request.json['challengeDeadline']
    challengeImageURL = request.json['challengeImageURL']
    challengePoints = request.json['challengePoints']

    conn.execute(
      "insert into challenge values(null, '{0}','{1}', '{2}', '{3}', '{4}', '{5}')"
      .format(challengeTitle, challengeBio, challengeRequirements, challengeDeadline, challengeImageURL, challengePoints))

    query = conn.execute('select * from challenge order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    challengeTitle = request.json['challengeTitle']
    challengeDescription = request.json['challengeDescription']
    challengeRequirements = request.json['challengeRequirements']
    challengeDeadline = request.json['challengeDeadline']
    challengeImageURL = request.json['challengeImageURL']
    challengePoints = request.json['challengePoints']

    conn.execute("update challenge set challengetitle ='" + str(challengeTitle) + "', challengedescription ='" +
                 str(challengeDescription) + "', challengeimageUrl='" + str(challengeImageURL) +
                 "', challengerequirements ='" + str(challengeRequirements) + "', challengedeadline='" +
                 str(challengeDeadline) + "', challengepoints='" + str(challengePoints) +
                 "'  where id =%d " % int(id))

    query = conn.execute("select * from challenge where id=%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class ChallengeResponse(Resource):

  def get(self):  # Mostra todos os usuários cadastrados no BD
    conn = db_connect.connect()
    query = conn.execute("select * from challengeResponse")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def post(self):  # Inclui no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    challengeLinkResponse = request.json['challengeLinkResponse']
    userId = request.json['userId']
    challengeId = request.json['challengeId']
    conn.execute("insert into challengeresponse values(null, '{0}','{1}','{2}')".format(
      challengeId, userId, challengeLinkResponse))
    query = conn.execute(
      'select * from challengeResponse order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    challengeLinkResponse = request.json['challengeLinkResponse']
    userId = request.json['userId']
    challengeId = request.json['challengeId']

    conn.execute("update challengeResponse set challengeId ='" + str(challengeId) + "', userId ='" + str(userId) + "', challengeLinkResponse='" + str(challengeLinkResponse) + "' where id =%d " % int(id))

    query = conn.execute("select * from challengeResponse where id=%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class UserById(Resource): 
  def delete(self, id): # Deleta no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    conn.execute("delete from user where id=%d " % int(id))
    return {"status": "success"}

  def get(self, id): # Busca no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    query = conn.execute("select * from user where id =%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result

class UserByLogin(Resource): 
  def get(self, login): # Busca no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    query = conn.execute('select * from user where userName = "%s"' % str(login))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result

class MaterialById(Resource): 
  def delete(self, id): # Deleta no BD de um material passado como parâmetro
    conn = db_connect.connect()
    conn.execute("delete from material where id=%d " % int(id))
    return {"status": "success"}

  def get(self, id): # Busca no BD um material passado como parâmetro
    conn = db_connect.connect()
    query = conn.execute("select * from material where id =%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result

@app.route("/var", methods=["POST"]) # Login
def var_user():
    user = request.json
    userById = UserById()
    userByLogin = UserByLogin() # -> Pegar login e senha, para verificar.

    if(not(userByLogin.get(user["login"]))): # Verificando se esse login existe na base de dados.
        return {"message" : 403}
    else:
        userGetLogin = userByLogin.get(user["login"])[0] # Buscando o userById do UserLogin - Creio que esteja obsoleto.
        hashed = userById.get(userGetLogin["id"])[0]["password"] # Password do banco
        # Sempre termina em [0], porque retorna uma lista de JSON.
    password = user["password"] # Password da requisição
    password = password.encode('utf8') # Transformando em byte
    hashed = hashed.encode('utf8') # Transformando em byte
    if(bcrypt.hashpw(password, hashed) == hashed):
        return {"message" : 202}
    else:
        return {"message" : 403}

api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')
api.add_resource(UserByLogin, '/usersbylogin/<login>')
api.add_resource(Material, '/material')
api.add_resource(MaterialById, '/material/<id>')
api.add_resource(Challenges, '/challenges')
api.add_resource(ChallengeResponse, '/challengesresponse')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)