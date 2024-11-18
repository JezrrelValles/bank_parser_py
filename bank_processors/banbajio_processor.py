import re
from tabulate import tabulate
from bank_processors.base_processor import BankProcessor
import PyPDF2
import pdfplumber

class BanbajioProcessor(BankProcessor):
    """
    Specific processor to handle extraction and processing of BBVA bank statements.
    """
    def extract_data(self):
        """Extract raw data from the BBVA PDF file."""
        print(f"Processing PDF file: {self.pdf_file}")
        
        try:
            with pdfplumber.open(self.pdf_file) as pdf:
                num_pages = len(pdf.pages)
                print(f"Number of pages in the PDF: {num_pages}")
                
                extracted_text = []
                capturing = False 
                
                for i, page in enumerate(pdf.pages):
                    try:
                        print(f"Text on page {i + 1}:")
                        text = page.extract_text()
                        
                        if text:  
                            lines = text.split("\n")

                            # Iterar sobre las líneas del texto
                            for line in lines:
                                # Mostrar depuración detallada con caracteres invisibles
                                print("Buscando la linea ",line)
        
                                # Verificar si la línea empieza con 'DETALLE DE LA CUENTA:'
                                if line.startswith("DETALLE DE LA CUENTA:"):
                                    capturing = True
                                    print(f"Found 'DETALLE DE LA CUENTA:' on page {i + 1}")
                                    continue  # Saltar a la siguiente línea para iniciar captura

                                # Si se está capturando, verificar el patrón de fecha
                                if capturing:
                                    date_pattern = r'^\d{1,2}\s[A-Z]{3}'  
                                    
                                    if re.match(date_pattern, line):  #
                                        extracted_text.append(line)
                                        print(f"Captured line: {line}")
                                        
                                            
                                if "TOTAL DE MOVIMIENTOS" in line:
                                    capturing = False
                                    print(f"Found 'TOTAL DE MOVIMIENTOS' on page {i + 1}")
                                    break  
                        
                    except Exception as e:
                        print(f"Error extracting text from page {i + 1}: {e}")
            print("Lineas ", extracted_text)
            return extracted_text
        except Exception as e:
            print(f"Error opening PDF file: {e}")
            return []

    def preprocess_data(self, raw_data):
        """Preprocess extracted data into a standardized format."""
        print("Preprocessing data...")

        date_pattern = r'^\d{1,2}\s[A-Z]{3}'

        processed_data = []
        
        for line in raw_data:
            if re.match(date_pattern, line):
                line = re.sub(r'(\d{1,2}\s[A-Z]{3}).*?\$', r'\1   $', line)
                processed_data.append(line)
            else:
                processed_data.append(line)
        
        return processed_data
    
        
