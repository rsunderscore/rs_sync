import PySimpleGUI as sg
import utils as u

# altered sync to return a string rather than printing
#u.sync(dir1, dir2)

sg.theme('Default1')
sg.FolderBrowse()
layout = [[sg.Text('Enter 2 files to comare')],
          [sg.Text('File 1', size=(8, 1)), sg.Input(key='t1'), sg.FolderBrowse(key='b1')],
          [sg.Text('File 2', size=(8, 1)), sg.Input(key='t2'), sg.FolderBrowse(key='b2')],
          [sg.Checkbox(' Report Only', key='report_only', default=True)],
          [sg.Combo(['newer','bigger'], key='conflict_handling', default_value='newer')],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Window Title', layout)    

event, values = window.read()
window.close()
print(f'event is {event} and values is {values}')
s=u.sync(values['t1'], values['t2'], report_only=values['report_only'], favornewer=True)
print(s)
sg.popup_scrolled(s,title='output', size=(80,10))


#show output in a window as well
#or generate output as a text file and open it
#window with export button
#text_input = values['t1']    
#sg.popup(f'You entered {values["t1"]} and {values["t2"]} all values {values}')


def test_popup():
    s="""1
    2
    3
    4
    5
    6
    7
    8
    9
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    """
    sg.popup_scrolled(s,title='output', size=(80,10))


# reroute print stmts to a StringIO
def redirect_print():
    """return the stringIO that will contain all the print output
        - need to do this as a context manager???
    """
    import sys
    old_stdout = sys.stdout
    from io import StringIO
    my_stdout = StringIO()
    sys.stdout = my_stdout
    print('test')
    sys.stdout = old_stdout
    my_stdout.getvalue()