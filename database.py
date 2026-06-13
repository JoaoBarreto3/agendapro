import sqlite3
from flask import g

DATABASE = 'agendamento.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.executescript('''
        CREATE TABLE IF NOT EXISTS clientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome     TEXT NOT NULL,
            telefone TEXT
        );
        CREATE TABLE IF NOT EXISTS servicos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nome         TEXT NOT NULL,
            duracao_min  INTEGER DEFAULT 30,
            preco        REAL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS agendamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id  INTEGER NOT NULL REFERENCES clientes(id),
            servico_id  INTEGER NOT NULL REFERENCES servicos(id),
            data        TEXT NOT NULL,
            hora        TEXT NOT NULL,
            observacao  TEXT DEFAULT ''
        );
    ''')
    # Dados de exemplo
    if db.execute('SELECT COUNT(*) FROM clientes').fetchone()[0] == 0:
        db.executescript('''
            INSERT INTO clientes (nome, telefone) VALUES
                ('João Silva', '(12) 99999-1111'),
                ('Maria Souza', '(12) 98888-2222'),
                ('Pedro Lima', '(12) 97777-3333');
            INSERT INTO servicos (nome, duracao_min, preco) VALUES
                ('Corte', 30, 35.00),
                ('Barba', 20, 25.00),
                ('Corte + Barba', 50, 55.00),
                ('Hidratação', 40, 45.00);
        ''')
    db.commit()
    db.close()
