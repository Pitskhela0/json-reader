from .exporter import JSONExporter, XMLExporter, Exporter
from ..constants.errors_messages import ErrorMessages


class ExporterFactory:
    """Factory to create appropriate exporter instances"""

    _exporters = {
        "json": JSONExporter,
        "xml": XMLExporter,
    }

    @classmethod
    def create_exporter(cls, format_type: str) -> Exporter:
        """Create and return an exporter for the specified format"""
        format_type = format_type.lower()

        if format_type not in cls._exporters:
            raise ValueError(ErrorMessages.UNSUPPORTED_FORMAT.format(format_type))

        return cls._exporters[format_type]()

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        """Get list of supported export formats"""
        return list(cls._exporters.keys())
