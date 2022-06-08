from datetime import datetime
from sqlite_handler import *
import sys
import os

# Os functions <------------------------------------------------------------------------->
clear = lambda: os.system('cls')
sys.tracebacklimit = 0
# <-------------------------------------------------------------------------------------->

# Simple functions <--------------------------------------------------------------------->
def get_time():
    return datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
def is_string(string_input): # Confere se o nome passado é uma string
    return isinstance(string_input, str)
def is_integer(age):
    return isinstance(age, int)
def contains_number(text):
    for character in text:
        if character.isdigit():
            return True
    return False
# <-------------------------------------------------------------------------------------->

# Parsing functions <-------------------------------------------------------------------->
def parse_name():
    name = input("Digite seu nome: ")
    if contains_number(name):
            print("O nome do paciente deve conter apenas letras.")
            name = parse_name()
    if len(name) > 60:
            print("O nome do paciente deve ter menos de 60 caracteres.")
            name = parse_name()
    return name
def parse_age():
    age = input("Digite sua idade: ")
    if not age.isdecimal():
        print("A idade do paciente pode conter apenas números.")
        age = parse_age()
    if int(age) > 100 or int(age) < 0:
        print("A idade deve estrar entre 120 e 0.")
        age = parse_age()
    return int(age)
def parse_gender():
    gender = input("Digite seu gênero: ")
    if contains_number(gender):
        print("O gênero do paciente deve conter apenas letras.")
        gender = parse_gender()
    if gender[0].upper() not in ['M','F','O']:
        print("O gênero deve ser uma opção válida (Masculino, Feminino, Outro).")
        gender = parse_gender()
    return gender[0]
def parse_id():
    id = input("Digite sua identificação: ")
    if is_registered(id):
        print("Identificação já registrada.")
        id = parse_id()
    if not id.isnumeric():
        print("A identificação do paciente pode conter apenas números.")
        id = parse_id()
    return id
def parse_id_for_login():
    id = input("Digite sua identificação: ")
    if not is_registered(id):
        print("Identificação não registrada.")
        id = parse_id_for_login()
    if not id.isnumeric():
        print("A identificação do paciente pode conter apenas números.")
        id = parse_id_for_login()
    return id
def parse_phone_number():
    phone_number = input("Digite seu número de telefone: ")
    if not phone_number.isnumeric():
        print("Patient's phone number can only have numbers.")
        phone_number = parse_phone_number()
    if len(phone_number) < 10 or len(phone_number) > 11:
        print("O número de telefone deve ter entre 10 a 11 caracteres. (Ex: 21 91234 5678")
        phone_number = parse_phone_number()

    return phone_number
# <--------------------------------------------------------------------------------------> 

# Login functions <-------------------------------------------------------------------->
def log_in():
    id = parse_id_for_login()

    data = get_data_by_id(id)
    name = data[0]
    age = data[1]
    gender = data[2]
    id = data[3]
    phone_number = data[4]
    register_date = data[5]

    return Patient(name, age, gender, id, phone_number, register_date)
def register():
    name = parse_name()
    age = parse_age()
    gender = parse_gender()
    id = parse_id()
    phone_number = parse_phone_number()
    registered_date = get_time()
    create_new_patient(name, age, gender, id, phone_number, registered_date)

    return Patient(name, age, gender, id, phone_number, registered_date)
# <-------------------------------------------------------------------------------------->

# Menu functions <----------------------------------------------------------------------->
def print_menu(menu):
    clear()
    for key, value in menu.items():
        print(key, value)
def main_menu():
    main_menu_options = {
    "1": "Conectar",
    "2": "Registrar",
    "3": "Terminar aplicação"
}
    while True:
        print_menu(main_menu_options)
        option = input("Digite sua escolha: ")
        clear()

        if option == "1":
            usuario = log_in()
            first_menu(usuario)
        elif option == "2":
            usuario = register()
            first_menu(usuario)
        elif option == "3":
            quit()
def first_menu(usuario):
    first_menu_options = {
        "Bem vindo": f"{usuario.nome}\n",
        "1": "Agendar consulta",
        "2": "Ver histórico de consultas",
        "3": "Ver dados de usuário",
        "4": "Voltar ao menu"
    }
    while True:
        
        print_menu(first_menu_options)
        option = input("Digite sua escolha: ")
        clear()
        if option == "1":
            usuario.make_an_appointment()
        elif option == "2":
            usuario.get_appointments_history()
        elif option == "3":
            usuario.see_data()
        elif option == "4":
            return
# <-------------------------------------------------------------------------------------->
    
# Classes and class functons <----------------------------------------------------------->
class Patient:
    def __init__(self, name, age, gender, id, phone_number, register_date):
        self.nome = name
        self.idade = age
        self.gênero = gender
        self.identificação = id
        self.telefone = phone_number
        self.registro = register_date

    def see_data(self):
        for key, value in vars(self).items():
            print(key.capitalize() + ":", value)
        input("\nAperte algo para voltar.")
        clear()

    def make_an_appointment(self):

        id = self.identificação
        problem_description = input("Descreva o motivo da consulta: ")
        date = input("Digite no formato DD/MM/YYYY a data para a consulta: ")
        location = input("Digite o nome de seu estado e cidade (Ex: Teresópolis, RJ): ")
        create_new_appointment(id, problem_description, date, location)

        print("Consulta marcada com sucesso.")
        input("Aperte algo para continuar. ")
    
    def get_appointments_history(self):
        count = 1
        for appointment in get_appointments_from_id(self.identificação):
            descrição = appointment[1]
            data = appointment[2]
            local = appointment[3]

            print(f"Número: {count}, Descrição: {descrição}, Data: {data}, Local: {local}")
            count += 1

        input("\nAperte algo para continuar. ")
# <-------------------------------------------------------------------------------------->