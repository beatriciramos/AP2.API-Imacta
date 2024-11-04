from flask import Blueprint, jsonify, request
from config import db
from models.professores_model import Professor

professor_bp = Blueprint('professor', __name__, url_prefix='/professores')

@professor_bp.route('', methods=['POST'])
def add_professor():
    data = request.json
    if 'nome' not in data or 'idade' not in data or 'materia' not in data:
        return jsonify({'error': 'Campos obrigatórios: nome, idade, materia.'}), 400

    novo_professor = Professor(
        nome=data['nome'],
        idade=data['idade'],
        materia=data['materia'],
        observacoes=data.get('observacoes', '')
    )

    db.session.add(novo_professor)
    db.session.commit()

    return jsonify({'id': novo_professor.id}), 201

@professor_bp.route('', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([{
        'id': professor.id,
        'nome': professor.nome,
        'idade': professor.idade,
        'materia': professor.materia,
        'observacoes': professor.observacoes
    } for professor in professores]), 200

@professor_bp.route('/<int:professor_id>', methods=['GET'])
def get_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({'error': 'Professor não encontrado.'}), 404

    return jsonify({
        'id': professor.id,
        'nome': professor.nome,
        'idade': professor.idade,
        'materia': professor.materia,
        'observacoes': professor.observacoes
    }), 200

@professor_bp.route('/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    data = request.json
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({'error': 'Professor não encontrado.'}), 404

    professor.nome = data.get('nome', professor.nome)
    professor.idade = data.get('idade', professor.idade)
    professor.materia = data.get('materia', professor.materia)
    professor.observacoes = data.get('observacoes', professor.observacoes)

    db.session.commit()

    return jsonify({'message': 'Professor atualizado com sucesso.'}), 200

@professor_bp.route('/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({'error': 'Professor não encontrado.'}), 404

    db.session.delete(professor)
    db.session.commit()

    return jsonify({'message': 'Professor removido com sucesso.'}), 200
