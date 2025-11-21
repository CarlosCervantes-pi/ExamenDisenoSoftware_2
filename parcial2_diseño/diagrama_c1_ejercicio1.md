mermaid
C4Context
    title Sistema de Notificaciones de Pedidos - Contexto (C1)
    
    Person(cliente, "Cliente", "Realiza pedidos en la tienda online")
    Person(admin, "Administrador", "Gestiona el sistema de notificaciones")
    
    System(notifSystem, "Sistema de Notificaciones", "Envía notificaciones de pedidos por múltiples canales")
    
    System_Ext(emailServer, "Servidor SMTP", "Envío de correos electrónicos")
    System_Ext(smsGateway, "Gateway SMS", "Envío de mensajes de texto")
    System_Ext(pushService, "Servicio Push", "Notificaciones push móviles")
    System_Ext(whatsappAPI, "WhatsApp API", "Mensajería WhatsApp")
    
    Rel(cliente, notifSystem, "Realiza pedido")
    Rel(admin, notifSystem, "Configura canales")
    Rel(notifSystem, emailServer, "Envía emails")
    Rel(notifSystem, smsGateway, "Envía SMS")
    Rel(notifSystem, pushService, "Envía push")
    Rel(notifSystem, whatsappAPI, "Envía WhatsApp")