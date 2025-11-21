C4Container
    title Sistema de Generación de Reportes - Contenedores (C2)
    
    Person(user, "Usuario", "Administrador o Gerente")
    
    Container_Boundary(system, "Sistema de Reportes") {
        Container(facade, "ReportFacade", "Python", "Interfaz simplificada con atajos predefinidos")
        Container(core, "ReportSystem", "Python", "Orquestador principal del proceso")
        Container(generators, "Generadores", "Python", "SalesReport, InventoryReport, FinancialReport, AuditReport")
        Container(formatters, "Formateadores", "Python", "PDFFormatter, ExcelFormatter, HTMLFormatter")
        Container(delivery, "Métodos de Entrega", "Python", "EmailDelivery, DownloadDelivery, CloudDelivery")
        Container(factories, "Factories", "Python", "ReportGeneratorFactory, FormatterFactory, DeliveryFactory")
    }
    
    System_Ext(external, "Servicios Externos", "Email, Cloud, FileSystem")
    
    Rel(user, facade, "Usa interfaz simplificada")
    Rel(facade, core, "Delega generación")
    Rel(core, factories, "Solicita componentes")
    Rel(factories, generators, "Crea generadores")
    Rel(factories, formatters, "Crea formateadores")
    Rel(factories, delivery, "Crea métodos de entrega")
    Rel(delivery, external, "Entrega reportes")