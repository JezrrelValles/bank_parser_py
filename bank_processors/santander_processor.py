from .base_processor import BankProcessor
import re
from tabulate import tabulate
from bank_processors.base_processor import BankProcessor
import PyPDF2
import pdfplumber


class SantanderProcessor(BankProcessor):

    """
    Specific processor to handle extraction and processing of Santander bank statements.
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
                    # Recortar las páginas según las especificaciones
                    if i + 1 > 1:
                        if i + 1 == 2:
                            # Si es la página 2, quitar 55% de la parte superior
                            page = page.crop((0, page.height * 0.30, page.width, page.height * 0.94))
                        else:
                            # Si es cualquier página después de la 1, quitar 15% de la parte superior
                            page = page.crop((0, page.height * 0.15, page.width, page.height * 0.94))
                    else:
                        # Para la primera página, solo quitar 6% de la parte inferior
                        page = page.crop((0, 0, page.width, page.height * 0.94))
                    text = page.extract_text()
                    try:
                        print(f"Processing page {i + 1}...")
                        
                        table_settings = {
                        "vertical_strategy": "lines",
                        "horizontal_strategy": "text",
                        "explicit_vertical_lines": [],
                        "explicit_horizontal_lines": [],
                        "snap_tolerance": 10,
                        "snap_x_tolerance": 5,
                        "snap_y_tolerance": 5,
                        "join_tolerance": 15,
                        "join_x_tolerance": 2,
                        "join_y_tolerance": 15,
                        "edge_min_length": 3,
                        "min_words_vertical": 2,  
                        "min_words_horizontal": 2,  
                        "text_keep_blank_chars": True,
                        "text_tolerance": 3,
                        "text_x_tolerance": 4,
                        "text_y_tolerance": 4,
                        "intersection_tolerance": 5,
                        "intersection_x_tolerance": 5,
                        "intersection_y_tolerance": 15,
                    }
                        # Extraer tabla
                        table = page.extract_table(table_settings)
                        if table:
                            # print(f"Table found on page {i + 1}")
                            # print(table)
                            # # if i+1 ==3:
                            # im = page.to_image()
                            # im.reset().debug_tablefinder(table_settings)
                            # im.save(f"page_{i + 1}_debug.png")
                            
                            #print(tabulate(table))
                            # Patrones de fecha y hora
                       
                            # Patrones de fecha y cifra
                            date_pattern = r'^\d{2}-[A-Z]{3}-\d{4}'  # Fecha en formato 25-SEP-2024 (inicio de la fila)
                            number_pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?$'  # Cifra como 311,821.97 o 339237.74 (al final de la fila)

                            # Filtrar filas con los patrones
                            for row in table:
                                print(row)
                                row_str = ' '.join([str(cell) for cell in row])  # Unir los elementos de la fila en una cadena
                                print(row_str)
                                # Verificar si la fila contiene una fecha al inicio y una cifra al final
                                if re.match(date_pattern, row_str) and re.search(number_pattern, row_str):
                                    extracted_text.append(row)
                                    print(f"Matched date and number row: {row}")

                           
                        else:
                            print(f"No table found on page {i + 1}")

                    except Exception as e:
                        print(f"Error processing page {i + 1}: {e}")
                        
            return extracted_text

        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return []

    def preprocess_data(self, raw_data):
        """Preprocess extracted data into a standardized format."""
        print("Preprocessing data...")

        return raw_data
    
        
