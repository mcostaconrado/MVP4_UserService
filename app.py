from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session
#from model.Registro import Registro
from model.User import User
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="PUC Trading Bank - User service", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentation", description="Documentation of User service")
routes_tag = Tag(name="Routes", description="Implemented routes for User service")

@app.get('/', tags=[home_tag])
def home():
    """Redirects to the Swagger documentation of User Service
    """
    return redirect('/openapi/swagger')

@app.post('/user', tags=[routes_tag],
          responses={"200": UserViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Insert a new user to the database
    Returns a representation of the new inserted user
    """        
    user = User(
        first_name=form.first_name,
        last_name=form.last_name,
        document=form.document
        )
    
    full_name = user.get_full_name()
    print(f"Registrating {full_name}")
    
    try:
        session = Session()
        session.add(user)

        session.commit()
        logger.debug(f"Adding user '{full_name}'")
        return reprUser(user), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Error regis]"
        error_msg = e
        # logger.warning(e)
        # logger.warning(f"Erro ao adicionar registro '{registro.titulo}' do dia '{registro.data_registro}, {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/user', tags=[routes_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserSearchSchema):
    """ Search for a user id in the database
    Returns information about the user
    """
    id = query.id     
    
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    
    user = session.query(User).filter(User.id == id).first()
    
    if not user:
        # se o registro não foi encontrado
        error_msg = "There is no user with this id registered in the database "
        logger.warning(f"Error getting a username with document {id}, {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Registro encontrado!")
        # retorna a representação de registro
        return reprUser(user), 200
    
@app.put('/user', tags=[routes_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def put_balance(query: UserSumBalanceSchema):
    """Modifies a user's balance
    Returns the updated information about the user
    """
    id = query.id
    delta = query.delta  
    
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    
    user = session.query(User).filter(User.id == id).first()
    
    if not user:
        # se o registro não foi encontrado
        error_msg = "There is no user with this id registered in the database "
        logger.warning(f"Error getting a username with id #{id}, {error_msg}")
        return {"message": error_msg}, 404
    else:
        current_balance = user.get_balance()
        session.query(User).filter(User.id == id).update({'balance': round(current_balance + delta, 2)})
        session.commit()

        logger.debug(f"Registro encontrado!")
        # retorna a representação de registro
        return reprUser(user), 200

@app.delete('/user', tags=[routes_tag],
            responses={"200": UserSchema, "404": ErrorSchema})
def delete_user(query: UserSearchSchema):
    """Deletes a user entry
    Returns a confirmation message
    """
    print(query)
    id = query.id
    
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(User).filter(User.id == id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        message = f"User id #{id} was successfully removed from data base"
        logger.debug(message)

        return {"mesage": message}, 200
    else:
        # se o registro não foi encontrado
        error_msg = "User not found"
        logger.warning(f"Exception was thrown when trying to delete user id #'{id}', {error_msg}")
        return {"mesage": error_msg}, 404