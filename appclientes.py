from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import sqlite3
import re
import csv
import os
from tkinter import messagebox, filedialog
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# -------------------------------------------------------------------------------
# AUTOR CALIQUIS CRISTIAN
# ------------------------------------------------------------------------------


aplicacion = tk.Tk()


valor_cuenta = IntVar()
valor_reparto = IntVar()
valor_cliente = IntVar()
valor_sucursal = IntVar()
valor_razon = StringVar()
valor_direccion = StringVar()
valor_localidad = StringVar()


titulo = Label(
    aplicacion,
    text="BASE CLIENTES",
    bg="Grey49",
    fg="white",
    height=1,
    width=55,
    font=("bold"),
)
titulo.grid(row=0, column=0, columnspan=7, padx=1, pady=1, sticky=W + E)


cuenta = Label(aplicacion, text="Cuenta :", fg="black", anchor="center")
cuenta.grid(row=1, column=0, sticky=W)
reparto = Label(aplicacion, text="Reparto :", fg="black", anchor="center")
reparto.grid(row=2, column=0, sticky=W)
numero_de_cliente = Label(
    aplicacion,
    text="Numero de Cliente : ",
    fg="black",
    anchor="center",
)
numero_de_cliente.grid(row=3, column=0, sticky=W)
sucursal = Label(
    aplicacion,
    text="Sucursal:",
    fg="black",
    anchor="center",
)
sucursal.grid(row=3, column=0, sticky=E)
razonsocial = Label(aplicacion, text="Razon Social : ", fg="black", anchor="center")
razonsocial.grid(row=4, column=0, sticky=W)
direccion = Label(aplicacion, text="Direccion : ", fg="black", anchor="center")
direccion.grid(row=5, column=0, sticky=W)
localidad = Label(aplicacion, text="Localidad :", fg="black", anchor="center")
localidad.grid(row=6, column=0, sticky=W)

entry_cuenta = Entry(aplicacion, textvariable=valor_cuenta, width=15)
entry_cuenta.grid(row=1, column=0)
entry_reparto = Entry(aplicacion, textvariable=valor_reparto, width=15)
entry_reparto.grid(row=2, column=0)
entry_numero_de_cliente = Entry(aplicacion, textvariable=valor_cliente, width=15)
entry_numero_de_cliente.grid(row=3, column=0)
entry_sucursal = Entry(aplicacion, textvariable=valor_sucursal, width=5)
entry_sucursal.grid(row=3, column=1, sticky=W)
entry_razonsocial = Entry(aplicacion, textvariable=valor_razon, width=30)
entry_razonsocial.grid(row=4, column=0)
entry_direccion = Entry(aplicacion, textvariable=valor_direccion, width=30)
entry_direccion.grid(row=5, column=0)
entry_localidad = Entry(aplicacion, textvariable=valor_localidad, width=30)
entry_localidad.grid(row=6, column=0)
entrybusqueda = ttk.Entry(aplicacion)
entrybusqueda.grid(row=9, column=0, padx=55, pady=8, ipady=3, ipadx=60)


# BASE SQLITE--------------------------------------------------------------------------


my_data = (
    []
)  # variable global que me permite en la funcion_imprimir(), pasar el string de datos del treeview


def base():
    con = sqlite3.connect("base_2.db")
    return con


def crear_tabla():
    con = base()
    cursor = con.cursor()
    sql = "CREATE TABLE clientes (cuenta INTERGER, reparto INTERGER, numero_de_cliente INTERGER PRIMARY KEY, sucursal INTERGER, razonsocial VARCHAR, direccion VARCHAR, localidad VARCHAR)"
    cursor.execute(sql)
    con.commit()


try:
    base()
    crear_tabla()
except:
    print("Hay un error")


# Funciones CRUD-------------------------------------------------------------------------


def actualizar(tree):

    records = tree.get_children()
    global my_data
    for element in records:
        tree.delete(element)
    sql = "SELECT * FROM clientes ORDER BY cuenta ASC"
    con = base()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    my_data = datos.fetchall()
    for fila in my_data:
        print(fila)
        tree.insert(
            "",
            "end",
            text=fila[0],
            values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]),
        )

    limpiar_registro()


# ----------------------------------------------------------------------------------------


def funcion_alta(
    cuenta,
    reparto,
    numero_de_cliente,
    sucursal,
    razonsocial,
    direccion,
    localidad,
    tree,
):
    if askquestion("Base Clientes", "Desea crear el registro"):
        cuenta = valor_cuenta.get()
        reparto = valor_reparto.get()
        numero_de_cliente = valor_cliente.get()
        sucursal = valor_sucursal.get()
        razonsocial = valor_razon.get()
        direccion = valor_direccion.get()
        localidad = valor_localidad.get()
        regex = valor_razon.get()
        expresion = "[a-zA-ZÀ-ÿ(0-9)]"
        if re.match(expresion, regex):
            Label(
                aplicacion, text="Registro valido", font="Courier, 10", fg="blue2"
            ).place(x=280, y=100)
            con = base()
            cursor = con.cursor()
            data = (
                cuenta,
                reparto,
                numero_de_cliente,
                sucursal,
                razonsocial,
                direccion,
                localidad,
            )
            sql = "INSERT INTO clientes(cuenta, reparto, numero_de_cliente, sucursal, razonsocial, direccion, localidad) VALUES(?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            tree.insert(
                "",
                "end",
                values=(
                    valor_cuenta.get(),
                    valor_reparto.get(),
                    valor_cliente.get(),
                    valor_sucursal.get(),
                    valor_razon.get(),
                    valor_direccion.get(),
                    valor_localidad.get(),
                ),
            )
            showinfo("Base Clientes", "Registro creado")
        else:
            Label(
                aplicacion,
                text="Invalido. Registro solo alfanumerico",
                font="Courier, 10",
                fg="red2",
            ).place(x=280, y=100)
            showwarning("Base Clientes", "No se pudo crear el registro")
    else:
        showwarning("Base Clientes", "No se pudo crear el registro")

    actualizar(tree)
    limpiar_registro()


# ------------------------------------------------------------------------------------------------------------


def limpiar_registro():
    valor_cuenta.set("0"), valor_reparto.set("0"), valor_cliente.set(
        "0"
    ), valor_sucursal.set("0"), valor_razon.set(""), valor_direccion.set(
        ""
    ), valor_localidad.set(
        ""
    )


# -----------------------------------------------------------------------------------------------------------


def funcion_borrar(tree):
    if askquestion("Base Clientes", "Desea eliminar el registro"):
        Label(
            aplicacion, text="Registro Eliminado", font="Courier, 15", fg="blue2"
        ).place(x=400, y=220)
        cliente = tree.selection()
        item = tree.item(cliente)
        print(item)
        print(item["text"])
        mi_id = item["text"]
        con = base()
        cursor = con.cursor()
        data = (mi_id,)
        tree.delete(cliente)
        sql = "DELETE FROM clientes WHERE cuenta = ?;"
        cursor.execute(sql, data)
        con.commit()
        limpiar_registro()
    else:
        Label(
            aplicacion, text="Registro No Eliminado", font="Courier, 15", fg="blue2"
        ).place(x=400, y=220)


# ------------------------------------------------------------------------------------------------------------


def funcion_modificar(tree):
    if askyesno("Base Clientes", "Desea modificar el registro?"):
        cliente = tree.selection()
        item = tree.item(cliente)
        mi_id = item["text"]
        con = base()
        cursor = con.cursor()
        sql = f"UPDATE clientes SET cuenta = '{valor_cuenta.get()}', reparto = '{valor_reparto.get()}', numero_de_cliente = '{valor_cliente.get()}', sucursal = '{valor_sucursal.get()}', razonsocial = '{valor_razon.get()}', direccion = '{valor_direccion.get()}', localidad = '{valor_localidad.get()}' WHERE cuenta = '{mi_id}';"
        cursor.execute(sql)
        con.commit()
        actualizar(tree)
        showinfo("Base Clientes", "Registro modificado")
    else:
        showinfo(
            "Base Clientes", "Debe seleccionar un registro y completar todos los campos"
        )


# -----------------------------------------------------------------------------------------------------------


def funcion_buscar(tree):
    records = tree.get_children()
    global my_data
    for element in records:
        tree.delete(element)
    sql = f"SELECT * FROM clientes WHERE cuenta LIKE '%{entrybusqueda.get()}%' OR reparto LIKE '%{entrybusqueda.get()}%' OR numero_de_cliente LIKE '%{entrybusqueda.get()}%' OR sucursal LIKE '%{entrybusqueda.get()}%' OR razonsocial LIKE '%{entrybusqueda.get()}%' OR direccion LIKE '%{entrybusqueda.get()}%' OR localidad LIKE '%{entrybusqueda.get()}%' "
    con = base()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    my_data = datos.fetchall()
    for fila in my_data:
        print(fila)
        tree.insert(
            "",
            "end",
            text=fila[0],
            values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]),
        )


def funcion_imprimir():
    # codigo para generar un txt con resultado del treeview -------
    """with open("pendientes.txt", "w") as f:    -------
    for item_id in tree.get_children():          -------
        item = tree.item(item_id)                -------
    print(item["text"], item["values"], file=f)  -------
    """
    # ---------------------------------------------------------------

    if len(my_data) < 1:
        showwarning("Base Clientes", "El archivo no fue exportado")
        return False
    fln = filedialog.asksaveasfilename(
        initialdir=os.getcwd(),
        title="Archivo CSV",
        filetypes=(("CVS Archivo", ".csv"), ("All files", ".*")),
    )
    with open(fln, mode="w") as myfile:
        exp_writer = csv.writer(myfile, delimiter=",")
        for i in my_data:
            exp_writer.writerow(i)
    messagebox.showinfo(
        "Archivo Exportado",
        "El archivo " + os.path.basename(fln) + " se exporto correctamente.",
    )


# -------------------------------------------------
# TREEVIEW
# -------------------------------------------------


tree = ttk.Treeview(aplicacion)

aplicacion.geometry("1125x740")

scroll = ttk.Scrollbar(aplicacion)
scroll.place(x=1105, y=310, height=380, width=15)
tree.config(yscrollcommand=scroll.set)
scroll.config(command=tree.yview)


"""
-------------------Theme anterior----------------
s = ttk.Style()
s.theme_use("clam")
s.configure("Treeview.Heading", background="Grey49", bg="white", fg="white")
s.configure(
    "Treeview",
    background="grey74",
    fieldbackground="grey74",
    foreground="black",
)
---------------------------------------------------
"""
Style = ttk.Style("superhero")
Style.configure(
    "Vertical.TScrollbar",
    gripcount=6,
    background="White",
    darkcolor="Black",
    troughcolor="gray78",
    bordercolor="Black",
    arrowcolor="gray36",
)


tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=50, minwidth=80, anchor=CENTER)
tree.column("col1", width=50, minwidth=80, anchor=CENTER)
tree.column("col2", width=130, minwidth=80, anchor=CENTER)
tree.column("col3", width=50, minwidth=80, anchor=CENTER)
tree.column("col4", width=300, minwidth=80, anchor=W)
tree.column("col5", width=290, minwidth=80, anchor=W)
tree.column("col6", width=230, minwidth=80, anchor=W)


tree.heading("#0", text="Cuenta")
tree.heading("col1", text="Reparto")
tree.heading("col2", text="Numero de Cliente")
tree.heading("col3", text="Sucursal")
tree.heading("col4", text="Razon Social")
tree.heading("col5", text="Direccion")
tree.heading("col6", text="Localidad")

tree.grid(column=0, row=20, columnspan=5, ipady=100)

boton_guardar = ttk.Button(
    aplicacion,
    text="Alta",
    bootstyle=DEFAULT,
    # bg="Grey49",
    # fg="white",
    # padx=71,
    # pady=3,
    command=lambda: funcion_alta(
        cuenta,
        reparto,
        numero_de_cliente,
        sucursal,
        razonsocial,
        direccion,
        localidad,
        tree,
    ),
)
boton_guardar.grid(row=3, column=2, padx=17, pady=8, ipady=1, ipadx=25, sticky=W)
boton_borrar = ttk.Button(
    aplicacion,
    text="Eliminar",
    bootstyle=DANGER,
    # bg="Grey49",
    # fg="white",
    # padx=60,
    # pady=3,
    command=lambda: funcion_borrar(tree),
)
boton_borrar.grid(row=4, column=2, padx=17, pady=8, ipady=1, ipadx=15, sticky=W)
boton_salir = ttk.Button(
    aplicacion,
    text="Salir",
    bootstyle=WARNING,
    # bg="Grey49",
    # fg="white",
    # padx=60,
    # pady=3,
    command=aplicacion.quit,
)
boton_salir.grid(row=6, column=3, padx=17, pady=8, ipady=1, ipadx=40, sticky=W)
boton_modificar = ttk.Button(
    aplicacion,
    text="Modificar",
    bootstyle=SUCCESS,
    # bg="Grey49",
    # fg="white",
    # padx=56,
    # pady=3,
    command=lambda: funcion_modificar(tree),
)
boton_modificar.grid(row=5, column=2, padx=17, pady=8, ipady=1, ipadx=10, sticky=W)
boton_actualizar = ttk.Button(
    aplicacion,
    bootstyle=DEFAULT,
    text="Actualizar",
    # bg="Grey49",
    # fg="white",
    # padx=56,
    # pady=3,
    command=lambda: actualizar(tree),
)
boton_actualizar.grid(row=6, column=2, padx=17, pady=8, ipady=1, ipadx=10, sticky=W)


boton_buscar = Button(
    aplicacion,
    text="Buscar",
    bg="Grey49",
    fg="white",
    command=lambda: funcion_buscar(tree),
)
boton_buscar.grid(row=9, column=0, padx=17, pady=8, ipady=1, ipadx=10, sticky=W)


boton_imprimir = ttk.Button(
    aplicacion,
    text="Exportar Archivo",
    bootstyle=LIGHT,
    # bg="Grey49",
    # fg="white",
    # padx=56,
    # pady=3,
    command=lambda: funcion_imprimir(),
)
boton_imprimir.grid(row=4, column=3, sticky=W)


aplicacion.mainloop()
