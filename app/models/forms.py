#from flask_wtf import Form
from flask_wtf import FlaskForm as FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField(label=('Submit'))
    name = ""

class Aviso(FlaskForm):
    msg = TextAreaField("aviso", validators=[DataRequired()])
    n_loja = StringField("loja", validators=[DataRequired()])
    opcoes_envio = SelectField('Opções de envio', choices=[
    ('todas', 'Todas as lojas'),
    ('especifica', 'Loja específica')
    ])
    submit = SubmitField('Enviar')
    
class ProfileEdit(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    mail = StringField("mail", validators=[DataRequired()])
    submit = SubmitField('Salvar')
    
 
class PassEdit(FlaskForm):
    old_password = PasswordField("old_password", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    new_password = PasswordField("new_password", validators=[DataRequired()]) 
    submit = SubmitField('Salvar')