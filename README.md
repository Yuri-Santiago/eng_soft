# API Academica com Flask, SQLite e Swagger

Este é um projeto simples de uma API REST para gerenciar um sistema academico, construída com **Flask**, **SQLite** e documentação interativa usando **Swagger (Flasgger)**.

---

## Requisitos

- Python 3.12+

---

## Instalação

1. Clone o repositório:

```
git clone https://github.com/Yuri-Santiago/eng_soft.git
cd eng_soft
```


2. Crie um ambiente virtual:
```
python -m venv .venv
. .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

## Como rodar a aplicação:
Execute o servidor Flask:
```
python app.py
```
A aplicação estará disponível em:
http://localhost:5000

A documentação interativa Swagger está disponível em:
http://localhost:5000/apidocs/

## Testes automatizados
Para rodar os testes unitários:
```
pytest test_api_pytest.py -v
```
