from flask import render_template, flash, redirect, url_for, Response, request, jsonify, send_from_directory
from flask_login import login_user, logout_user, UserMixin, login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app import app, db, login_manager
from app.models.tables import User
from app.models.forms import LoginForm, Aviso, ProfileEdit, PassEdit
import os.path
from datetime import datetime
import time
import pyodbc
from app import app, socketio
import threading
from datetime import datetime, timedelta
import requests
import re
import os
from flask_socketio import SocketIO, emit

    
@socketio.on('connect')
def connect_handler():
    if current_user.is_authenticated:
        current_user.is_online = True
        db.session.commit()

        # Emite um sinal para o cliente informando que está online
        emit('user_status', {'user_id': current_user.id, 'is_online': True})

@socketio.on('disconnect')
def test_disconnect():
    if current_user.is_authenticated:
        current_user.is_online = False
        db.session.commit()

        # Emite um sinal para o cliente informando que está offline
        emit('user_status', {'user_id': current_user.id, 'is_online': False})

@socketio.on('check_user_status')
def check_user_status(data):
   if current_user.is_authenticated:
    # Retorna o status online/offline diretamente da coluna is_online do usuário
    is_online = current_user.is_online
    emit('user_status', {'user_id': current_user.id, 'is_online': is_online})

@socketio.on('get_all_users')
def get_all_users():
  if current_user.is_authenticated:
    # Consulta todos os usuários no banco de dados
    users = User.query.all()

    # Cria uma lista de dicionários contendo informações de cada usuário
    users_info = [{'user_id': user.id, 'username': user.username, 'is_online': user.is_online} for user in users]

    # Emite a lista de usuários e seus estados online/offline para o cliente
    emit('all_users_status', {'users': users_info})

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/index', methods = ["GET", "POST"])
@app.route('/')
def index():  # put application's code here
    if current_user.is_authenticated:
       img_user = recupera_imagem(current_user.id, current_user.username)
       return render_template('index.html', img_user=img_user)
    else:  
      return redirect(url_for('login'))

   
@app.route('/login', methods = ["GET", "POST"])
def login():  # put application's code here
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():

       u = User.query.filter_by(username=form.username.data).first()
       if u:
       
        if u and u.password == form.password.data:
           login_user(u)
           name = u.name
           pic_profile = recupera_imagem(u.id, u.username)
           return redirect(url_for('index', pic_profile=pic_profile))
           
        elif check_password_hash(u.password, form.password.data):
           login_user(u)
           return redirect(url_for('index'))
           
        else:
          flash("Usuario ou senha incorretos!")
       else:
           flash("Usuario Incorreto ou não existe!")    
           
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Deslogado")
    return redirect(url_for("login"))

@app.route('/dashboard', methods=["POST","GET"])
@login_required
def dashboard():  # put application's code here
    
    return render_template('dashboard.html')

@app.route('/robots', methods=["POST","GET"])
@login_required
def robots():  # put application's code here
    
    return render_template('board.html')

@app.route('/monitors', methods=["POST","GET"])
@login_required
def monitors():  # put application's code here
    
    return render_template('login.html')

@app.route('/apps', methods=["POST","GET"])
@login_required
def apps():  # put application's code here
    
    return render_template('board.html')

@app.route('/aviso', methods=["POST", "GET"])
@login_required
def aviso():
    form = Aviso()
    msg = form.msg.data
    n_loja = form.n_loja.data
    opcoes_envio = form.opcoes_envio.data
        
    return render_template('aviso.html', form=form)

@app.route('/queue', methods=["POST", "GET"])
@login_required
def queue():
    form = Aviso()
    msg = form.msg.data
    client_ip = '192.168.100.199'
    n_loja = request.form['filial']
    opcoes_envio = request.form['opcoes_envio_hidden']
    local_user = request.form['local_user']
    
    if opcoes_envio not in ["todas", "especifica"]:
        #send = {'opcoes_envio': False}
        send = {'return': False, 'text': ' Selecionar uma opção de envio!'}
        print("erro")
        return jsonify(send)
    
    elif len(msg) <= 30:
        send = {'return': False, 'text': 'Aviso deve conter mais que 20 caracteres!'}
        return jsonify(send)
        
    else:
        if opcoes_envio == "todas":
            print("todas")
            send_aviso(msg, opcoes_envio, n_loja, client_ip)
            send = {'return': True, 'text': 'Alerta para todas as lojas foi enviado com sucesso!'}
            return jsonify(send)  

        elif opcoes_envio == "especifica":
            print("especifica")
            send_aviso(msg, opcoes_envio, n_loja, client_ip)
            send = {'return': True, 'text': f'Alerta para loja {n_loja} foi enviado com sucesso!'}
            return jsonify(send)

    return render_template("index.html")

@app.route('/panel', methods=["POST","GET"])
@login_required
def panel():  # put application's code here
    form = Aviso()
    return render_template('aviso.html', form=form)

@login_required
def users_logged_in():
    users = list(logged_in_users.values())
    return users
    
@app.route('/team', methods=["POST","GET"])
@login_required
def team():  
    users = users_logged_in()   
    list_users = User.query.all() 
    return render_template('team.html', users=users, list_users=list_users)
 
 
@app.route('/perfil', methods=["POST", "GET"])
@login_required
def perfil():
    form_profile = ProfileEdit()
    form_pass = PassEdit()  
    img_user = recupera_imagem(current_user.id, current_user.username)
    if form_profile.validate_on_submit(): 
       print("True profile")
       
    elif form_pass.validate_on_submit():
         print("True pass")    
         
    return render_template('perfil.html', form=form_pass, form1=form_profile, img_user=img_user)
    
  
    
@app.route('/v_profile', methods=["POST", "GET"])
@login_required
def v_profile():      
    form1 = ProfileEdit()  
    username = form1.username.data
    mail = form1.mail.data
    name = form1.name.data
    user = User.query.filter_by(username=current_user.username).first()
    list_users = User.query.all()
     
    alter = 0
    if form1.validate_on_submit(): 
       padrao = r'^[\w\-.]+@[a-zA-Z\d\-.]+\.[a-zA-Z]{2,}$'        
               
       if user.email != mail and not re.match(padrao, mail):
          alter = 1
          send = {'return': False, 'text': f'E-mail invalido!'}
          return jsonify(send)
       
       if user.email != mail and re.match(padrao, mail):
          alter = 1       
          user.email = mail
          db.session.commit()
        
       if username != user.username and username in list_users:
          alter = 1
          send = {'return': True, 'text': f'Usuario já existe!'}
          return jsonify(send)
          
       if username != user.username and user.username not in list_users:
           alter = 1
           user.username = username
           db.session.commit()
             
       if name != user.name:
            user.name = name
            db.session.commit()
            alter = 1             
              
       if alter == 0:
          send = {'return': False, 'text': f'Você não alterou nenhum dado!'}
          return jsonify(send) 
              
       if alter == 1:
          send = {'return': True, 'text': f'Dados foram salvos com sucesso!'}
          return jsonify(send)  
          
       send = {'return': False, 'text': f'Erro desconhecido, contate o Mike!'}
       return jsonify(send)  
       
    else:
       send = {'return': False, 'text': f'Necessario preencher todos os campos para salvar!'}
       return jsonify(send)     
    
    
@app.route('/uploads', methods=["POST"])
@login_required
def uploads():
    if request.method == "POST":
        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']

            if arquivo.filename != '' and arquivo.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                upload_path = app.config['UPLOAD_PATH']   
                timestamp = time.time()
                
                deleta_arquivo(current_user.id, current_user.username)
                
                arquivo.save(f'{upload_path}/{current_user.username}-{timestamp}.jpg')
                # Lógica adicional para processar o upload bem-sucedido, se necessário

                send = {'return': True, 'text': 'Imagem e perfil atualizados!'}
                return jsonify(send)

            else:
                # Lógica para lidar com nenhum arquivo selecionado ou formato inválido
                send = {'return': False, 'text': 'Erro: Nenhum arquivo selecionado ou formato inválido!'}
                return jsonify(send)

        else:
            # Lógica para lidar com o envio sem arquivo
            send = {'return': False, 'text': 'Erro: Nenhum arquivo enviado!'}
            return jsonify(send)

@app.route('/imagem/<nome_arquivo>')
def imagem(nome_arquivo):
    meu_diretorio = app.config['UPLOAD_PATH']
    return send_from_directory(meu_diretorio, nome_arquivo)

def recupera_imagem(id, user):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'{user}' in nome_arquivo:
            return nome_arquivo

    return 'avatar1.png'

def deleta_arquivo(id, user):
    id = id
    user = user
    arquivo = recupera_imagem(id, user)
    if arquivo != "avatar1.png":
        caminho_completo = os.path.join(app.config['UPLOAD_PATH'], arquivo)
        os.remove(caminho_completo)
 
                
@app.route('/v_pass', methods=["POST", "GET"])
@login_required
def v_pass():      
    
    form = PassEdit()  
    old_password = form.old_password.data
    password = form.password.data
    new_password = form.new_password.data
    
    user = User.query.filter_by(username=current_user.username).first()
    
    if form.validate_on_submit(): 
      if password == new_password:
         if old_password == user.password:
           if len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password) and re.search(r"[.!@#$%^&*()-+=]", password):
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            db.session.commit()
            send = {'return': True, 'text': f'Nova Senha foi salva com sucesso!'}
            return jsonify(send)
            
           else:
              send = {'return': False, 'text': f'Senha deve conter(numero,simbolo,letra maiuscula,minimo 8 caracteres)'}
              return jsonify(send)
            
         elif check_password_hash(user.password, old_password):
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            db.session.commit()
            send = {'return': True, 'text': f'Nova Senha foi salva com sucesso!'}
            return jsonify(send)
         
         else:
            send = {'return': False, 'text': f'Senha atual incorreta!'}
            return jsonify(send)     
      else:
        send = {'return': False, 'text': f'Verifique o campo de confirmação de senha'}
        return jsonify(send)         
    else:
       send = {'return': False, 'text': f'Dados incorretos!'}
       return jsonify(send)    

    # Verifique se a senha atual fornecida corresponde à senha no banco de dados
    if check_password_hash(user.password, current_password):
        # Gere o hash da nova senha
        hashed_password = generate_password_hash(new_password)

        # Atualize a senha no banco de dados
        user.password = hashed_password
        db.session.commit()
    
    
@app.route('/manager_users', methods=["POST", "GET"])
@login_required
def manager_users():
    list_users = User.query.all() 
    return render_template('crud_users.html', list_users=list_users)
    

@app.route('/replicate', methods=["POST", "GET"])
@login_required
def replicate():   
    send = {'return': True, 'text': f'Exec foi executada!'}
    os.remove(rf"C:\sync_pdv\sync_seller.txt")
    return jsonify(send)
    

def send_aviso(aviso_txt, alert_check, filial, client_ip):
     
    print(f"cliente conectado {client_ip}")
    # Corrigir o acesso correto ao dicionário session_datas
    user = '777'
    timeout = '60'
    aviso_txt = aviso_txt
    alert_check = alert_check
    link_text = 'False'
    link = 'http://192.168.100.199/'
    filial = filial
    horas = datetime.now()
    dats = str(horas.strftime("%d/%m/%Y %H:%M:%S")) 
              
                           
    if aviso_txt:
       server = '192.168.100.199'
       database = 'PREVERSION'
       username = 'SA'
       password = 'ruqaBAvU7?g6!T'

       connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

       try:
           conn = pyodbc.connect(connection_string)
           cursor = conn.cursor()

           cursor.execute("""SELECT TOP 1 * FROM queue
                      ORDER BY position DESC;""")

           row_q = cursor.fetchone()                 
           
           if row_q is None:
               
             hora_now = datetime.now()
             data_hora_1 = str(hora_now.strftime("%d/%m/%Y %H:%M:%S")) 
             
             cursor.execute(f""" INSERT INTO [dbo].[queue]
                 ([solicitante]
                 ,[data_hora]
                 ,[position]
                 ,[send]
                 ,[aviso]
                 ,[timeout]
                 ,[alert_check]
                 ,[link]
                 ,[link_text]
                 ,[filial])
               VALUES
                 ('{user}'
                 ,'{data_hora_1}'
                 ,'1'
                 ,'N'
                 ,'{aviso_txt}'
                 ,'{timeout}'
                 ,'{alert_check}'
                 ,'{link}'
                 ,'{link_text}'
                 ,'{filial}')""")
              
             cursor.commit()
             return jsonify({'message': f'Seu alerta foi enviado!', 'status': True})
             
           else:     
              solicitante = str(row_q[0])
              data_hora = str(row_q[1])
              position = int(row_q[2])
              send = str(row_q[3])           
              current_position = position + 1
              data_hora_1 = datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S")
              hora_atual_1 = datetime.now()
              diferenca_1 = hora_atual_1 - data_hora_1
             
              hora_now0 = datetime.now()
              data_hora_0 = str(hora_now0.strftime("%d/%m/%Y %H:%M:%S"))        
                       
                    
              
              #log_cmd = "Atenção: Seu aviso está na fila para envio, sua posição é " + str(current_position)
              lapse_t = str(diferenca_1)             
   
              cursor.execute(f""" INSERT INTO [dbo].[queue]
                 ([solicitante]
                 ,[data_hora]
                 ,[position]
                 ,[send]
                 ,[aviso]
                 ,[timeout]
                 ,[alert_check]
                 ,[link]
                 ,[link_text]
                 ,[filial])
               VALUES
                 ('{user}'
                 ,'{data_hora_0}'
                 ,'{current_position}'
                 ,'N'
                 ,'{aviso_txt}'
                 ,'{timeout}'
                 ,'{alert_check}'
                 ,'{link}'
                 ,'{link_text}'
                 ,'{filial}')""")
              
              cursor.commit()
              
              return jsonify({'message': f'Aviso na fila para envio, posição {str(current_position)}, tempo aproximado {lapse_t}', 'status': True})
           
             
       except (pyodbc.OperationalError, pyodbc.Error) as e:
              print("Erro ao acessar o serv8idor!")
              return jsonify({'message': f'Erro ao conectar com o servidor!', 'status': False})

       finally:              
           conn.close()
    else:
       return jsonify({'message': f'Acesso foi negado!', 'status': False})


def mars():   
    
    while True:
       print("Verificando novamente....")
       server = '192.168.100.199'
       database = 'PREVERSION'
       username = 'SA'
       password = 'ruqaBAvU7?g6!T'

       connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

       try:
           conn = pyodbc.connect(connection_string)
           cursor = conn.cursor()
           #cursor.execute("""SELECT TOP 1 *
           #FROM queue
           #ORDER BY data_hora DESC;""")           
           
           cursor.execute("""SELECT TOP 1 * FROM queue
           ORDER BY position ASC""")
         
           #cursor.execute("""select * from queue;""")
            
           row_w = cursor.fetchone()
           
           if row_w is not None:
              hour_v = row_w[1]
             # Resto do seu código aqui
              send_timeout = 2       
           
              hour_v = row_w[1]
              solicitante_o = row_w[0]
              position = int(row_w[2])
              aviso = row_w[4]
              timeout = row_w[5]
              alert_check = row_w[6]
              link = row_w[7]
              link_text = row_w[8]
              filial =  row_w[9]
                     
          
           if row_w:        
            
             cursor.close()
       
             data_hora = datetime.strptime(hour_v, "%d/%m/%Y %H:%M:%S")
             hora_atual = datetime.now()
             diferenca = hora_atual - data_hora
       
             # Obter a hora atual
             hora_now = datetime.now()

              # Formatar a hora atual no formato desejado
             hora_f = hora_now.strftime("%d/%m/%Y %H:%M:%S")
       
            # Verificar se passaranta pm 3 minutos
             alert_t_ok = False
             if diferenca >= timedelta(minutes=send_timeout) or 1==1:
                 conn = pyodbc.connect(connection_string)
                 cursor = conn.cursor()
                
                 try: 
                                
                   if alert_check == "especifica":
                      cursor.execute(f"""update Alertas_TI set alert_all = 'False', one_alert = '{filial}', filial = '{filial}',
                      alert_homolog = 'False', alert_pr = 'False', alert_sp = 'False', alert_sc = 'False'""")
                      
                   elif alert_check == "todas":
                      cursor.execute(f"""update Alertas_TI set alert_all = 'True', alert_pr = 'True', alert_sp = 'True', alert_sc = 'True',
                      one_alert = 'False', filial = 'None'""")                   
           
                   cursor.execute(f"""update Alertas_TI set mensagem = '{aviso}', data = '{hora_f}', timeout='{timeout}', link='{link}', link_text='{link_text}'""")
                   cursor.commit()               
                   cursor.close()
                  
                   conn = pyodbc.connect(connection_string)
                   cursor = conn.cursor()
                   cursor.execute(f"""select * FROM Alertas_TI""") 
                   val = cursor.fetchone()
                   msg_0 = str(val[0])
                   filial_0 = str(filial) 
                   cursor.close()
                 
                   if msg_0 == str(aviso) and filial_0 == str(filial):
                      conn = pyodbc.connect(connection_string)
                      cursor = conn.cursor()                  
                      cursor.execute(f"""DELETE from queue where position = '{position}'""")
                      cursor.commit()
                      cursor.close()   
                        
                      conn = pyodbc.connect(connection_string)
                      cursor = conn.cursor() 
                      cursor.execute("""SELECT TOP 1 * FROM queue
                      ORDER BY position DESC;""")
                      t1 = cursor.fetchone()
                      
                      if t1 is not None:                      
                         p1 = int(t1[2]) + 1 - 1               
                         cursor.execute(f"""update queue set position = '{p1}' where position = '{t1[2]}'""")
                         cursor.commit()               
                         cursor.close()
                      
                   else:
                     print("Algo deu errado no update!")
                   
                 except Exception as e:
                    print(f"Erro 1: {e}")                 
   
             else:
                print(f"mensagens em fila aguardar....{diferenca}")
           else:
              print("Nenhum aviso está em fila!")
              
       except(pyodbc.OperationalError, pyodbc.Error) as e:
              print("Erro ao acessar o serv8idor!")
          
       time.sleep(10)  
       
validate_queue = threading.Thread(target=mars)
validate_queue.start()      