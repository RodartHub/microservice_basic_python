import pika

# 1. Conexión al servidor (tu contenedor mdi_bus)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Creamos una "fila" o cola de mensajes
channel.queue_declare(queue='ordenes_venta')

# 3. Enviamos un mensaje (Simulando una venta de Odoo)
mensaje = "Orden confirmada: ID 500 - Cliente: Rodrigo"
channel.basic_publish(exchange='',
                      routing_key='ordenes_venta',
                      body=mensaje)

print(f" [x] Mensaje enviado: '{mensaje}'")

connection.close()