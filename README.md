# Práctica: microservicios con mensajería y API

Proyecto de clase que simula un flujo sencillo de **microservicios**: un productor envía “órdenes” por **RabbitMQ**, un consumidor las **persiste en PostgreSQL** y una **API FastAPI** expone esas órdenes por HTTP. Incluye instrumentación con **Prometheus** (métricas de la API) y un stack opcional con **Grafana**.

## Estructura del proyecto

La **raíz del repositorio** es la carpeta donde está este `README.md`. El código Python vive en la subcarpeta `scripts/`:

```
.
├── docker/              # docker-compose, prometheus.yml
├── scripts/             # aplicación Python (api, BD, sender, receiver)
│   ├── api.py
│   ├── database.py
│   ├── receiver.py
│   └── sender.py
├── .gitignore
├── README.md
└── venv/                # local (no se sube al repo)
```

## Qué hace cada parte

| Componente | Ubicación | Rol |
|------------|-----------|-----|
| Infraestructura | `docker/docker-compose.yml` | RabbitMQ, PostgreSQL (puerto host **5433**), Prometheus y Grafana |
| Modelo y BD | `scripts/database.py` | SQLAlchemy, tabla `ordenes_procesadas`, función `init_db()` |
| Productor | `scripts/sender.py` | Publica un mensaje en la cola `ordenes_venta` |
| Consumidor | `scripts/receiver.py` | Lee la cola y guarda cada mensaje en PostgreSQL |
| API de consulta | `scripts/api.py` | FastAPI: `/`, `/ordenes` y métricas Prometheus (`prometheus-fastapi-instrumentator`) |

La URL de base de datos en código es `postgresql://admin:password123@localhost:5433/micro_service_db`, alineada con el `docker-compose`.

## Requisitos previos

- **Docker** y **Docker Compose**
- **Python 3.10+** (recomendado 3.12)

## Cómo inicializarlo

### 1. Levantar la infraestructura

Desde la **raíz del proyecto**:

```bash
cd docker
docker compose up -d
cd ..
```

Servicios útiles:

- RabbitMQ (AMQP): `localhost:5672`
- Panel RabbitMQ: http://localhost:15672 (usuario/contraseña por defecto en la imagen: `guest` / `guest`)
- PostgreSQL en el host: `localhost:5433`
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (usuario `admin`, contraseña `admin` según el compose)

### 2. Entorno Python y dependencias

En la **raíz del proyecto** (junto al `README.md`):

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary pika prometheus-fastapi-instrumentator
```

### 3. Crear las tablas en PostgreSQL

Los imports de los módulos están pensados para ejecutarse **desde la carpeta `scripts/`** (la de los `.py`). Con el venv activado y los contenedores en marcha:

```bash
cd scripts
python database.py
cd ..
```

Deberías ver un mensaje indicando que las tablas se crearon correctamente.

### 4. Ejecutar los servicios (varias terminales)

Misma regla: terminal con directorio de trabajo en `scripts/` (subcarpeta con el código).

1. **Consumidor**:

   ```bash
   cd scripts
   python receiver.py
   ```

2. **Productor** (opcional):

   ```bash
   cd scripts
   python sender.py
   ```

3. **API**:

   ```bash
   cd scripts
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

Luego abre en el navegador:

- http://localhost:8000 — mensaje de bienvenida
- http://localhost:8000/ordenes — lista de órdenes guardadas
- http://localhost:8000/docs — documentación interactiva (Swagger)

Prometheus del compose está configurado para scrapear la API en `host.docker.internal:8000`; con la API en el puerto 8000 del host, las métricas deberían verse en Prometheus tras unos segundos.

