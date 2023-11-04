import sqlite3

con = sqlite3.connect('db/carcrud.db', check_same_thread=False)

def criar_tabelas():
    cursor = con.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
            VEICULO (
                id_veiculo integer primary key NOT NULL,
                placa text UNIQUE NOT NULL,
                marca text NOT NULL,  
                ano integer NOT NULL, 
                modelo text NOT NULL, 
                valor_de_compra real NOT NULL,
                status text
            )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
        DESPESAS (
                id_veiculo INTEGER NOT NULL,
                titulo text NOT NULL, 
                valor_gasto real NOT NULL, 
                descricao text NOT NULL,
                FOREIGN KEY(id_veiculo) REFERENCES VEICULO (id_veiculo)
                )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
        VENDA (
                id_veiculo integer NOT NULL, 
                valor_vendido real NOT NULL,
                nome_comprador text NOT NULL,
                FOREIGN KEY(id_veiculo) REFERENCES VEICULO (id_veiculo)
                )
    ''')


    con.commit()

def salvar_carro(placa, marca, ano, modelo, status, valor_compra, con=con):
    try:
        cursor = con.cursor()
        cursor.execute(f''' INSERT INTO VEICULO 
                                (placa, marca, ano, modelo, status, valor_de_compra)
                        VALUES
                                ('{placa}','{marca}','{ano}',
                                '{modelo}','{status}','{valor_compra}');

''')
    except sqlite3.IntegrityError:
        return 'CAMPO VAZIO'
    else:
        con.commit()

def salvar_despesa(id_veiculo, titulo, valor_gasto, descricao,con=con):
    cursor = con.cursor()
    cursor.execute(f''' INSERT INTO DESPESAS 
                                (id_veiculo, titulo, valor_gasto, descricao)
                        VALUES
                                ('{id_veiculo}','{titulo}','{valor_gasto}','{descricao}');

''')
    con.commit()

def vender_carro(id_veiculo, preco_vendido, nome_comprador, con=con):
    cursor = con.cursor()
    cursor.execute(f'''
            INSERT INTO VENDA (id_veiculo, preco_vendido, nome_comprador)
            VALUE ('{id_veiculo}','{preco_vendido}','{nome_comprador}')
    ''')
    con.commit()

def consultar_gasto_veiculo(con=con):
    cursor = con.cursor()
    return cursor.execute(f'''
            SELECT id_veiculo, sum(valor_gasto) FROM DESPESAS GROUP BY id_veiculo;
''').fetchall()

def gerar_total_gasto_veiculo(id_veiculo,con=con):
    cursor = con.cursor()
    gastos = cursor.execute(f'''
        SELECT 
                   d.id_veiculo, 
                   sum(d.valor_gasto),
                    d.titulo, 
                   v.placa, 
                   v.marca || " - " || v.modelo || " - " ||  v.ano,
                    v.valor_de_compra
                    FROM DESPESAS d INNER JOIN VEICULO v
                    WHERE v.id_veiculo = {id_veiculo}
''')
    return gastos.fetchall()


def consultar_carros(con=con):
    cursor = con.cursor()
    return cursor.execute(f'''
                SELECT marca, modelo, ano, id_veiculo FROM VEICULO; ''').fetchall()

