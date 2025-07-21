---
marp: true
theme: default
paginate: true
---

# UN Mapa  
## Presentación de Proyecto  
### Ingeniería de Software I

Universidad Nacional de Colombia  
Sede Bogotá  
Estudiantes: Andres F. Franco, Daniel A. Ortiz, David F. Benjumea, Jesús E. Pérez

---

## 🎯 Objetivo del Proyecto

Desarrollar una aplicación de escritorio interactiva que:

- Facilite la **orientación dentro del campus**.
- Permita visualizar **eventos, edificios y servicios** georreferenciados.

---

## 📋 Levantamiento de Requerimientos

- Entrevistas informales con estudiantes.
- Consulta de documentos institucionales.
- Revisión comparativa con herramientas como Google Maps.

---

## ⚠️ Errores y Retroalimentación

- Alcance inicial muy ambicioso → se ajustó a recursos del curso.
- Alcance inicial muy genéfico → se incluyeron funciones inovadoras. 
- Requisitos mal definidos: evento ≠ solicitud de evento.
- Dificultad para modelar "estados" y "alertas" en tiempo real.
- Se simplificaron funcionalidades de rutas y filtros dinámicos. (Implementación de Google Maps).

---

## 🛠️ Tecnologías Seleccionadas

| Componente        | Herramienta         | Justificación |
|------------------|---------------------|---------------|
| Lenguaje         | Python 3.x          | Claro, potente, conocido por el equipo. |
| GUI              | Pywebview y Jinja2  | HTML embebido, sin servidor web. |
| Mapa interactivo | Folium              | Mapa offline, visual e intuitivo. |
| Base de datos    | MySQL               | Robusta, integrable y relacional. |
| Testing          | unittest / pytest   | Documentadas, fáciles de integrar. |
| Seguridad        | bcrypt / hashlib    | Contraseñas cifradas. |
| Estilo           | flake8              | Clean Code con estándar PEP8. |

---

## 👥 Dificultades al Programar en Equipo

- Conflictos de ramas y rutas absolutas en el código.
- Inexperiencia en uso de Git y GitHub por parte de algunos miembros.
- Diferencias de estilo → definimos convenciones comunes.
- Sincronización de horarios de trabajo → usamos un grupo de Whatsapp para coordinar y asignar tareas.

---

## ✅ Herramientas de Testing

- `unittest`: básico, pero funcional para integración rápida.
- Fixtures para pruebas con base de datos temporal.
- Integración con linter (`flake8`) para validación de estilo.

---

## 🔁 Retroalimentación sobre Testing

- Algunas pruebas iniciales eran muy **simples**.
- No se cubrían casos negativos ni errores comunes.
- Se agregó validación de lógica de negocio:  
  ✅ Ej: Verificación de contraseñas débiles, y autentificación de usuarios.

---

## 💥 Reto Importante

### Visualización del mapa sin conexión a Internet

**Problema:**
- El campus es grande y los eventos son dinámicos.
- No existía base de datos que conecte edificios con su geolocalización

**Solución:**
- Generamos un mapa SVG offline, y una base de datos apropiada.
- Integramos `folium` con datos georreferenciados y lógica desde Python.
- Añadimos renderizado dinámico por estado y tipo de lugar, poblado desde la base de datos.

---


## 🙌 Gracias

¿Preguntas o comentarios?

> [Repositorio](https://github.com/AFrancoSUNAL/Algoritmicos) | Universidad Nacional de Colombia  
