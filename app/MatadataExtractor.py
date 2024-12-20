import os
import pefile


class MetadataExtractor:
    @staticmethod
    def extract(file_path):
        """
        Extract metadata from the given file.
        Includes file path, size, type, architecture, number of imports and exports.
        """
        metadata = {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "file_type": "dll" if file_path.endswith(".dll") else "exe",
            "architecture": "x64" if "x64" in file_path else "x32",
            "number_of_imports": 0,
            "number_of_exports": 0
        }

        try:
            pe = pefile.PE(file_path)

            # Number of imports
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                metadata["number_of_imports"] = sum(
                    len(entry.imports) for entry in pe.DIRECTORY_ENTRY_IMPORT
                )

            # Number of exports
            if hasattr(pe,
                       'DIRECTORY_ENTRY_EXPORT') and pe.DIRECTORY_ENTRY_EXPORT:
                metadata["number_of_exports"] = len(
                    pe.DIRECTORY_ENTRY_EXPORT.symbols)

        except Exception as e:
            print(f"Failed to parse {file_path}: {e}")

        return metadata
