from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, get_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'troque-esta-chave-em-producao'

@app.before_request
def setup():
    init_db()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'admin' in session:
        return redirect(url_for('agendamentos'))
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('agendamentos'))
        flash('Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/sair')
def sair():
    session.clear()
    return redirect(url_for('login'))

# ── Agendamentos ──────────────────────────────────────────────────────────────

@app.route('/agendamentos')
@login_required
def agendamentos():
    db = get_db()
    hoje = datetime.today().strftime('%Y-%m-%d')
    data = request.args.get('data', hoje)
    registros = db.execute('''
        SELECT a.id, c.nome AS cliente, s.nome AS servico, a.data, a.hora, a.observacao
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN servicos s ON a.servico_id = s.id
        WHERE a.data = ?
        ORDER BY a.hora
    ''', (data,)).fetchall()
    return render_template('agendamentos.html', registros=registros, data=data)

@app.route('/agendamentos/novo', methods=['GET', 'POST'])
@login_required
def novo_agendamento():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            'INSERT INTO agendamentos (cliente_id, servico_id, data, hora, observacao) VALUES (?,?,?,?,?)',
            (request.form['cliente_id'], request.form['servico_id'],
             request.form['data'], request.form['hora'], request.form.get('observacao', ''))
        )
        db.commit()
        flash('Agendamento criado com sucesso!')
        return redirect(url_for('agendamentos', data=request.form['data']))
    clientes = db.execute('SELECT * FROM clientes ORDER BY nome').fetchall()
    servicos = db.execute('SELECT * FROM servicos ORDER BY nome').fetchall()
    return render_template('form_agendamento.html', clientes=clientes, servicos=servicos)

@app.route('/agendamentos/excluir/<int:id>')
@login_required
def excluir_agendamento(id):
    db = get_db()
    ag = db.execute('SELECT data FROM agendamentos WHERE id=?', (id,)).fetchone()
    db.execute('DELETE FROM agendamentos WHERE id=?', (id,))
    db.commit()
    flash('Agendamento removido.')
    return redirect(url_for('agendamentos', data=ag['data'] if ag else ''))

# ── Clientes ──────────────────────────────────────────────────────────────────

@app.route('/clientes')
@login_required
def clientes():
    db = get_db()
    lista = db.execute('SELECT * FROM clientes ORDER BY nome').fetchall()
    return render_template('clientes.html', clientes=lista)

@app.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def novo_cliente():
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO clientes (nome, telefone) VALUES (?,?)',
                   (request.form['nome'], request.form['telefone']))
        db.commit()
        flash('Cliente cadastrado!')
        return redirect(url_for('clientes'))
    return render_template('form_cliente.html', cliente=None)

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    db = get_db()
    cliente = db.execute('SELECT * FROM clientes WHERE id=?', (id,)).fetchone()
    if request.method == 'POST':
        db.execute('UPDATE clientes SET nome=?, telefone=? WHERE id=?',
                   (request.form['nome'], request.form['telefone'], id))
        db.commit()
        flash('Cliente atualizado!')
        return redirect(url_for('clientes'))
    return render_template('form_cliente.html', cliente=cliente)

@app.route('/clientes/excluir/<int:id>')
@login_required
def excluir_cliente(id):
    db = get_db()
    db.execute('DELETE FROM clientes WHERE id=?', (id,))
    db.commit()
    flash('Cliente removido.')
    return redirect(url_for('clientes'))

# ── Serviços ──────────────────────────────────────────────────────────────────

@app.route('/servicos')
@login_required
def servicos():
    db = get_db()
    lista = db.execute('SELECT * FROM servicos ORDER BY nome').fetchall()
    return render_template('servicos.html', servicos=lista)

@app.route('/servicos/novo', methods=['GET', 'POST'])
@login_required
def novo_servico():
    db = get_db()
    if request.method == 'POST':
        db.execute('INSERT INTO servicos (nome, duracao_min, preco) VALUES (?,?,?)',
                   (request.form['nome'], request.form['duracao_min'], request.form['preco']))
        db.commit()
        flash('Serviço cadastrado!')
        return redirect(url_for('servicos'))
    return render_template('form_servico.html', servico=None)

@app.route('/servicos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_servico(id):
    db = get_db()
    servico = db.execute('SELECT * FROM servicos WHERE id=?', (id,)).fetchone()
    if request.method == 'POST':
        db.execute('UPDATE servicos SET nome=?, duracao_min=?, preco=? WHERE id=?',
                   (request.form['nome'], request.form['duracao_min'], request.form['preco'], id))
        db.commit()
        flash('Serviço atualizado!')
        return redirect(url_for('servicos'))
    return render_template('form_servico.html', servico=servico)

@app.route('/servicos/excluir/<int:id>')
@login_required
def excluir_servico(id):
    db = get_db()
    db.execute('DELETE FROM servicos WHERE id=?', (id,))
    db.commit()
    flash('Serviço removido.')
    return redirect(url_for('servicos'))

if __name__ == '__main__':
    app.run(debug=True)
