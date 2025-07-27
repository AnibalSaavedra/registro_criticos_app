
import streamlit as st
import pandas as pd
from datetime import datetime, time
import os
from io import BytesIO

st.set_page_config(page_title="Notificación de Valores Críticos", page_icon="🚨", layout="centered")
st.title("🚨 Registro de Notificación de Valores Críticos")

EXCEL_FILE = "registro_valores_criticos.xlsx"

# Cargar o crear DataFrame
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=[
        "Fecha", "ID Muestra", "Hora Firma", "Nombre Paciente", "Apellido Paterno", "Apellido Materno",
        "RUN-RUNFIC", "Analito con Valor Crítico", "Unidad", "Nombre quien recibe", "Cargo o Parentesco",
        "Hora Notificación", "Nombre quien comunica", "Tiempo de Respuesta", "Estado de Reporte", "Teléfono de Contacto"
    ])

# Formulario
with st.form("formulario_valores_criticos"):
    fecha = st.date_input("📅 Fecha de Medición", value=datetime.now().date())
    id_muestra = st.text_input("🆔 ID Muestra")
    hora_firma = st.time_input("🕒 Hora Firma", value=datetime.now().time())
    nombre_paciente = st.text_input("👤 Nombre Paciente")
    apellido_paterno = st.text_input("👤 Apellido Paterno")
    apellido_materno = st.text_input("👤 Apellido Materno")
    run = st.text_input("🧾 RUN o RUNFIC")
    analito = st.text_input("🧪 Analito con Valor Crítico")
    unidad = st.selectbox("📏 Unidad", ["mEq/L", "ng/mL", "%", "mg/dl", "N/A"])
    nombre_receptor = st.text_input("👂 Nombre quien recibe")
    cargo_receptor = st.selectbox("💼 Cargo o Parentesco", ["Medico", "Enfermera", "TENS", "Paciente", "Familiar directo", "Otro"])
    telefono_contacto = st.text_input("📞 Teléfono de Contacto")
    hora_notificacion = st.time_input("📞 Hora de Notificación", value=datetime.now().time())
    comunicador = st.selectbox("🗣️ Nombre quien comunica", [
        "Stefanie Maureira", "Anibal Saavedra", "Nycole Farias",
        "Felipe Fernandez", "Paola Araya", "Paula Gutierrez", "Maria Rodriguez"
    ])

    submit = st.form_submit_button("✅ Guardar Registro")

    if submit:
        if nombre_paciente and id_muestra and analito:
            if hora_firma > hora_notificacion:
                st.error("❌ La Hora de Firma no puede ser posterior a la Hora de Notificación.")
            else:
                tiempo_delta = datetime.combine(datetime.today(), hora_notificacion) - datetime.combine(datetime.today(), hora_firma)
                tiempo_minutos = max(int(tiempo_delta.total_seconds() // 60), 0)

                if tiempo_minutos <= 60:
                    estado_reporte = "Comunicación Efectiva"
                else:
                    estado_reporte = "Se contacta después de 60 minutos"

                nueva_fila = {
                    "Fecha": fecha.strftime("%Y-%m-%d"),
                    "ID Muestra": id_muestra,
                    "Hora Firma": hora_firma.strftime("%H:%M:%S"),
                    "Nombre Paciente": nombre_paciente,
                    "Apellido Paterno": apellido_paterno,
                    "Apellido Materno": apellido_materno,
                    "RUN-RUNFIC": run,
                    "Analito con Valor Crítico": analito,
                    "Unidad": unidad,
                    "Nombre quien recibe": nombre_receptor,
                    "Cargo o Parentesco": cargo_receptor,
                    "Hora Notificación": hora_notificacion.strftime("%H:%M:%S"),
                    "Nombre quien comunica": comunicador,
                    "Tiempo de Respuesta": tiempo_minutos,
                    "Estado de Reporte": estado_reporte,
                    "Teléfono de Contacto": telefono_contacto
                }

                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                st.success("✅ Registro guardado correctamente.")
        else:
            st.warning("⚠️ Debes completar los campos obligatorios.")

# Mostrar registros
st.markdown("### 📋 Registros Anteriores")
st.dataframe(df, use_container_width=True)

# Descargar Excel desde memoria
def to_excel_memory(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

excel_bytes = to_excel_memory(df)

st.download_button(
    label="📥 Descargar Registros",
    data=excel_bytes,
    file_name="registro_valores_criticos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Footer
st.markdown("---")
st.markdown("👨‍🔬 **Desarrollado por**: Anibal Saavedra | anibal.saavedra@crb.clinciasdelcobre.cl")
st.markdown("📧 **Contacto**: anibalsaavedra@crb.clinicasdelcobre.cl")
st.markdown("🔗 **Licencia**: [MIT](https://opensource.org/licenses/MIT)")
st.markdown("📅 **Última actualización**: 2025-07-27")
st.markdown("🌐 **Sitio Web**: [Clinicas del Cobre](https://www.clinicasdelcobre.cl)")
st.markdown("📊 **Versión**: 1.0.0")
