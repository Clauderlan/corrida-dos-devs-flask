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
    query = conn.execute("select * from aluno")
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
    query = conn.execute('select * from aluno order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def patchUserRankPoints(self):
      conn = db_connect.connect()
      id = request.json['id']
      userRankPoints = request.json['rankPoints']
      print(userRankPoints)
      #conn.execute("update aluno set rankPoints='" + int(userRankPoints) + "' where id =%d " % int(id))
      #query = conn.execute("select * from aluno where id=%d " % int(id))
      #result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      #return jsonify(result)
      return id
      
      
  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    userName = request.json['userName']
    userEmail = request.json['userEmail']
    userPassword = request.json['userPassword']
    hashedPass = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())
    userBio = request.json['userBio']
    userRankPoints = request.json['userRankPoints']
    #rankPoints = request.json['rankPoints']
    #challenge = request.json['challenge']
    #socialNetwork = request.json['socialNetwork']

    conn.execute("update aluno set name ='" + str(userName) + "', email ='" + str(userEmail) + "', password='" + hashedPass.decode("utf8") + "', bio= '" + str(userBio) + "', rankPoints='" + int(userRankPoints) + "' where id =%d " % int(id))

    query = conn.execute("select * from aluno where id=%d " % int(id))
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

    conn.execute("update material set title ='" + str(materialTitle) +
                 "', description ='" + str(materialDescription) + "', thumbnailUrl='" +
                 str(materialThumbnailUrl) + "', visibilityDate='" + str(materialDataView) +
                 "'  where id =%d " % int(materialId))

    query = conn.execute("select * from material where id=%d " % int(materialId))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)


class Challenges(Resource):

  def get(self):  # Mostra todos os usuários cadastrados no BD
    conn = db_connect.connect()
    query = conn.execute("select * from desafio")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def post(self):  # Inclui no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    title = request.json['title']
    bio = request.json['bio']
    requirements = request.json['requirements']
    term = request.json['term']
    imageURL = request.json['imageURL']
    points = request.json['points']

    conn.execute(
      "insert into desafio values(null, '{0}','{1}', '{2}', '{3}', '{4}', '{5}')"
      .format(title, bio, requirements, term, imageURL, points))

    query = conn.execute('select * from desafio order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    title = request.json['title']
    bio = request.json['bio']
    requirements = request.json['requirements']
    term = request.json['term']
    imageURL = request.json['imageURL']
    points = request.json['points']

    conn.execute("update desafio set challenge ='" + str(title) + "', bio ='" +
                 str(bio) + "', imageURL='" + str(imageURL) +
                 "', requirements ='" + str(requirements) + "', term='" +
                 str(term) + "', points='" + int(points) +
                 "'  where id =%d " % int(id))

    query = conn.execute("select * from desafio where id=%d " % int(id))
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
    link = request.json['link']
    userId = request.json['userId']
    conn.execute("insert into user values(null, '{0}','{1}')".format(
      userId, link))
    query = conn.execute(
      'select * from challengeResponse order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def put(
      self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    userId = request.json['userId']
    link = request.json['link']

    conn.execute("update user set challenge ='" + str(userId) + "', bio ='" +
                 str(link) + "'  where id =%d " % int(id))

    query = conn.execute("select * from course where id=%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)


class UserById(Resource): 
  def delete(self, id): # Deleta no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    conn.execute("delete from aluno where id=%d " % int(id))
    return {"status": "success"}

  def get(self, id): # Busca no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    query = conn.execute("select * from aluno where id =%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result


class UserByLogin(Resource): 
  def get(self, login): # Busca no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    query = conn.execute('select * from aluno where name = "%s"' % str(login))
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
def var_aluno():
    aluno = request.json
    userById = UserById()
    userByLogin = UserByLogin() # -> Pegar login e senha, para verificar.

    if(not(userByLogin.get(aluno["login"]))): # Verificando se esse login existe na base de dados.
        return {"message" : 403}
    else:
        userGetLogin = userByLogin.get(aluno["login"])[0] # Buscando o userById do UserLogin - Creio que esteja obsoleto.
        hashed = userById.get(userGetLogin["id"])[0]["password"] # Password do banco
        # Sempre termina em [0], porque retorna uma lista de JSON.
    password = aluno["password"] # Password da requisição
    password = password.encode('utf8') # Transformando em byte
    hashed = hashed.encode('utf8') # Transformando em byte
    if(bcrypt.hashpw(password, hashed) == hashed):
        return {"message" : 202}
    else:
        return {"message" : 403}

api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')
api.add_resource(UserByLogin, '/usersByLogin/<login>')
api.add_resource(Material, '/material')
api.add_resource(MaterialById, '/material/<id>')
api.add_resource(Challenges, '/challenges')
api.add_resource(ChallengeResponse, '/challengesResponse')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)