from flask import Blueprint, jsonify, request
from config import db
from models.alunos_model import Aluno

aluno_bp = Blueprint('aluno', __name__, url_prefix='/alunos')


@aluno_bp.route('', methods=['POST'])
def add_aluno():
    data = request.json
    required_fields = ['nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}.'}), 400

    
    media_final = (data['nota_primeiro_semestre'] + data['nota_segundo_semestre']) / 2

    
    novo_aluno = Aluno(
        nome=data['nome'],
        idade=data['idade'],
        turma_id=data['turma_id'],
        data_nascimento=data['data_nascimento'],
        nota_primeiro_semestre=data['nota_primeiro_semestre'],
        nota_segundo_semestre=data['nota_segundo_semestre']
    )
    novo_aluno.media_final = media_final

    
    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({'id': novo_aluno.id}), 201



@aluno_bp.route('/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.json

    
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado.'}), 404

    
    aluno.nome = data.get('nome', aluno.nome)
    aluno.idade = data.get('idade', aluno.idade)
    aluno.turma_id = data.get('turma_id', aluno.turma_id)
    aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)

    
    nota_primeiro = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    nota_segundo = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    aluno.nota_primeiro_semestre = nota_primeiro
    aluno.nota_segundo_semestre = nota_segundo
    aluno.media_final = (nota_primeiro + nota_segundo) / 2

    
    db.session.commit()

    return jsonify({'message': 'Aluno atualizado com sucesso.'}), 200
