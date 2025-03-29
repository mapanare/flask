from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class SancionForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    expediente_sancion = StringField('Expediente de Sanción', validators=[DataRequired()])
    expediente_origen = StringField('Expediente de Origen', validators=[Optional()])
    id_sala_origen = StringField('ID Sala de Origen', validators=[Optional()])
    rif = StringField('RIF', validators=[DataRequired()])
    fecha_reinspeccion = DateField('Fecha de Reinspección', format='%Y-%m-%d', validators=[Optional()])
    numero_orden_servicio = StringField('Número Orden de Servicio', validators=[Optional()])
    nombre_entidad_trabajo = StringField('Nombre Entidad de Trabajo', validators=[DataRequired()])
    direccion_notificacion = TextAreaField('Dirección de Notificación', validators=[DataRequired()])
    id_municipio_notificacion = SelectField('Municipio de Notificación', coerce=int, validators=[DataRequired()])
    id_parroquia_notificacion = SelectField('Parroquia de Notificación', coerce=int, validators=[DataRequired()])
    fech_recep_oficio = DateField('Fecha Recepción Oficio', format='%Y-%m-%d', validators=[Optional()])
    fecha_indica_oficio = DateField('Fecha Indicada Oficio', format='%Y-%m-%d', validators=[Optional()])
    fecha_notificacion_procedimiento = DateField('Fecha Notificación Procedimiento', format='%Y-%m-%d', validators=[Optional()])
    folio_auto_apertura = StringField('Folio Auto de Apertura', validators=[Optional()])
    descripcion_inspectoría_trabajo = TextAreaField('Descripción Inspectoría del Trabajo', validators=[Optional()])
    id_inspector = StringField('ID Inspector', validators=[DataRequired()])
    submit = SubmitField('Guardar')