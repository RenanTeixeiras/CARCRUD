from flask import Flask, render_template, request, flash
from create_databases import (salvar_carro, consultar_carros, salvar_despesa,
    criar_tabelas, gerar_total_gasto_veiculo)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string' 

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/compra", methods=['GET','POST'])
def compra():
    if request.method == 'POST':
        if salvar_carro(
                placa = request.form['placa'],
                marca = request.form['marca'],
                ano = request.form['ano'],
                modelo = request.form['modelo'],
                status = request.form['status'],
                valor_compra= request.form['valor_de_compra']
            ) == 'CAMPO VAZIO':
            flash('Nenhum campo pode estar vazio!')
            return render_template('compra.html')
        else:
            salvar_carro( 
                placa = request.form['placa'],
                marca = request.form['marca'],
                ano = request.form['ano'],
                modelo = request.form['modelo'],
                status = request.form['status'],
                valor_compra= request.form['valor_de_compra']
                )
            return render_template('compra.html')
    else:
        return render_template('compra.html')

@app.route("/despesa", methods=['GET', 'POST'])
def despesa():
    carros = consultar_carros()
    if request.method=='POST':
        salvar_despesa(
            id_veiculo=request.form['Carros'],
            titulo=request.form['despesa'],
            valor_gasto=request.form['valor_gasto'],
            descricao=request.form['descricao']
            )
        return render_template('add_despesa.html', carros = carros)
    else:  
        return render_template('add_despesa.html', carros = carros)

@app.route("/venda", methods=['GET','POST'])
def venda():
    carros = consultar_carros()
    if request.method=='POST':
        return render_template('venda.html',carros=carros)
    else:
        return render_template('venda.html',carros=carros)

@app.route("/resumo/<id>", methods=['GET','POST'])
def resumo(id):
    gastos = gerar_total_gasto_veiculo(id)
    total_despesas = 0
    valor_compra = gastos[0][5]
    for gasto in gastos:
        total_despesas += gasto[1]
    return render_template("resumo.html", gastos=gastos, total_despesas = total_despesas, valor_compra = valor_compra)


if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)