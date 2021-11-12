import json
import os
import pytz
from datetime import datetime, date
from win10toast import ToastNotifier

def save_reminder(timezone:str, date:str, message:str) -> bool:
    # Create reminders file if it doesn't exist
    if not os.path.exists('reminders.json'):
        with open('reminders.json', 'w') as file:
            json.dump({'reminders':[]}, file)

    # Read reminders file
    with open('reminders.json', 'r') as file:
        reminders = json.load(file)    

    # Modify reminders
    reminders['reminders'].append({'timezone': timezone, 'day': date,'message': message,})

    # Save reminders
    with open('reminders.json', 'w') as file:
        json.dump(reminders, file)

    return True


def check_reminders():

    with open('reminders.json', 'r') as file:
        reminders = json.load(file)    

    while True:

        for reminder in reminders['reminders']:

            actual_date = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            if reminder['timezone']:
                timezone = pytz.timezone(reminder['timezone'])
                actual_date = datetime.now(timezone).strftime('%d/%m/%Y %H:%M')


            if reminder['day'] == actual_date:
                # Delete reminder
                msg =  reminder['message']
                reminders['reminders'].remove(reminder)

                with open('reminders.json', 'w') as file:
                    json.dump(reminders, file)

                yield msg
                



def add_reminder() -> None:
    print('Hola ingrese la zona horaria y la fecha con el siguiente formato')
    print('Zona horaria: Continente/Ciudad, Fecha: dia/mes/año hora:minutos')
    print(f"Ejemplo: America/Mexico_City  -  {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    zona_horaria:str = input("Ingrese la zona horaria (o dejelo en blanco para usar la local): ")
    dia_hora:str = input("Ingrese dia y hora a acordar: ")
    mensaje:str = input("Ingrese mensaje a recordar: ")

    if save_reminder(zona_horaria, dia_hora, mensaje):
        print('Tu recordatorio se ha guardado correctamente :) \n')   
    

def main(): 
    toaster = ToastNotifier()

    add_reminder()

    reminders = check_reminders()

    for msg in reminders:
        toaster.show_toast('- RECORDATORIO -',msg)


if __name__ == "__main__":
    main()
