# AgendaPro 📅

Sistema de agendamento web para pequenos negócios (barbearias, clínicas, salões).

## Funcionalidades

- Login de administrador
- Agenda por dia com filtro de data
- Cadastro e gerenciamento de clientes
- Cadastro de serviços com duração e preço
- Criação e remoção de agendamentos

## Tecnologias

- **Python 3** + **Flask**
- **SQLite** (banco de dados local, sem instalação extra)
- **HTML/CSS** puro

## Como rodar

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/agendapro.git
cd agendapro

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode o servidor
python app.py
```

Acesse **http://localhost:5000**

**Login padrão:** usuário `admin` / senha `admin123`

## Estrutura do projeto

```
agendamento/
├── app.py            # Rotas e lógica principal
├── database.py       # Configuração e criação do banco
├── requirements.txt
├── static/
│   └── css/style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── agendamentos.html
    ├── form_agendamento.html
    ├── clientes.html
    ├── form_cliente.html
    ├── servicos.html
    └── form_servico.html
```

## Prints

> (adicione prints do sistema funcionando aqui)

## Autor

Feito por [seu nome] — [linkedin.com/in/seu-perfil]
