from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
import pandas as pd
from forms import SancionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Necesario para CSRF

# Conexión a la base de datos
def init_db_connection():
    engine = create_engine('mysql+mysqlconnector://root@localhost/sanciones_db')
    return engine

# Cargar opciones para dropdowns
def load_options():
    engine = init_db_connection()
    municipios = pd.read_sql("SELECT id_municipio, nom_municipio FROM municipios", engine)
    return municipios

# Ruta para el formulario
@app.route('/form', methods=['GET', 'POST'])
def sancion_form():
    form = SancionForm()
    municipios = load_options()
    form.id_municipio_notificacion.choices = [(row.id_municipio, row.nom_municipio) for row in municipios.itertuples()]
    form.id_parroquia_notificacion.choices = [(0, 'Seleccione un municipio primero')]

    if form.validate_on_submit():
        engine = init_db_connection()
        data = {
            'codigo': form.codigo.data,
            'expediente_de_sancion': form.expediente_sancion.data,
            'expediente_de_origen': form.expediente_origen.data,
            'id_sala_de_origen': form.id_sala_origen.data,
            'rif': form.rif.data,
            'fecha_de_reinspeccion': form.fecha_reinspeccion.data,
            'numero_orden_de_servicio': form.numero_orden_servicio.data,
            'nombre_entidad_de_trabajo': form.nombre_entidad_trabajo.data,
            'direccion_de_notificacion': form.direccion_notificacion.data,
            'id_municipio_notificacion': form.id_municipio_notificacion.data,
            'id_parroquia_notificacion': form.id_parroquia_notificacion.data,
            'fech_recep_oficio': form.fech_recep_oficio.data,
            'fecha_indica_oficio': form.fecha_indica_oficio.data,
            'fecha_notificacion_del_procedimiento': form.fecha_notificacion_procedimiento.data,
            'folio_auto_de_apertura': form.folio_auto_apertura.data,
            'descripcion_inspectoría_del_trabajo': form.descripcion_inspectoría_trabajo.data,
            'id_inspector': form.id_inspector.data
        }

        query = """
            INSERT INTO proc_sancionatorio (
                codigo, expediente_de_sancion, expediente_de_origen, id_sala_de_origen, rif,
                fecha_de_reinspeccion, numero_orden_de_servicio, nombre_entidad_de_trabajo,
                direccion_de_notificacion, id_municipio_notificacion, id_parroquia_notificacion,
                fech_recep_oficio, fecha_indica_oficio, fecha_notificacion_del_procedimiento,
                folio_auto_de_apertura, descripcion_inspectoría_del_trabajo, id_inspector
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with engine.connect() as conn:
            conn.execute(query, (
                data['codigo'], data['expediente_de_sancion'], data['expediente_de_origen'],
                data['id_sala_de_origen'], data['rif'], data['fecha_de_reinspeccion'],
                data['numero_orden_de_servicio'], data['nombre_entidad_de_trabajo'],
                data['direccion_de_notificacion'], data['id_municipio_notificacion'],
                data['id_parroquia_notificacion'], data['fech_recep_oficio'],
                data['fecha_indica_oficio'], data['fecha_notificacion_del_procedimiento'],
                data['folio_auto_de_apertura'], data['descripcion_inspectoría_del_trabajo'],
                data['id_inspector']
            ))
        return redirect(url_for('sancion_form'))

    return render_template('form.html', form=form)

# Ruta para obtener parroquias dinámicamente
@app.route('/get_parroquias/<int:municipio_id>')
def get_parroquias(municipio_id):
    engine = init_db_connection()
    query = f"SELECT id_parroquia, nom_parroquia FROM parroquia WHERE id_municipio = {municipio_id}"
    parroquias = pd.read_sql(query, engine).to_dict(orient='records')
    return jsonify({'parroquias': parroquias})

if __name__ == '__main__':
    app.run(debug=True)