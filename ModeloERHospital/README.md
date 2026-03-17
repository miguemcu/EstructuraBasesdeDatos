# Modelo ER - Hospital (Notación Baker)

En este archivo hice un modelo Entidad-Relacion para un hospital, siguiendo el enunciado del taller.

Archivo principal:
- diagrama_hospital.drawio: aqui esta el diagrama completo.

El modelo:
- Entidades: Empleado, Sala y Paciente.
- Atributos identificadores (#):
  - Empleado: n0_empleado.
  - Sala: codigo_sala.
  - Paciente: n0_registro.
- Otros atributos:
  - Empleado: direccion, telefono, nombre.
  - Sala: nombre, cantidad_camas.
  - Paciente: nombre.
- Relaciones (segun el diagrama):
  - Empleado trabaja en Sala (N a 1): varios empleados trabajan en una misma sala.
  - Paciente esta internado en Sala (N a 1): varios pacientes están internados en una misma sala.
  - Desde Sala se ve la inversa: una sala puede tener trabajando empleados y tiene internado(s) pacientes.

