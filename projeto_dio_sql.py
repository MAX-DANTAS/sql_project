from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy.sql import func

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente_account"
   
    # atributos
    id = Column(Integer, primary_key=True, autoincrement=True)  
    nome = Column(String, unique=True)
    cpf = Column(String, unique=True)
    endereco = Column(String, unique=True)
    
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereço={self.endereco})"
    
    
class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer, unique=True)
    id_cliente = Column(Integer, ForeignKey('cliente_account.id'), nullable=False, unique=True)
    saldo = Column(DECIMAL)
    
    cliente = relationship("Cliente", back_populates="conta")
    
    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero_da_conta={self.num}, saldo={self.saldo}) "
    
print(Cliente.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando classes como tabelas no banco de dados
Base.metadata.create_all(engine)

insp = inspect(engine)

print(insp.has_table("cliente_account"))

with Session(engine) as session:
    julia = Cliente(
        nome="Júlia Marques Maximo Dantas",
        cpf="25646377799",
        endereco="Nova Horizontino",
        conta=[Conta(tipo='Conta corrente', agencia='543453', num=8748, saldo=22)]
    )
    
    pedro = Cliente(
        nome="Pedro Silva",
        cpf="12345678900",
        endereco="Rua das Flores, 123",
        conta=[Conta(tipo='Conta poupança', agencia='123456', num=5678, saldo=1500)]
    )
    
    maria = Cliente(
        nome="Maria Oliveira",
        cpf="98765432100",
        endereco="Avenida Central, 456",
        conta=[Conta(tipo='Conta corrente', agencia='654321', num=1234, saldo=300)]
    )
    
    ana = Cliente(
        nome="Ana Souza",
        cpf="11223344556",
        endereco="Praça da Liberdade, 789",
        conta=[Conta(tipo='Conta poupança', agencia='789012', num=9012, saldo=5000)]
    )
        
    session.add_all([julia, pedro, maria, ana])
    session.commit()
    
    # Selecionando e ordenando os clientes pela conta
    stmt_order = session.execute(select(Cliente).order_by(Cliente.id)).scalars().all()
    for cliente in stmt_order:
        print(cliente)
    
    stmt_join = select(Cliente.cpf, Conta.saldo).join_from(Conta, Cliente)
    results = session.execute(stmt_join).all()
    for result in results:
        print(result)
        
    stmt_count = select(func.count('*')).select_from(Cliente)
    for result in session.scalars(stmt_count):
        print(result)