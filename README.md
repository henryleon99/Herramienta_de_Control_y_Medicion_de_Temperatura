# Herramienta de Control de Temperatura para Productos No Perecederos

## 📌 Descripción
Esta aplicación permite **simular, monitorear y proyectar** el comportamiento de la temperatura en productos no perecederos.
Incluye una interfaz gráfica interactiva desarrollada en **Python (Tkinter)** y utiliza **gráficos dinámicos** para el análisis.

La herramienta está diseñada como un apoyo para comprender riesgos de deterioro por condiciones de almacenamiento, integrando
**software libre (Python, Matplotlib, Pandas, Tkinter, tkcalendar)** con **software propietario (Microsoft Excel)** para la exportación
de reportes.

Actualmente, la aplicación también cuenta con una versión **ejecutable (.exe)** que no requiere instalar Python ni dependencias,
facilitando su uso en equipos Windows.

## 🚀 Funcionalidades
- Simulación de temperaturas en 10 productos predefinidos durante los últimos 5 días.
- Visualización de datos en gráficos de barras, líneas y matrices.
- Exportación de reportes a **Excel** con selección de rango de fechas.
- Animación de la evolución horaria de temperaturas.
- Gestión dinámica de productos (agregar / quitar).
- Pantalla de proyección con:
  - **Top 3** productos con mayor riesgo.
  - **Tendencia general** de riesgos.
  - **Gráfico de Pareto** proyectando 4 días hacia adelante.

## 🛠️ Tecnologías utilizadas
- **Python 3**
- **Tkinter** (interfaz gráfica)
- **Matplotlib** (visualizaciones)
- **Pandas** (gestión de datos)
- **tkcalendar** (selección de fechas)
- **openpyxl** (exportación a Excel)
- **PyInstaller** (para generar el ejecutable .exe)

## ⚙️ Instalación y ejecución

### 🔹 Opción 1: Ejecutar con Python
1. Clonar repositorio:
```bash
git clone https://github.com/usuario/herramienta-temperatura.git
cd herramienta-temperatura
```
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```
3. Ejecutar la aplicación:
```bash
python base.py
```

### 🔹 Opción 2: Ejecutar como programa (.exe)
1. Descargar el archivo `herramienta_temperatura.exe` desde la carpeta `dist/` o el release publicado.  
2. Ejecutar directamente el `.exe` en Windows sin necesidad de instalar Python ni librerías.  

## 📊 Exportación de datos
Los reportes pueden exportarse en formato `.xlsx` para su análisis en **Microsoft Excel**, permitiendo aprovechar lo mejor
del **software libre** y el **software propietario**.

## 🔒 Consideraciones éticas y de seguridad
- Transparencia en el manejo de datos simulados.
- Protección de información en implementaciones reales.
- Uso responsable de la herramienta como apoyo a la toma de decisiones.
- Posible escalabilidad hacia sensores reales con cumplimiento de estándares de ciberseguridad.

## 👥 Autores
- Erick Edgardo Delgado Palacios.
- Gabriel Eduardo García Hernández.
- Henry Reynaldo De León Morales.
- Nathaly Ivonne Espinoza de Méndez.
- Karen Olimpia Hernández Amaya.

Proyecto desarrollado como parte de un ejercicio académico para demostrar la integración entre tecnologías de software libre y propietario.
