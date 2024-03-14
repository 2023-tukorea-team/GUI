import tkinter as tk
from tkinter import Scrollbar, simpledialog, messagebox
from wifi import Cell
import subprocess
import re
import requests

def MAC_address():
    result = subprocess.check_output(["ifconfig"])
    mac_address = re.findall(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', result.decode())
    if mac_address:
        return mac_address[0]
    else:
        return None

def scan_wifi():
    Network = Cell.all('wlan0')
    list_wifi.delete(0, tk.END)
    for network in Network:
        list_wifi.insert(tk.END, f"SSID: {network.ssid} Signal Strenth: {network.signal}")

def connect_wifi():
    selected_index = list_wifi.curselection()
    if selected_index:
        ssid = list_wifi.get(selected_index[0]).split()[1]
        current_ssid = get_current_ssid()
        if current_ssid is not None:
            disconnect_wifi(current_ssid)
        
        password = simpledialog.askstring("password", f"Enter password for {ssid}: ")
        if password is not None:
            subprocess.call(['sudo', 'iwconfig', 'wlan0', 'essid', ssid, 'key', password])
            subprocess.call(['sudo', 'dhclient', 'wlan0'])
            status_label.config(text=f"Connected to {ssid}")
            show_server_connect_gui()

def get_current_ssid():
    try:
        output = subprocess.check_output(['iwgetid', '--raw', 'wlan0']).strip()
        return output.decode('utf-8')
    except subprocess.CalledProcessError:
        return None
    
def disconnect_wifi(ssid):
    subprocess.call(['sudo', 'iwconfig', 'wlan0', 'essid', 'off'])

def GUI_serverconnect():
    root.withdraw()  
    server_connect_window = tk.Toplevel(root)
    server_connect_window.title("[Server Connection]")
    
    
    id_label = tk.Label(server_connect_window, text="ID: ")
    id_label.pack()

    id_entry = tk.Entry(server_connect_window)
    id_entry.pack()

    check_button = tk.Button(server_connect_window, text="Check ID", command=checkId)
    check_button.pack()

    start_var = tk.BooleanVar()
    door_var = tk.BooleanVar()
    person_var = tk.BooleanVar()

    start_check = tk.Checkbutton(server_connect_window, text="Start", variable=start_var)
    start_check.pack()

    door_check = tk.Checkbutton(server_connect_window, text="Door", variable=door_var)
    door_check.pack()

    person_check = tk.Checkbutton(server_connect_window, text="Person", variable=person_var)
    person_check.pack()

    speed_label = tk.Label(server_connect_window, text="Speed:")
    speed_label.pack()

    speed_entry = tk.Entry(server_connect_window)
    speed_entry.pack()

    addlog_button = tk.Button(server_connect_window, text="Add Log", command=addLog)
    addlog_button.pack()

def checkId():
    id=id_entry.get()
    url='http://15.164.151.155:8080/sensor/checkid'
    params={'id':id}
    response=requests.post(url,json=params)

    if response.status_code==200:
        result=response.json()
        messagebox.showinfo("Connection Success.",f"Connection Success.\nresult: {result}")
        
    else:
        messagebox.showerror("Connection Failed.","Conncection Failed.\nTry Again.")
    
def addLog(sensor_id,start,door,person,spped):
    id=id_entry.get()
    start=start_var.get()
    door=door_var.get()
    person=person_var.get()
    speed=speed_entry.get()
    mac=MAC_address()

    url='http://15.164.151.155:8080/sensor/log'
    data={
        'id':id,
        'start':1 if start else 0,
        'door':1 if door else 0,
        'person':1 if person else 0,
        'speed': speed,
        'mac':mac
    }
    response=requests.post(url,json=data)

    if response.status_code==200:
        result=response.json()
        messagebox.showinfo("Connection Success.",f"Connection Success.\nresult: {result}")
    else:
        messagebox.showerror("Connection Failed.","Conncection Failed.\nTry Again.")

root = tk.Tk()
root.title("[WiFi Scanner]")

frame_wifi = tk.Frame(root)
frame_wifi.pack(padx=11, pady=11)

list_wifi = tk.Listbox(frame_wifi, width=50)
list_wifi.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = Scrollbar(frame_wifi, orient=tk.VERTICAL)
scrollbar.config(command=list_wifi.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
list_wifi.config(yscrollcommand=scrollbar.set)

scan_button = tk.Button(root, text="Scan WiFi", command=scan_wifi)
scan_button.pack()

connect_button = tk.Button(root, text="Connect WiFi", command=connect_wifi)
connect_button.pack()

status_label = tk.Label(root, text=" ")
status_label.pack()

root.mainloop()
