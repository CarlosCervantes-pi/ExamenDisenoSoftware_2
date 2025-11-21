# ejercicio2_gestor_documentos_refactorizado.py
"""
Sistema de Generación de Reportes - Refactorizado con SOLID y Patrones de Diseño

Principios SOLID aplicados:
- SRP: Separación clara entre generadores, formateadores y métodos de entrega
- OCP: Nuevos tipos se agregan sin modificar código existente
- LSP: Todas las implementaciones son intercambiables
- ISP: Interfaces pequeñas y específicas
- DIP: Dependemos de abstracciones, no de implementaciones

Patrones de diseño aplicados:
- Strategy Pattern: Formateadores y métodos de entrega intercambiables
- Factory Pattern: Fábricas para crear cada componente
- Template Method: Estructura base para generadores de reportes
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

# ============================================================================
# ENTIDADES / MODELOS DE DATOS
# ============================================================================

@dataclass
class ReportRecord:
    """Registro de un reporte generado"""
    report_type: str
    output_format: str
    delivery_method: str
    timestamp: str


# ============================================================================
# STRATEGY + TEMPLATE METHOD - Generadores de Reportes
# ============================================================================

class ReportGenerator(ABC):
    """
    Clase abstracta para generadores de reportes (Template Method Pattern)
    
    Define la estructura base que todos los reportes deben seguir.
    Principio DIP: Las clases de alto nivel dependen de esta abstracción.
    """
    
    def generate(self, data: Dict[str, Any]) -> str:
        """
        Template Method: Define el esqueleto del algoritmo
        """
        content = self._build_header()
        content += self._build_body(data)
        content += self._build_footer()
        return content
    
    def _build_header(self) -> str:
        """Construye el encabezado del reporte"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = "=" * 60 + "\n"
        header += f"           {self.get_title()}\n"
        header += "=" * 60 + "\n"
        header += f"Fecha de generación: {timestamp}\n\n"
        return header
    
    def _build_footer(self) -> str:
        """Construye el pie del reporte"""
        return "\n" + "=" * 60 + "\n"
    
    @abstractmethod
    def _build_body(self, data: Dict[str, Any]) -> str:
        """Construye el cuerpo del reporte - implementado por subclases"""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """Retorna el tipo de reporte"""
        pass
    
    @abstractmethod
    def get_title(self) -> str:
        """Retorna el título del reporte"""
        pass


class SalesReportGenerator(ReportGenerator):
    """
    Generador de reportes de ventas
    
    Principio SRP: Solo se encarga de generar contenido de ventas
    """
    
    def get_type(self) -> str:
        return "sales"
    
    def get_title(self) -> str:
        return "REPORTE DE VENTAS"
    
    def _build_body(self, data: Dict[str, Any]) -> str:
        sales = data.get('sales', [])
        period = data.get('period', 'No especificado')
        
        total_sales = sum(item['amount'] for item in sales)
        
        body = f"Total de ventas: ${total_sales:.2f}\n"
        body += f"Número de transacciones: {len(sales)}\n"
        body += f"Periodo: {period}\n\n"
        body += "Detalle de ventas:\n"
        body += "-" * 60 + "\n"
        
        for sale in sales:
            body += f"  • Producto: {sale['product']} - ${sale['amount']:.2f}\n"
        
        return body


class InventoryReportGenerator(ReportGenerator):
    """
    Generador de reportes de inventario
    
    Principio SRP: Solo se encarga de generar contenido de inventario
    """
    
    def get_type(self) -> str:
        return "inventory"
    
    def get_title(self) -> str:
        return "REPORTE DE INVENTARIO"
    
    def _build_body(self, data: Dict[str, Any]) -> str:
        items = data.get('items', [])
        
        total_items = sum(item['quantity'] for item in items)
        categories = len(set(item['category'] for item in items))
        
        body = f"Total de productos: {total_items}\n"
        body += f"Categorías: {categories}\n\n"
        body += "Inventario actual:\n"
        body += "-" * 60 + "\n"
        
        for item in items:
            body += f"  • {item['name']} ({item['category']}): {item['quantity']} unidades\n"
        
        return body


class FinancialReportGenerator(ReportGenerator):
    """
    Generador de reportes financieros
    
    Principio SRP: Solo se encarga de generar contenido financiero
    """
    
    def get_type(self) -> str:
        return "financial"
    
    def get_title(self) -> str:
        return "REPORTE FINANCIERO"
    
    def _build_body(self, data: Dict[str, Any]) -> str:
        income = data.get('income', 0)
        expenses = data.get('expenses', 0)
        balance = income - expenses
        
        body = f"Ingresos: ${income:.2f}\n"
        body += f"Gastos: ${expenses:.2f}\n"
        body += f"Balance: ${balance:.2f}\n"
        
        if balance > 0:
            body += "\n✅ Estado: POSITIVO\n"
        elif balance < 0:
            body += "\n⚠️  Estado: NEGATIVO\n"
        else:
            body += "\n➖ Estado: NEUTRO\n"
        
        return body


# ============================================================================
# STRATEGY PATTERN - Formateadores de Salida
# ============================================================================

class OutputFormatter(ABC):
    """
    Interfaz para formateadores de salida (Strategy Pattern)
    
    Principio ISP: Interfaz pequeña y específica
    """
    
    @abstractmethod
    def format(self, content: str) -> str:
        """Formatea el contenido del reporte"""
        pass
    
    @abstractmethod
    def get_format_type(self) -> str:
        """Retorna el tipo de formato"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Retorna la extensión del archivo"""
        pass


class PDFFormatter(OutputFormatter):
    """Formateador para PDF"""
    
    def get_format_type(self) -> str:
        return "pdf"
    
    def get_file_extension(self) -> str:
        return "pdf"
    
    def format(self, content: str) -> str:
        print("📄 Generando reporte en formato PDF...")
        return f"[PDF FORMAT]\n{content}\n[END PDF]"


class ExcelFormatter(OutputFormatter):
    """Formateador para Excel"""
    
    def get_format_type(self) -> str:
        return "excel"
    
    def get_file_extension(self) -> str:
        return "xlsx"
    
    def format(self, content: str) -> str:
        print("📊 Generando reporte en formato Excel...")
        return f"[EXCEL FORMAT]\n{content}\n[END EXCEL]"


class HTMLFormatter(OutputFormatter):
    """Formateador para HTML"""
    
    def get_format_type(self) -> str:
        return "html"
    
    def get_file_extension(self) -> str:
        return "html"
    
    def format(self, content: str) -> str:
        print("🌐 Generando reporte en formato HTML...")
        return f"<html><body><pre>{content}</pre></body></html>"


# ============================================================================
# STRATEGY PATTERN - Métodos de Entrega
# ============================================================================

class DeliveryMethod(ABC):
    """
    Interfaz para métodos de entrega (Strategy Pattern)
    
    Principio ISP: Interfaz pequeña y específica
    """
    
    @abstractmethod
    def deliver(self, content: str, report_type: str, file_extension: str) -> None:
        """Entrega el reporte"""
        pass
    
    @abstractmethod
    def get_method_type(self) -> str:
        """Retorna el tipo de método de entrega"""
        pass


class EmailDelivery(DeliveryMethod):
    """Entrega por correo electrónico"""
    
    def __init__(self, recipient: str = "admin@company.com"):
        self.recipient = recipient
    
    def get_method_type(self) -> str:
        return "email"
    
    def deliver(self, content: str, report_type: str, file_extension: str) -> None:
        print(f"📧 Enviando reporte por email...")
        print(f"   Destinatario: {self.recipient}")
        print(f"   Adjunto: report_{report_type}.{file_extension}")


class DownloadDelivery(DeliveryMethod):
    """Entrega por descarga directa"""
    
    def get_method_type(self) -> str:
        return "download"
    
    def deliver(self, content: str, report_type: str, file_extension: str) -> None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{report_type}_{timestamp}.{file_extension}"
        print(f"💾 Reporte disponible para descarga: {filename}")


class CloudDelivery(DeliveryMethod):
    """Entrega a la nube"""
    
    def __init__(self, cloud_url: str = "https://cloud.company.com/reports"):
        self.cloud_url = cloud_url
    
    def get_method_type(self) -> str:
        return "cloud"
    
    def deliver(self, content: str, report_type: str, file_extension: str) -> None:
        print(f"☁️  Subiendo reporte a la nube...")
        print(f"   URL: {self.cloud_url}/{report_type}.{file_extension}")


# ============================================================================
# FACTORY PATTERN - Fábricas
# ============================================================================

class ReportGeneratorFactory:
    """Fábrica de generadores de reportes"""
    
    _generators: Dict[str, type] = {}
    
    @classmethod
    def register(cls, report_type: str, generator_class: type):
        cls._generators[report_type] = generator_class
    
    @classmethod
    def create(cls, report_type: str) -> ReportGenerator:
        if report_type not in cls._generators:
            raise ValueError(f"Tipo de reporte desconocido: {report_type}")
        return cls._generators[report_type]()


class FormatterFactory:
    """Fábrica de formateadores"""
    
    _formatters: Dict[str, type] = {}
    
    @classmethod
    def register(cls, format_type: str, formatter_class: type):
        cls._formatters[format_type] = formatter_class
    
    @classmethod
    def create(cls, format_type: str) -> OutputFormatter:
        if format_type not in cls._formatters:
            raise ValueError(f"Formato desconocido: {format_type}")
        return cls._formatters[format_type]()


class DeliveryFactory:
    """Fábrica de métodos de entrega"""
    
    _methods: Dict[str, type] = {}
    
    @classmethod
    def register(cls, method_type: str, method_class: type):
        cls._methods[method_type] = method_class
    
    @classmethod
    def create(cls, method_type: str) -> DeliveryMethod:
        if method_type not in cls._methods:
            raise ValueError(f"Método de entrega desconocido: {method_type}")
        return cls._methods[method_type]()


# Registrar componentes
ReportGeneratorFactory.register("sales", SalesReportGenerator)
ReportGeneratorFactory.register("inventory", InventoryReportGenerator)
ReportGeneratorFactory.register("financial", FinancialReportGenerator)

FormatterFactory.register("pdf", PDFFormatter)
FormatterFactory.register("excel", ExcelFormatter)
FormatterFactory.register("html", HTMLFormatter)

DeliveryFactory.register("email", EmailDelivery)
DeliveryFactory.register("download", DownloadDelivery)
DeliveryFactory.register("cloud", CloudDelivery)


# ============================================================================
# SISTEMA PRINCIPAL
# ============================================================================

class ReportSystem:
    """
    Sistema principal de generación de reportes
    
    Principio SRP: Solo orquesta el proceso
    Principio DIP: Depende de abstracciones (factories)
    """
    
    def __init__(self):
        self._reports_generated: List[ReportRecord] = []
    
    def generate_report(
        self,
        report_type: str,
        data: Dict[str, Any],
        output_format: str,
        delivery_method: str
    ) -> str:
        """
        Genera un reporte completo
        
        Args:
            report_type: 'sales', 'inventory', 'financial'
            data: Datos para el reporte
            output_format: 'pdf', 'excel', 'html'
            delivery_method: 'email', 'download', 'cloud'
        """
        # Crear componentes usando factories
        generator = ReportGeneratorFactory.create(report_type)
        formatter = FormatterFactory.create(output_format)
        delivery = DeliveryFactory.create(delivery_method)
        
        # Generar contenido
        content = generator.generate(data)
        
        # Formatear
        formatted_content = formatter.format(content)
        
        # Entregar
        delivery.deliver(
            formatted_content,
            report_type,
            formatter.get_file_extension()
        )
        
        # Registrar
        self._reports_generated.append(ReportRecord(
            report_type=report_type,
            output_format=output_format,
            delivery_method=delivery_method,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        
        print(f"\n✅ Reporte generado exitosamente\n")
        print(formatted_content)
        print("\n" + "=" * 60 + "\n")
        
        return formatted_content
    
    def get_report_history(self) -> List[Dict]:
        """Retorna el historial de reportes generados"""
        return [
            {
                "type": r.report_type,
                "format": r.output_format,
                "delivery": r.delivery_method,
                "timestamp": r.timestamp
            }
            for r in self._reports_generated
        ]


# ============================================================================
# FACADE PATTERN - Interfaz Simplificada
# ============================================================================

class ReportFacade:
    """
    Fachada para el sistema de reportes (Facade Pattern - Estructural)
    
    Proporciona una interfaz simplificada para generar reportes comunes.
    Oculta la complejidad de las factories y configuraciones.
    
    Principio: Simplifica el uso del sistema para el cliente
    """
    
    def __init__(self):
        self._system = ReportSystem()
    
    def generate_sales_report_pdf_email(self, period: str, sales: List[Dict]) -> str:
        """Atajo: Reporte de ventas en PDF enviado por email"""
        data = {'period': period, 'sales': sales}
        return self._system.generate_report('sales', data, 'pdf', 'email')
    
    def generate_inventory_report_excel_download(self, items: List[Dict]) -> str:
        """Atajo: Reporte de inventario en Excel para descarga"""
        data = {'items': items}
        return self._system.generate_report('inventory', data, 'excel', 'download')
    
    def generate_financial_report_html_cloud(self, income: float, expenses: float) -> str:
        """Atajo: Reporte financiero en HTML subido a la nube"""
        data = {'income': income, 'expenses': expenses}
        return self._system.generate_report('financial', data, 'html', 'cloud')
    
    def generate_custom_report(
        self,
        report_type: str,
        data: Dict[str, Any],
        output_format: str,
        delivery: str
    ) -> str:
        """Genera un reporte personalizado"""
        return self._system.generate_report(report_type, data, output_format, delivery)
    
    def get_available_options(self) -> Dict[str, List[str]]:
        """Retorna todas las opciones disponibles"""
        return {
            "report_types": list(ReportGeneratorFactory._generators.keys()),
            "formats": list(FormatterFactory._formatters.keys()),
            "delivery_methods": list(DeliveryFactory._methods.keys())
        }
    
    def get_history(self) -> List[Dict]:
        """Obtiene el historial de reportes"""
        return self._system.get_report_history()


# ============================================================================
# EJEMPLO DE EXTENSIBILIDAD (OCP)
# ============================================================================

class AuditReportGenerator(ReportGenerator):
    """
    Generador de reportes de auditoría - Ejemplo de extensibilidad
    
    Demuestra OCP: Se agregó sin modificar código existente
    """
    
    def get_type(self) -> str:
        return "audit"
    
    def get_title(self) -> str:
        return "REPORTE DE AUDITORÍA"
    
    def _build_body(self, data: Dict[str, Any]) -> str:
        actions = data.get('actions', [])
        
        body = f"Total de acciones auditadas: {len(actions)}\n\n"
        body += "Registro de actividades:\n"
        body += "-" * 60 + "\n"
        
        for action in actions:
            body += f"  • [{action['timestamp']}] {action['user']}: {action['action']}\n"
        
        return body


# Registrar nuevo generador (sin modificar código existente)
ReportGeneratorFactory.register("audit", AuditReportGenerator)


# ============================================================================
# CÓDIGO DE PRUEBA
# ============================================================================

if __name__ == "__main__":
    
    # ========================================================================
    # DEMOSTRACIÓN 1: Uso del Facade (interfaz simplificada)
    # ========================================================================
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 1: USO DEL FACADE (PATRÓN ESTRUCTURAL)")
    print("Interfaz simplificada con métodos predefinidos")
    print("="*60)
    
    facade = ReportFacade()
    
    # Mostrar opciones disponibles
    print("\nOpciones disponibles en el sistema:")
    print(json.dumps(facade.get_available_options(), indent=2))
    print()
    
    # Reporte de ventas (atajo)
    sales_data = [
        {'product': 'Laptop HP', 'amount': 899.99},
        {'product': 'Mouse Logitech', 'amount': 25.50},
        {'product': 'Teclado Mecánico', 'amount': 120.00},
        {'product': 'Monitor LG 24"', 'amount': 199.99}
    ]
    facade.generate_sales_report_pdf_email('Enero 2024', sales_data)
    
    # Reporte de inventario (atajo)
    inventory_items = [
        {'name': 'Laptop HP', 'category': 'Computadoras', 'quantity': 15},
        {'name': 'Mouse Logitech', 'category': 'Accesorios', 'quantity': 50},
        {'name': 'Teclado Mecánico', 'category': 'Accesorios', 'quantity': 30},
        {'name': 'Monitor LG', 'category': 'Pantallas', 'quantity': 20}
    ]
    facade.generate_inventory_report_excel_download(inventory_items)
    
    # Reporte financiero (atajo)
    facade.generate_financial_report_html_cloud(50000.00, 32000.00)
    
    # ========================================================================
    # DEMOSTRACIÓN 2: Uso directo del sistema (más control)
    # ========================================================================
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 2: USO DIRECTO DEL SISTEMA")
    print("Para casos que requieren más control")
    print("="*60)
    
    system = ReportSystem()
    
    financial_data = {'income': 75000.00, 'expenses': 45000.00}
    system.generate_report('financial', financial_data, 'pdf', 'download')
    
    # ========================================================================
    # DEMOSTRACIÓN 3: Extensibilidad (OCP)
    # ========================================================================
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 3: EXTENSIBILIDAD (OCP)")
    print("Nuevo tipo 'audit' agregado sin modificar código existente")
    print("="*60)
    
    audit_data = {
        'actions': [
            {'timestamp': '2024-01-15 10:30', 'user': 'admin', 'action': 'Login exitoso'},
            {'timestamp': '2024-01-15 10:35', 'user': 'admin', 'action': 'Modificó usuario #123'},
            {'timestamp': '2024-01-15 11:00', 'user': 'admin', 'action': 'Exportó reporte de ventas'}
        ]
    }
    facade.generate_custom_report('audit', audit_data, 'pdf', 'email')
    
    # ========================================================================
    # HISTORIAL
    # ========================================================================
    print("\n" + "="*60)
    print("HISTORIAL DE REPORTES GENERADOS")
    print("="*60)
    print(json.dumps(facade.get_history(), indent=2))