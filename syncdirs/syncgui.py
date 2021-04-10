import PySimpleGUI as sg



#sg.popup_get_folder("folder1")


sg.theme('Default1')

layout = [[sg.Text('Enter 2 files to comare')],
          [sg.Text('File 1', size=(8, 1)), sg.Input(key='t1'), sg.FileBrowse(key='b1')],
          [sg.Text('File 2', size=(8, 1)), sg.Input(key='t2'), sg.FileBrowse(key='b2')],
          [sg.Submit(), sg.Cancel()]]     

window = sg.Window('Window Title', layout)    

event, values = window.read()
window.close()
print(f'event is {event} and values is {values}')

text_input = values['t1']    
sg.popup(f'You entered {values["t1"]} and {values["t2"]}')