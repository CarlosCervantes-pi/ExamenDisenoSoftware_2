classDiagram
    direction TB
    
    %% ==================== DATACLASS ====================
    class ReportRecord {
        <<dataclass>>
        +str report_type
        +str output_format
        +str delivery_method
        +str timestamp
    }
    
    %% ==================== TEMPLATE METHOD - GENERATORS ====================
    class ReportGenerator {
        <<abstract>>
        +generate(data: Dict) str
        #_build_header() str
        #_build_body(data: Dict) str*
        #_build_footer() str
        +get_type() str*
        +get_title() str*
    }
    
    class SalesReportGenerator {
        +get_type() str
        +get_title() str
        #_build_body(data: Dict) str
        -_calculate_total_sales(sales: List) float
    }
    
    class InventoryReportGenerator {
        +get_type() str
        +get_title() str
        #_build_body(data: Dict) str
        -_count_categories(items: List) int
    }
    
    class FinancialReportGenerator {
        +get_type() str
        +get_title() str
        #_build_body(data: Dict) str
        -_calculate_balance(income: float, expenses: float) float
    }
    
    class AuditReportGenerator {
        +get_type() str
        +get_title() str
        #_build_body(data: Dict) str
    }
    
    %% ==================== STRATEGY - FORMATTERS ====================
    class OutputFormatter {
        <<abstract>>
        +format(content: str) str*
        +get_format_type() str*
        +get_file_extension() str*
    }
    
    class PDFFormatter {
        +format(content: str) str
        +get_format_type() str
        +get_file_extension() str
    }
    
    class ExcelFormatter {
        +format(content: str) str
        +get_format_type() str
        +get_file_extension() str
    }
    
    class HTMLFormatter {
        +format(content: str) str
        +get_format_type() str
        +get_file_extension() str
    }
    
    %% ==================== STRATEGY - DELIVERY ====================
    class DeliveryMethod {
        <<abstract>>
        +deliver(content: str, report_type: str, file_ext: str) void*
        +get_method_type() str*
    }
    
    class EmailDelivery {
        -str recipient
        +__init__(recipient: str)
        +deliver(content: str, report_type: str, file_ext: str) void
        +get_method_type() str
    }
    
    class DownloadDelivery {
        +deliver(content: str, report_type: str, file_ext: str) void
        +get_method_type() str
        -_generate_filename(report_type: str, ext: str) str
    }
    
    class CloudDelivery {
        -str cloud_url
        +__init__(cloud_url: str)
        +deliver(content: str, report_type: str, file_ext: str) void
        +get_method_type() str
    }
    
    %% ==================== FACTORIES ====================
    class ReportGeneratorFactory {
        <<factory>>
        -Dict~str, type~ _generators$
        +register(report_type: str, generator_class: type)$ void
        +create(report_type: str)$ ReportGenerator
    }
    
    class FormatterFactory {
        <<factory>>
        -Dict~str, type~ _formatters$
        +register(format_type: str, formatter_class: type)$ void
        +create(format_type: str)$ OutputFormatter
    }
    
    class DeliveryFactory {
        <<factory>>
        -Dict~str, type~ _methods$
        +register(method_type: str, method_class: type)$ void
        +create(method_type: str)$ DeliveryMethod
    }
    
    %% ==================== CORE SYSTEM ====================
    class ReportSystem {
        -List~ReportRecord~ _reports_generated
        +__init__() void
        +generate_report(report_type: str, data: Dict, output_format: str, delivery_method: str) str
        +get_report_history() List~Dict~
    }
    
    %% ==================== FACADE ====================
    class ReportFacade {
        <<facade>>
        -ReportSystem _system
        +__init__() void
        +generate_sales_report_pdf_email(period: str, sales: List) str
        +generate_inventory_report_excel_download(items: List) str
        +generate_financial_report_html_cloud(income: float, expenses: float) str
        +generate_custom_report(report_type: str, data: Dict, format: str, delivery: str) str
        +get_available_options() Dict
        +get_history() List~Dict~
    }
    
    %% ==================== INHERITANCE - GENERATORS ====================
    ReportGenerator <|-- SalesReportGenerator : extends
    ReportGenerator <|-- InventoryReportGenerator : extends
    ReportGenerator <|-- FinancialReportGenerator : extends
    ReportGenerator <|-- AuditReportGenerator : extends
    
    %% ==================== INHERITANCE - FORMATTERS ====================
    OutputFormatter <|-- PDFFormatter : extends
    OutputFormatter <|-- ExcelFormatter : extends
    OutputFormatter <|-- HTMLFormatter : extends
    
    %% ==================== INHERITANCE - DELIVERY ====================
    DeliveryMethod <|-- EmailDelivery : extends
    DeliveryMethod <|-- DownloadDelivery : extends
    DeliveryMethod <|-- CloudDelivery : extends
    
    %% ==================== FACTORY ASSOCIATIONS ====================
    ReportGeneratorFactory ..> ReportGenerator : creates
    FormatterFactory ..> OutputFormatter : creates
    DeliveryFactory ..> DeliveryMethod : creates
    
    %% ==================== SYSTEM ASSOCIATIONS ====================
    ReportSystem --> ReportGeneratorFactory : uses
    ReportSystem --> FormatterFactory : uses
    ReportSystem --> DeliveryFactory : uses
    ReportSystem *-- ReportRecord : stores
    
    %% ==================== FACADE ASSOCIATIONS ====================
    ReportFacade *-- ReportSystem : delegates to