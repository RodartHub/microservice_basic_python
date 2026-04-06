import pika, sys, os
from database import SessionLocal, OrdenProcesada

def callback(ch, method, properties, body):
    mensaje_texto = body.decode()
    print(f" [v] Recibido: {mensaje_texto}")
    
    # --- LÓGICA DE PERSISTENCIA ---
    db = SessionLocal()
    nueva_orden = OrdenProcesada(contenido=mensaje_texto)
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    db.close()
    # ------------------------------
    
    print(f" [!] Guardado en DB con ID: {nueva_orden.id}")

def main():
    # 1. Conexión al mismo servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 2. Nos aseguramos de que la cola existe
    channel.queue_declare(queue='ordenes_venta')

    # 4. Le decimos a RabbitMQ que use esa función para esta cola
    channel.basic_consume(queue='ordenes_venta', 
                         on_message_callback=callback, 
                         auto_ack=True)

    print(' [*] Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)