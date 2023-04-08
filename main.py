from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import bcrypt
from flask_cors import CORS, cross_origin

#Precisa instalar os 4 pacotes:
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
    query = conn.execute("select id, userName, userbio, useremail, userrankpoints from user order by userrankpoints desc")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    challengeContent = ChallengeContentByUserId()
    categoryRule = CategoryByUserId()
    socialName = SocialByUserId()
    for x in result:
        x["userChallengesResponse"] = challengeContent.get(x["id"])
        x["userRule"] = categoryRule.get(x["id"])
        x["socialName"] = socialName.get(x["id"])
    return jsonify(result)

  def post(self):  # Inclui no BD um usuário passado como parâmetro
    conn = db_connect.connect()
    userName = request.json['userName']
    userEmail = request.json['userEmail']
    userPassword = request.json['userPassword']
    hashedPass = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())
    userBio = request.json['userBio']
    userRankPoints = request.json['userRankPoints']
    conn.execute("insert into aluno values(null, '{0}','{1}','{2}','{3}','{4}')".format(userName, hashedPass.decode('utf8'), userBio, userEmail, userRankPoints))
    query = conn.execute('select id, userName, userbio, useremail, userrankpoints from user order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      
    return jsonify(result)
      
  def patch(self): # Patch para atualizar determinado atributo passado pelo request.
      
      conn = db_connect.connect()
      userId = request.json['userId']
      patchColumn = request.json['patchColumn']
      valueColumn = request.json['valueColumn']
      conn.execute("update user set {0} = '{1}' where id = '{2}'".format(patchColumn, valueColumn, userId))
      query = conn.execute("select id, userName, userbio, useremail, userrankpoints from user where id=%d " % int(userId))
      result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      return jsonify(result)      
      
  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['id']
    userName = request.json['userName']
    userEmail = request.json['userEmail']
    userPassword = request["userPassword"]
    hashedPass = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())
    userBio = request.json['userBio']
    userRankPoints = request.json['userRankPoints']

    conn.execute("update user set username ='" + str(userName) + "', useremail ='" + str(userEmail) + "', userpassword='" + hashedPass.decode("utf8") + "', userbio= '" + str(userBio) + "', userrankPoints= " + str(userRankPoints) + " where id =%d " % int(id))
    query = conn.execute("select id, userName, userbio, useremail, userrankpoints from user where id=%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class SocialNetwork(Resource):
    
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from socialNetwork order by id desc")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        socialName = request.json['socialName']
        userId = request.json['userId']
        conn.execute("insert into socialNetwork values(null, '{0}','{1}')".format(socialName, userId))
        query = conn.execute('select * from socialNetwork')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class Category(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from category order by id desc")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
        
    def post(self):
        conn = db_connect.connect()
        categoryRule = request.json['categoryRule']
        categoryName = request.json['categoryName'] # Posso deixar independente do front.
        userId = request.json['userId']
        conn.execute("insert into category values(null, '{0}','{1}','{2}')".format(categoryRule, categoryName, userId))
        query = conn.execute('select * from category')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class Material(Resource):

  def get(self):
    conn = db_connect.connect()
    query = conn.execute("select * from material")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    materialContent = MaterialContentById()
    for x in result:
        x["materialContentList"] = materialContent.get(x["id"])
    return jsonify(result)

  def post(self):
    conn = db_connect.connect()
    materialTitle = request.json['materialTitle']
    materialVideoUrl = request.json['materialVideoUrl']
    materialIdealFor = request.json['materialIdealFor']
    materialDetailedInformation = request.json['materialDetailedInformation']
    materialShortInformation = request.json['materialShortInformation']

    conn.execute("insert into material values(null, '{0}','{1}', '{2}', '{3}', '{4}')".format(materialTitle, materialVideoUrl, materialIdealFor, materialDetailedInformation, materialShortInformation))

    query = conn.execute('select * from material order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def patch(self): # Patch para atualizar determinado atributo passado pelo request.
      conn = db_connect.connect()
      materialId = request.json['materialId']
      patchColumn = request.json['patchColumn']
      valueColumn = request.json['valueColumn']
      conn.execute("update material set {0} = '{1}' where id = '{2}'".format(patchColumn, valueColumn, materialId))
      query = conn.execute('select * from material where id = {0}'.format(materialId))
      result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      return jsonify(result)

  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    materialId = request.json['materialId']
    materialTitle = request.json['materialTitle']
    materialVideoUrl = request.json['materialVideoUrl']
    materialIdealFor = request.json['materialIdealFor']
    materialDetailedInformation = request.json['materialDetailedInformation']
    materialShortInformation = request.json['materialShortInformation']

    conn.execute("update material set materialtitle ='" + str(materialTitle) +
"', materialVideoUrl ='" + str(materialVideoUrl) + "', materialIdealFor='" + str(materialIdealFor) + "', materialDetailedInformation='" + str(materialDetailedInformation) + "', materialShortInformation='" + str(materialShortInformation) + "'  where id =%d " % int(materialId))

    query = conn.execute("select * from material where id=%d " % int(materialId))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class MaterialContent(Resource):
    
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from materialContentList")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
        
    def post(self):
        conn = db_connect.connect()
        materialContent = request.json['materialContent']
        conn.execute("insert into materialContentList values(null, '{0}')".format(materialContent))
        query = conn.execute('select * from materialContentList order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self): # Patch para atualizar determinado atributo passado pelo request.
        conn = db_connect.connect()
        materialContentId = request.json['materialContentId']
        materialContent = request.json['materialContent']
        conn.execute("update materialContentList set materialContent = '{0}' where id = '{1}'".format(materialContent, str(materialContentId)))
        query = conn.execute('select * from materialContentList where id = {0}'.format(str(materialContentId)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class Challenges(Resource):

  def get(self):
    conn = db_connect.connect()
    query = conn.execute("select * from challenge")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def post(self):
    conn = db_connect.connect()
    challengeTitle = request.json['challengeTitle']
    challengeBio = request.json['challengeBio']
    challengeRequirements = request.json['challengeRequirements']
    challengeDeadline = request.json['challengeDeadline']
    challengeImageURL = request.json['challengeImageURL']
    challengePoints = request.json['challengePoints']

    conn.execute("insert into challenge values(null, '{0}','{1}', '{2}', '{3}', '{4}', '{5}')".format(challengeTitle, challengeBio, challengeRequirements, challengeDeadline, challengeImageURL, challengePoints))

    query = conn.execute('select * from challenge order by id desc limit 1')
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def patch(self): # Patch para atualizar determinado atributo passado pelo request.

      conn = db_connect.connect()
      challengeId = request.json['challengeId']
      patchColumn = request.json['patchColumn']
      valueColumn = request.json['valueColumn']
      conn.execute("update challenge set {0} = '{1}' where id = '{2}'".format(patchColumn, valueColumn, challengeId))
      query = conn.execute('select * from challenge where id = {0}'.format(challengeId))
      result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      return jsonify(result)
  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    challengeId = request.json['challengeId']
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
                 "'  where id =%d " % int(challengeId))

    query = conn.execute("select * from challenge where id=%d " % int(challengeId))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class ChallengeResponse(Resource):

  def get(self):
    conn = db_connect.connect()
    query = conn.execute("select * from challengeResponse")
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

  def post(self):
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

  def patch(self): # Patch para atualizar determinado atributo passado pelo request.

      conn = db_connect.connect()
      challengeResponseId = request.json['challengeResponseId']
      patchColumn = request.json['patchColumn']
      valueColumn = request.json['valueColumn']
      conn.execute("update challengeResponse set {0} = '{1}' where id = '{2}'".format(patchColumn, valueColumn, challengeResponseId))
      query = conn.execute('select * from challengeresponse where id = {0}'.format(challengeResponseId))
      result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
      return jsonify(result)
    
  def put(self):  # Update*(atualizar) no BD de um usuário passado como parâmetro
    conn = db_connect.connect()
    id = request.json['challengeResponseId']
    challengeLinkResponse = request.json['challengeLinkResponse']
    userId = request.json['userId']
    challengeId = request.json['challengeId']

    conn.execute("update challengeResponse set challengeId ='" + str(challengeId) + "', userId ='" + str(userId) + "', challengeLinkResponse='" + str(challengeLinkResponse) + "' where id =%d " % int(id))

    query = conn.execute("select * from challengeResponse where id=%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return jsonify(result)

class UserById(Resource): 
  def delete(self, id): # Deleta no BD um usuário passado como parâmetro
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

class ChallengesById(Resource): 
  def delete(self, id):
    conn = db_connect.connect()
    conn.execute("delete from challenge where id=%d " % int(id))
    return {"status": "success"}

  def get(self, id):
    conn = db_connect.connect()
    query = conn.execute("select * from challenge where id =%d " % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result

class MaterialContentById(Resource): 
  def get(self, id):
    conn = db_connect.connect()
    query = conn.execute('select * from materialContentList where id = "%d"' % int(id))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result
      
class ChallengeContentByUserId(Resource): 
  def get(self, userId):
    conn = db_connect.connect()
    query = conn.execute('select * from challengeResponse where userid = "%d"' % int(userId))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    listChallenges = []
    for x in result:
      queryC = conn.execute('select challengeTitle from challenge where id = "%d"' % int(x["challengeId"]))
      resultC = [dict(zip(tuple(queryC.keys()), i)) for i in queryC.cursor]
      listChallenges.append(resultC[0]["challengeTitle"])
    return listChallenges

class CategoryByUserId(Resource): 

  def get(self, userId):
    conn = db_connect.connect()
    query = conn.execute("select categoryRule from category where userId =%d " % int(userId))
    result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
    return result

class SocialByUserId(Resource): 

  def get(self, userId):
    conn = db_connect.connect()
    query = conn.execute("select socialName from socialNetwork where userId =%d " % int(userId))
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

api.add_resource(SocialNetwork, '/socialnetwork')
api.add_resource(SocialByUserId, '/socialnetwork/<userId>')

api.add_resource(Category, '/category')
api.add_resource(CategoryByUserId, '/category/<userId>')

api.add_resource(Material, '/material')
api.add_resource(MaterialContent, '/materialcontent')
api.add_resource(MaterialById, '/material/<id>')
api.add_resource(MaterialContentById, '/materialcontent/<id>')

api.add_resource(Challenges, '/challenges')
api.add_resource(ChallengesById, '/challenges/<id>')
api.add_resource(ChallengeResponse, '/challengesresponse')
api.add_resource(ChallengeContentByUserId, '/challengesresponse/<userId>')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)