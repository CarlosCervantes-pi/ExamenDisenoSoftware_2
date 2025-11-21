C4Container
    title Sistema de Notificaciones de Pedidos - Contenedores (C2)
    
    Person(user, "Usuario", "Cliente o Administrador")
    
    Container_Boundary(system, "Sistema de Notificaciones") {
        Container(facade, "NotificationFacade", "Python", "Interfaz simplificada con métodos predefinidos")
        Container(core, "OrderNotificationSystem", "Python", "Orquestador principal del proceso")
        Container(notifiers, "Notificadores", "Python", "EmailNotifier, SMSNotifier, PushNotifier, WhatsAppNotifier")
        Container(factory, "NotifierFactory", "Python", "Crea instancias de notificadores")
        Container(models, "Modelos de Datos", "Python", "Customer, Order, NotificationRecord")
    }
    
    System_Ext(external, "Servicios Externos", "SMTP, SMS Gateway, Push Service, WhatsApp API")
    
    Rel(user, facade, "Usa interfaz simplificada")
    Rel(facade, core, "Delega procesamiento")
    Rel(core, factory, "Solicita notificadores")
    Rel(factory, notifiers, "Crea instancias")
    Rel(core, models, "Utiliza")
    Rel(notifiers, external, "Envía notificaciones")