import streamlit as st
from PyPDF2 import PdfReader
import zipfile
import os
import shutil

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.title("🗃️ RENOMBRA ARCHIVOS AFP")
st.markdown("Te toma tiempo renombrar los archivos pdf de AFP?")
st.markdown("Ya tienes la solución! En esta página podras cargar los archivos y se renombrarán automáticamente.")

def split_pdf_text(pdf):
    reader = PdfReader(pdf)
    page = reader.pages[0]
    content = page.extract_text().split("\n")
    return content

def generate_pdf_parameters(content):
    tabla_tipo_doc = {"PLANILLA": "PLANILLAS", "Comprobante": "CONSTANCIAS PAGO"}
    tipo_doc = content[0].split(" ")[0]
    tabla_ruc = {"PLANILLA": 7, "Comprobante": 8}
    tabla_afp = {"PLANILLA": 67, "Comprobante": 2}
    tabla_planilla = {"PLANILLA": 2, "Comprobante": 6}
    ruc = content[tabla_ruc[tipo_doc]].removeprefix("RUC: ")
    nro_planilla = content[tabla_planilla[tipo_doc]]
    name_afp = content[tabla_afp[tipo_doc]]
    periodo_devengue = content[4]
    pdf_new_name = "_".join([ruc, tabla_tipo_doc[tipo_doc], name_afp, periodo_devengue, nro_planilla])
    return {"pdf_name": pdf_new_name + ".pdf", "afp": name_afp, "periodo": periodo_devengue, "tipo_doc": tabla_tipo_doc[tipo_doc],"ruc":ruc}

def check_pdf_afp(content):
    if content[0].split(" ")[0] in ["PLANILLA","Comprobante"]:
        return True
    else:
        return False
    

files = st.file_uploader(label="Carga tus archivos pdf",accept_multiple_files=True,
                         type=["pdf"],help="Acepta solo .pdf")

if files:
    not_afp_files = []
    for file in files:
        if not check_pdf_afp(split_pdf_text(file)):
            not_afp_files.append(file.name)
    if not_afp_files:
        text = " - " + "\n- ".join(not_afp_files)
        st.error("No se podrá procesar a los siguientes archivos, por favor retiralos de la carga:",icon="🚨")
        st.error(text)  

converted_files = []

temp_folder = "temp"
def save_uploadedfile(uploadedfile):
    with open(os.path.join(temp_folder, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

if files and not not_afp_files:
    button_process_pdf = st.button("Procesar PDF")
    if button_process_pdf:
        os.makedirs(temp_folder,exist_ok=True)
        for file in files:
            content = split_pdf_text(file)
            pdf_parameters = generate_pdf_parameters(content)
            file.name = pdf_parameters["pdf_name"]
            new_filename = os.path.join(temp_folder, pdf_parameters["pdf_name"])
            save_uploadedfile(file)
            converted_files.append(new_filename)

        output_zip = "converted_files.zip"

        with zipfile.ZipFile(output_zip, "w") as zipf:
            for file in converted_files:
                zipf.write(file, os.path.basename(file))

        shutil.rmtree(temp_folder)
        st.success("Se ha convertido los archivos correctamente. Ya puedes descargarlos.")

        # Get the contents of the ZIP archive
        with open(output_zip, "rb") as zip_file:
            zip_contents = zip_file.read()

        st.download_button(
            label="Descargar archivo comprimido",
            data=zip_contents,
            file_name=output_zip)
        
        os.remove(output_zip)


st.markdown(" **Creador**: José Melgarejo")
st.markdown(" **Contacto**: [Linkedin](https://www.linkedin.com/in/jose-melgarejo/)")