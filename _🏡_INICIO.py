import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.subheader("Aquí podras encontrar diversas herramientas 🛠️ que te ayudarán en tu trabajo de planillas o administración de personal")

st.markdown("")

st.markdown(" **Creador**: José Melgarejo")
st.markdown(" **Contacto**: [Linkedin](https://www.linkedin.com/in/jose-melgarejo/)")
st.markdown(" **Sugerencias o bugs**: josemelgarejo88@gmail.com")