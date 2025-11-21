C4Context
    title Sistema de Generación de Reportes - Contexto (C1)
    
    Person(admin, "Administrador", "Usuario que genera reportes empresariales")
    Person(gerente, "Gerente", "Consulta reportes financieros y de ventas")
    
    System(reportSystem, "Sistema de Reportes", "Genera reportes en múltiples formatos y los entrega por diversos canales")
    
    System_Ext(emailServer, "Servidor de Email", "SMTP para envío de reportes")
    System_Ext(cloudStorage, "Almacenamiento en la Nube", "AWS S3, Google Cloud Storage")
    System_Ext(fileSystem, "Sistema de Archivos", "Almacenamiento local para descargas")
    
    Rel(admin, reportSystem, "Genera reportes")
    Rel(gerente, reportSystem, "Solicita reportes")
    Rel(reportSystem, emailServer, "Envía reportes por email")
    Rel(reportSystem, cloudStorage, "Sube reportes a la nube")
    Rel(reportSystem, fileSystem, "Guarda archivos para descarga")