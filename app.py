
from flask import Flask
from config import db
from controllers.alunos_controller import aluno_bp
from controllers.turmas_controller import turma_bp
from controllers.professores_controller import professor_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SECRET_KEY'] = 'chave-secreta'
db.init_app(app)

# Registrar os blueprints
app.register_blueprint(aluno_bp)
app.register_blueprint(turma_bp)
app.register_blueprint(professor_bp)

# Inicializar banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
