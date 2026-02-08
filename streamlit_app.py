import pandas as pd
import numpy as np
import streamlit as st

from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="products-project")
dbProductos = db.collection('productos')

# Create the title for the web app
st.title("Inventario de productos")


# Crea producto
st.header("Nuevo producto")
codigo = st.text_input('Codigo: ')
nombre = st.text_input('Nombre: ')
precio = st.text_input('Precio: ')
existencias = st.text_input('Existencias: ')
stock_minimo = st.text_input('Stock minimo: ')
stock_maximo = st.text_input('Stock maximo: ')

submit = st.button('Crear nuevo registro')

if codigo and nombre and precio and existencias and stock_minimo and stock_maximo and submit:
  doc_ref = db.collection('productos').document(nombre)
  doc_ref.set({
      'codigo': codigo,
      'nombre':nombre,
      'precio':precio,
      'existencias': existencias,
      'stock_minimo': stock_minimo,
      'stock_maximo':stock_maximo
  })
  st.sidebar.write('Producto creado')

#Busca por nombre
def loadByNombre(nombre):
  productos_ref = dbProductos.where(u'nombre', u'==', nombre)
  currentNombre = None
  for myname in productos_ref.stream():
    currentNombre = myname
  return currentNombre

st.sidebar.subheader("Buscar nombre")
nameSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Filtrar")

if (btnFiltrar):
  doc = loadByNombre(nameSearch)
  if doc is None:
    st.sidebar.write("El producto no existe")
  else:
    st.sidebar.write(doc.to_dict())

#Eliminar
st.sidebar.markdown("---'")
btnEliminar = st.sidebar.button("Eliminar")

if (btnEliminar):
  deletename = loadByNombre(nameSearch)
  if deletename is None:
    st.sidebar.write("El producto no existe")
  else:
    dbProductos.document(deletename.id).delete()
    st.sidebar.write("Producto eliminado")

st.sidebar.markdown("---'")

#Modificar
newname = st.sidebar.text_input("Modificar nombre")
btnModificar = st.sidebar.button("Modificar")

if btnModificar:
  updatename = loadByNombre(nameSearch)
  if updatename is None:
    st.sidebar.write("El producto no existe")
  else:
    myupdatename=dbProductos.document(updatename.id)
    myupdatename.update({
        'nombre': newname
    })


#Listado de produtos
productos_ref = list(db.collection(u'productos').stream())
productos_dict = list(map(lambda x: x.to_dict(), productos_ref))
productos_dataframe = pd.DataFrame(productos_dict)
st.dataframe(productos_dataframe)
