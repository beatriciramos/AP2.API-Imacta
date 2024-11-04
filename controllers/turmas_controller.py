from flask import Blueprint, jsonify, request
from config import db
from models.turmas_model import Turma

turma_bp = Blueprint('turma', __name__, url_prefix='/turmas')

@turma_bp.route('', methods=['POST'])
def add_turma():
    data = request.json
    if 'descricao' not in data or 'professor_id' not in data:
        return jsonify({'error': 'Campos obrigatórios: descricao, professor_id.'}), 400

    nova_turma = Turma(
        descricao=data['descricao'],
        professor_id=data['professor_id'],
        ativo=data.get('ativo', True)
    )

    db.session.add(nova_turma)
    db.session.commit()

    return jsonify({'id': nova_turma.id}), 201

@turma_bp.route('', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([{
        'id': turma.id,
        'descricao': turma.descricao,
        'professor_id': turma.professor_id,
        'ativo': turma.ativo
    } for turma in turmas]), 200

@turma_bp.route('/<int:turma_id>', methods=['GET'])
def get_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada.'}), 404

    return jsonify({
        'id': turma.id,
        'descricao': turma.descricao,
        'professor_id': turma.professor_id,
        'ativo': turma.ativo
    }), 200

@turma_bp.route('/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    data = request.json
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada.'}), 404

    turma.descricao = data.get('descricao', turma.descricao)
    turma.professor_id = data.get('professor_id', turma.professor_id)
    turma.ativo = data.get('ativo', turma.ativo)

    db.session.commit()

    return jsonify({'message': 'Turma atualizada com sucesso.'}), 200

@turma_bp.route('/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada.'}), 404

    db.session.delete(turma)
    db.session.commit()

    return jsonify({'message': 'Turma removida com sucesso.'}), 200
