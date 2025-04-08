from .base_processor import BankProcessor
import re
from tabulate import tabulate
from bank_processors.base_processor import BankProcessor
import PyPDF2
import pdfplumber


class ScotiabankProcessor(BankProcessor):

    """
    Specific processor to handle extraction and processing of Scotiabank bank statements.
    """
    def extract_data(self):
        """Extract raw data from the Scotiabank PDF file."""
        print(f"Processing PDF file: {self.pdf_file}")
        
        try:
            with pdfplumber.open(self.pdf_file) as pdf:
                num_pages = len(pdf.pages)
                print(f"Number of pages in the PDF: {num_pages}")
                
                extracted_text = []
                capturing = False 
                #Scotiabank estados de cuenta tienen 3 paginas al final con informacion, se eliminan
                for i, page in enumerate(pdf.pages[:-3]):
                    # Recortar las páginas según las especificaciones
                    if i ==0:
                        page = page.crop((0, page.height * 0.75, page.width, page.height * 0.94))                  
                    text = page.extract_text()
                    try:
                        print(f"Processing page {i + 1}...")
                        
                        table_settings = {
                        "vertical_strategy": "lines",
                                                    #Condicional por si la pagina 1 corta el movimiento
                        "horizontal_strategy": "lines" if i>0 else "text",
                        "explicit_vertical_lines": [],
                        "explicit_horizontal_lines": [],
                        "snap_tolerance": 10,
                        "snap_x_tolerance": 1,
                        "snap_y_tolerance": 5,
                        "join_tolerance": 1,
                        "join_x_tolerance": 2,
                        "join_y_tolerance": 15,
                        "edge_min_length": 5,
                        "min_words_vertical": 0,  
                        "min_words_horizontal": 0,  
                        "text_keep_blank_chars": False,
                        "text_tolerance": 4,
                        "text_x_tolerance": 4,
                        "text_y_tolerance": 15,
                        "intersection_tolerance": 1,
                        "intersection_x_tolerance": 10,
                        "intersection_y_tolerance": 5,
                       
                    }
                        # Extraer tabla
                        table = page.extract_table(table_settings)
                        if table:
                            print(f"Table found on page {i + 1}")
                            #print(table)
                      
                            # im = page.to_image()
                            # im.reset().debug_tablefinder(table_settings)
                            # im.save(f"page_{i + 1}_debug.png")
                            
                            #print(tabulate(table))
                            # Patrones de fecha y hora
                       
                            # Patrones de fecha y cifra
                            date_pattern = r'^\d{1,2}\s[A-Z]{3}'   # Fecha en formato 25-SEP-2024 (inicio de la fila)
                            number_pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?$'  # Cifra como 311,821.97 o 339237.74 (al final de la fila)

                            # Filtrar filas con los patrones
                            for row in table:
                                row_str = ' '.join([str(cell) for cell in row])  # Unir los elementos de la fila en una cadena
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

        date_pattern = r'^\d{1,2}\s[A-Z]{3}'

        processed_data = []
        
        for line in raw_data:
            processed_data.append([line[0], "CONCEPTO", line[-3], line[-2], line[-1]])          
           
        return processed_data
    
        
