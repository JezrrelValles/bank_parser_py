import re
from tabulate import tabulate
from bank_processors.base_processor import BankProcessor
import PyPDF2
import pdfplumber

class BanregioProcessor(BankProcessor):
    """
    Specific processor to handle extraction and processing of BBVA bank statements.
    """
    def extract_data(self):
        """Extract raw data from the Banregio PDF file."""
        print(f"Processing PDF file: {self.pdf_file}")
        
        try:
            with pdfplumber.open(self.pdf_file) as pdf:
                num_pages = len(pdf.pages)
                print(f"Number of pages in the PDF: {num_pages}")
                
                extracted_text = []
                capturing = False 
                
                for i, page in enumerate(pdf.pages):
                    #Quitar el encabezado de las paginas
                    #page = page.crop((0,page.height * 0.04 ,page.width, page.height))
                  
                    try:
                        print(f"Text on page {i + 1}:")
                     
                        text = page.extract_text()
                        print(text)
             
                        if text:  
                            lines = text.split("\n")
                            table_settings = {
                            "vertical_strategy": "text",  
                            "horizontal_strategy": "text", 
                            "explicit_vertical_lines": [],
                            "explicit_horizontal_lines": [],
                            "snap_tolerance": 3,
                            "snap_x_tolerance": 3,
                            "snap_y_tolerance": 3,
                            "join_tolerance": 3,
                            "join_x_tolerance": 3,
                            "join_y_tolerance": 3,
                            "edge_min_length": 3,
                            "min_words_vertical": 3,
                            "min_words_horizontal": 1,
                            "intersection_tolerance": 3,
                            "intersection_x_tolerance": 3,
                            "intersection_y_tolerance": 3,
                            "text_tolerance": 4,
                            "text_x_tolerance": 4,
                            "text_y_tolerance": 5,
                            }

                            table = page.extract_table(table_settings)
                            
                            if table:
                    
                                date_pattern = r'^\d{2}.*(?:\d{1,3}(?:,\d{3})*(?:\.\d{2})?)$'
                                
                                for row in table:
                                    row_str = ' '.join(row)  # Convertir la fila en una cadena de texto
                                    print(f"Row: {row_str}")  # Depuración: ver la línea completa
                                    
                                    # Aplicar la expresión regular sobre la cadena unificada (row_str)
                                    if re.search(date_pattern, row_str):  
                                        extracted_text.append(row) 
                                        print(f"ROW INCLUDE: {row_str}")  # Mostrar la línea que coincide con el patrón
                                    else:
                                        print(f"NO MATCH: {row_str}") 
 
                    except Exception as e:
                        print(f"Error extracting text from page {i + 1}: {e}")
                        
                

    
                return extracted_text
            
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ""
    def preprocess_data(self, raw_data):
        """Preprocess extracted data into a standardized format."""
        print("Preprocessing data...")

     
        return raw_data