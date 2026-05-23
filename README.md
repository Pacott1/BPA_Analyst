# Automatización del tipo de cambio EUR/USD

## Descripción

Prototipo desarrollado en Python para automatizar la consulta diaria del tipo de cambio **EUR/USD**, almacenarlo en un histórico CSV y calcular su variación respecto al último registro disponible.

La solución evita tareas manuales repetitivas como consultar el dato, copiarlo a un archivo y realizar el cálculo de variación.

---

## Estructura del proyecto

```text
PRUEBA_BPA_ANALYST/
│
├── data/
│   └── tipo_cambio_EUR_USD.csv
│
├── docs/
│   └── Parte_1_Analisis_procesos.pdf
│
├── funciones.py
├── main.ipynb
├── script.py
├── README.md
└── requirements.txt
```

| Archivo | Descripción |
|---|---|
| `main.ipynb` | Notebook utilizado para visualizar y comprobar el funcionamiento del prototipo. |
| `funciones.py` | Funciones que realizan la consulta, tratamiento y almacenamiento de los datos. |
| `script.py` | Archivo preparado para ejecutar el proceso de forma automática. |
| `data/tipo_cambio_EUR_USD.csv` | Histórico acumulativo generado por el proceso. |
| `docs/Parte_1_Analisis_procesos.pdf` | Análisis visual del proceso actual y automatizado. |

---

## Parte 1 — Análisis del proceso

El análisis del proceso actual (**as-is**) y del proceso automatizado propuesto (**to-be**) se encuentra en:

[Parte 1 — Análisis de procesos](docs/Parte_1_Analisis_procesos.pdf)

De forma resumida, el proceso manual consiste en consultar diariamente el tipo de cambio, registrarlo, calcular su variación y comunicar el resultado. La propuesta automatizada sustituye la consulta y el cálculo manual por un script que obtiene el dato desde una API y actualiza un histórico CSV.

---

## Parte 2 — Prototipo en Python

### Funcionamiento

El prototipo:

1. Consulta la API pública de Frankfurter para obtener el tipo de cambio EUR/USD.
2. Extrae la fecha y el valor disponible.
3. Crea el archivo CSV si no existe previamente.
4. Añade nuevos registros al histórico.
5. Evita duplicar una fecha ya registrada.
6. Calcula la variación porcentual respecto al último registro.
7. Muestra un resumen del resultado por consola.



### Tecnologías utilizadas

- Python
- `requests`
- `pandas`
- `pathlib`
- Jupyter Notebook

### Fuente de datos

```text
https://api.frankfurter.app/latest?from=EUR&to=USD
```

### Instalación

Crear y activar un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

### Ejecución desde el notebook

Abrir `main.ipynb`, seleccionar el entorno virtual como kernel y ejecutar las celdas en orden.

La función principal es:

```python
frankfurter_wrapper()
```

### Ejecución como script

Para ejecutar el proceso directamente desde terminal:

```bash
python script.py
```

### Archivo generado

El histórico se guarda en:

```text
data/tipo_cambio_EUR_USD.csv
```

Ejemplo de estructura:

```text
date,rate,change_pct
2026-05-22,1.1595,0.0%
2026-05-23,1.1600,+0.04%
```

En la primera ejecución, la variación se inicializa en `0.0%` como punto de partida del histórico, ya que todavía no existe un registro anterior almacenado.

### Ejecución automática diaria

Para que el proceso se ejecute automáticamente cada día, utilizaría el **Programador de tareas de Windows**:

1. Crear una tarea con frecuencia diaria.
2. Seleccionar la hora de ejecución.
3. Indicar como programa el ejecutable de Python del entorno virtual.
4. Indicar como argumento la ruta de `script.py`.
5. Comprobar mediante una ejecución de prueba que el CSV se actualiza correctamente.

De esta forma, el proceso podría ejecutarse cada día sin necesidad de abrir manualmente el notebook.
---

## Parte 3 — Reflexión

### ¿Qué haría diferente si este script fuera a producción?

En producción ejecutaría el proceso desde `script.py` de forma programada, sin depender de la apertura manual del notebook. También añadiría un registro de ejecuciones y errores para poder comprobar si el proceso se ha completado correctamente. Si el volumen de datos aumentara, valoraría sustituir el CSV por una base de datos.

### ¿Qué pasa si la API falla un día? ¿Cómo lo manejaría?

El prototipo incorpora un tiempo máximo de espera de 15 segundos para evitar que el proceso quede bloqueado si la API no responde.

Si la API fallara o no devolviera la información esperada, el histórico no debería actualizarse con datos incompletos. Como siguiente mejora, incorporaría validaciones adicionales sobre los campos recibidos y un registro del error para facilitar su seguimiento.

### ¿Qué añadiría si tuviera más tiempo?

Añadiría el envío automático del resumen por email, ya que completa el proceso manual original. También incorporaría pruebas para comprobar que el cálculo de variación es correcto y que no se registran fechas duplicadas.

---

## Limitaciones actuales

- El histórico se guarda en un archivo CSV local.
- El envío automático por email no está implementado.
