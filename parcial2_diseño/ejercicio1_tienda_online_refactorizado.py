# ejercicio1_tienda_online_refactorizado.py
"""
Sistema de Notificaciones de Pedidos - Refactorizado con SOLID y Patrones de Diseño

Principios SOLID aplicados:
- SRP: Cada clase tiene una única responsabilidad
- OCP: Abierto para extensión, cerrado para modificación
- LSP: Los notificadores son intercambiables
- ISP: Interfaz específica para notificadores
- DIP: Dependemos de abstracciones (Notifier), no de implementaciones

Patrones de diseño aplicados:
- Strategy Pattern: Cada notificador es una estrategia intercambiable
- Factory Pattern: NotifierFactory crea notificadores según el tipo
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

# ============================================================================
# ENTIDADES / MODELOS DE DATOS
# ============================================================================

@dataclass
class Customer:
    """Representa un cliente del sistema"""
    name: str
    email: str
    phone: str
    device_id: str


@dataclass
class Order:
    """Representa un pedido"""
    order_id: str
    customer: Customer
    total: float


@dataclass
class NotificationRecord:
    """Registro de una notificación enviada"""
    type: str
    recipient: str
    message: str
    timestamp: str


# ============================================================================
# STRATEGY PATTERN - Notificadores
# ============================================================================

class Notifier(ABC):
    """
    Interfaz abstracta para notificadores (Strategy Pattern)
    
    Principio DIP: Las clases de alto nivel dependen de esta abstracción
    Principio ISP: Interfaz específica y cohesiva para notificaciones
    """
    
    @abstractmethod
    def send(self, order: Order) -> NotificationRecord:
        """Envía una notificación y retorna el registro"""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """Retorna el tipo de notificación"""
        pass


class EmailNotifier(Notifier):
    """
    Notificador por correo electrónico
    
    Principio SRP: Solo se encarga de notificaciones por email
    """
    
    def get_type(self) -> str:
        return "email"
    
    def send(self, order: Order) -> NotificationRecord:
        message = (
            f"Estimado {order.customer.name}, su pedido #{order.order_id} "
            f"por ${order.total} ha sido confirmado."
        )
        recipient = order.customer.email
        
        print(f"📧 EMAIL enviado a {recipient}")
        print(f"   Asunto: Confirmación de Pedido #{order.order_id}")
        print(f"   Mensaje: {message}\n")
        
        return NotificationRecord(
            type=self.get_type(),
            recipient=recipient,
            message=message,
            timestamp=datetime.now().isoformat()
        )


class SMSNotifier(Notifier):
    """
    Notificador por SMS
    
    Principio SRP: Solo se encarga de notificaciones por SMS
    """
    
    def get_type(self) -> str:
        return "sms"
    
    def send(self, order: Order) -> NotificationRecord:
        message = (
            f"Pedido #{order.order_id} confirmado. "
            f"Total: ${order.total}. Gracias por su compra!"
        )
        recipient = order.customer.phone
        
        print(f"📱 SMS enviado a {recipient}")
        print(f"   Mensaje: {message}\n")
        
        return NotificationRecord(
            type=self.get_type(),
            recipient=recipient,
            message=message,
            timestamp=datetime.now().isoformat()
        )


class PushNotifier(Notifier):
    """
    Notificador por notificación push
    
    Principio SRP: Solo se encarga de notificaciones push
    """
    
    def get_type(self) -> str:
        return "push"
    
    def send(self, order: Order) -> NotificationRecord:
        message = f"¡Pedido confirmado! #{order.order_id} - ${order.total}"
        recipient = order.customer.device_id
        
        print(f"🔔 PUSH enviada al dispositivo {recipient}")
        print(f"   Mensaje: {message}\n")
        
        return NotificationRecord(
            type=self.get_type(),
            recipient=recipient,
            message=message,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# FACTORY PATTERN - Fábrica de Notificadores
# ============================================================================

class NotifierFactory:
    """
    Fábrica de notificadores (Factory Pattern)
    
    Principio OCP: Para agregar un nuevo notificador, solo se registra aquí
    sin modificar el código del OrderNotificationSystem
    """
    
    _notifiers: Dict[str, type] = {}
    
    @classmethod
    def register(cls, notifier_type: str, notifier_class: type):
        """Registra un nuevo tipo de notificador"""
        cls._notifiers[notifier_type] = notifier_class
    
    @classmethod
    def create(cls, notifier_type: str) -> Notifier:
        """Crea una instancia del notificador solicitado"""
        if notifier_type not in cls._notifiers:
            raise ValueError(f"Tipo de notificador desconocido: {notifier_type}")
        return cls._notifiers[notifier_type]()
    
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Retorna los tipos de notificadores disponibles"""
        return list(cls._notifiers.keys())


# Registrar notificadores disponibles
NotifierFactory.register("email", EmailNotifier)
NotifierFactory.register("sms", SMSNotifier)
NotifierFactory.register("push", PushNotifier)


# ============================================================================
# SISTEMA PRINCIPAL
# ============================================================================

class OrderNotificationSystem:
    """
    Sistema principal de notificaciones de pedidos
    
    Principio SRP: Solo orquesta el proceso de notificaciones
    Principio DIP: Depende de la abstracción Notifier, no de implementaciones
    """
    
    def __init__(self):
        self._notification_history: List[NotificationRecord] = []
    
    def process_order(self, order: Order, notification_types: List[str]) -> None:
        """
        Procesa un pedido y envía notificaciones según los tipos especificados
        
        Args:
            order: El pedido a procesar
            notification_types: Lista de tipos de notificación ('email', 'sms', 'push')
        """
        self._print_order_header(order)
        
        for notif_type in notification_types:
            try:
                notifier = NotifierFactory.create(notif_type)
                record = notifier.send(order)
                self._notification_history.append(record)
            except ValueError as e:
                print(f"⚠️  Error: {e}\n")
    
    def _print_order_header(self, order: Order) -> None:
        """Imprime el encabezado del pedido"""
        print(f"\n{'='*50}")
        print(f"Procesando pedido #{order.order_id}")
        print(f"Cliente: {order.customer.name}")
        print(f"Total: ${order.total}")
        print(f"{'='*50}\n")
    
    def get_notification_history(self) -> List[Dict]:
        """Retorna el historial de notificaciones como lista de diccionarios"""
        return [
            {
                "type": record.type,
                "to": record.recipient,
                "message": record.message,
                "timestamp": record.timestamp
            }
            for record in self._notification_history
        ]


# ============================================================================
# EJEMPLO DE EXTENSIBILIDAD (OCP)
# Para agregar WhatsApp, solo creamos la clase y la registramos
# ============================================================================

class WhatsAppNotifier(Notifier):
    """
    Notificador por WhatsApp - Ejemplo de extensibilidad
    
    Demuestra el principio OCP: Se agregó sin modificar código existente
    """
    
    def get_type(self) -> str:
        return "whatsapp"
    
    def send(self, order: Order) -> NotificationRecord:
        message = (
            f"🛒 *Pedido Confirmado*\n"
            f"Pedido: #{order.order_id}\n"
            f"Total: ${order.total}\n"
            f"¡Gracias por tu compra, {order.customer.name}!"
        )
        recipient = order.customer.phone
        
        print(f"💬 WHATSAPP enviado a {recipient}")
        print(f"   Mensaje: {message}\n")
        
        return NotificationRecord(
            type=self.get_type(),
            recipient=recipient,
            message=message,
            timestamp=datetime.now().isoformat()
        )


# Registrar el nuevo notificador (sin modificar código existente)
NotifierFactory.register("whatsapp", WhatsAppNotifier)


# ============================================================================
# FACADE PATTERN - Interfaz Simplificada
# ============================================================================

class NotificationFacade:
    """
    Fachada para el sistema de notificaciones (Facade Pattern - Estructural)
    
    Proporciona una interfaz simplificada para el sistema complejo de notificaciones.
    Oculta la complejidad de crear objetos Customer, Order y manejar el sistema.
    
    Principio: Simplifica el uso del sistema para el cliente
    """
    
    def __init__(self):
        self._system = OrderNotificationSystem()
    
    def send_order_notifications(
        self,
        order_id: str,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        device_id: str,
        total: float,
        channels: List[str]
    ) -> Dict:
        """
        Método simplificado para enviar notificaciones de un pedido.
        
        El cliente no necesita conocer las clases Customer, Order, etc.
        Solo pasa los datos y recibe el resultado.
        """
        # Crear objetos internamente (oculto al cliente)
        customer = Customer(
            name=customer_name,
            email=customer_email,
            phone=customer_phone,
            device_id=device_id
        )
        order = Order(order_id=order_id, customer=customer, total=total)
        
        # Procesar
        self._system.process_order(order, channels)
        
        return {
            "status": "success",
            "order_id": order_id,
            "channels_notified": channels,
            "total_notifications": len(channels)
        }
    
    def send_quick_email(self, order_id: str, name: str, email: str, total: float) -> Dict:
        """Atajo para enviar solo notificación por email"""
        return self.send_order_notifications(
            order_id=order_id,
            customer_name=name,
            customer_email=email,
            customer_phone="",
            device_id="",
            total=total,
            channels=["email"]
        )
    
    def send_all_channels(
        self,
        order_id: str,
        name: str,
        email: str,
        phone: str,
        device_id: str,
        total: float
    ) -> Dict:
        """Atajo para enviar por todos los canales disponibles"""
        all_channels = NotifierFactory.get_available_types()
        return self.send_order_notifications(
            order_id=order_id,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            device_id=device_id,
            total=total,
            channels=all_channels
        )
    
    def get_history(self) -> List[Dict]:
        """Obtiene el historial de notificaciones"""
        return self._system.get_notification_history()


# ============================================================================
# CÓDIGO DE PRUEBA
# ============================================================================

if __name__ == "__main__":
    
    # ========================================================================
    # DEMOSTRACIÓN 1: Uso directo del sistema (sin Facade)
    # ========================================================================
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 1: USO DIRECTO DEL SISTEMA")
    print("="*60)
    
    system = OrderNotificationSystem()
    
    # Pedido 1: Cliente premium (todos los canales)
    customer1 = Customer(
        name="Ana García",
        email="ana.garcia@email.com",
        phone="+34-600-123-456",
        device_id="DEVICE-ABC-123"
    )
    order1 = Order(order_id="ORD-001", customer=customer1, total=150.50)
    system.process_order(order1, ["email", "sms", "push"])
    
    # ========================================================================
    # DEMOSTRACIÓN 2: Uso del Facade (interfaz simplificada)
    # ========================================================================
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 2: USO DEL FACADE (PATRÓN ESTRUCTURAL)")
    print("Interfaz simplificada - no necesitas crear Customer/Order")
    print("="*60)
    
    facade = NotificationFacade()
    
    # Uso simplificado: solo pasar datos
    facade.send_order_notifications(
        order_id="ORD-002",
        customer_name="Carlos Ruiz",
        customer_email="carlos.ruiz@email.com",
        customer_phone="+34-600-789-012",
        device_id="DEVICE-XYZ-789",
        total=75.00,
        channels=["email", "sms"]
    )
    
    # Atajo: solo email
    print("--- Usando atajo send_quick_email ---")
    facade.send_quick_email(
        order_id="ORD-003",
        name="María López",
        email="maria@email.com",
        total=50.00
    )
    
    # ========================================================================
    # DEMOSTRACIÓN 3: Extensibilidad (OCP)
    # ========================================================================
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 3: EXTENSIBILIDAD (OCP)")
    print("WhatsApp agregado sin modificar código existente")
    print("="*60)
    
    facade.send_order_notifications(
        order_id="ORD-004",
        customer_name="Laura Méndez",
        customer_email="laura@email.com",
        customer_phone="+34-600-555-777",
        device_id="DEVICE-LMN-456",
        total=200.00,
        channels=["email", "whatsapp"]
    )
    
    # ========================================================================
    # HISTORIAL
    # ========================================================================
    print("\n" + "="*60)
    print("HISTORIAL DE NOTIFICACIONES")
    print("="*60)
    print(json.dumps(facade.get_history(), indent=2, ensure_ascii=False))