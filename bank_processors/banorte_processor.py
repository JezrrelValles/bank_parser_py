import re
from tabulate import tabulate
from bank_processors.base_processor import BankProcessor
import PyPDF2
import pdfplumber

class BanorteProcessor(BankProcessor):
    """
    Specific processor to handle extraction and processing of Banorte bank statements.
    """
    def extract_data(self):
        """Extract raw data from the Banorte PDF file."""
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
             
                        if text:  
                            lines = text.split("\n")
                            table_settings = {
                            "vertical_strategy": "text",  
                            "horizontal_strategy": "lines", 
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
                    
                                date_pattern = r'\d{1,2}\s*-\s*[A-Z]{3}\s*-\s*\d{1,2}'
                                
                                for row in table:
                                    row_str = ' '.join(row)
         
                                    if re.search(date_pattern, row_str):  
                                        extracted_text.append(row) 
                                    else:
                                        print("No funciono:", row)
            
 
                            # if "DETALLE DE MOVIMIENTOS (PESOS)▼" in lines:
                                
                            #     capturing = True
                            #     start_idx = lines.index("DETALLE DE MOVIMIENTOS (PESOS)") + 1
                            #     lines = lines[start_idx:]
                            #     print(f"DETALLE DE MOVIMIENTOS (PESOS)' on page {i + 1}")
                        
                            # if capturing:       
                            #     #extracted_text.extend(lines)

                            #     if "OTROS▼" in lines or "INVERSION ENLACE NEGOCIOS" in lines:
                            #         capturing = False
                            #         #end_idx = lines.index("Total de Movimientos")
                            #         #extracted_text = extracted_text[:-len(lines) + end_idx]
                            #         print(f"Found 'OTROS▼' on page {i + 1}")
                            #         break

                    except Exception as e:
                        print(f"Error extracting text from page {i + 1}: {e}")
                        
                

    
                return extracted_text
            
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ""
        
    def preprocess_data(self, raw_data):
        """Preprocess extracted data into a standardized format."""
        print("Preprocessing data...")

        cleaned_data = []

        # Patrón para la fecha (formato de fecha tipo 06-MAY-24)
        date_pattern = r'\d{2}-[A-Z]{3}-\d{2}'  # Ejemplo: 06-MAY-24

        for row in raw_data:
         

            # Limpiar cada fila, eliminando todo lo que esté después de un salto de línea
            cleaned_row = []
            for element in row:
                # Si encuentra un salto de línea en el elemento, se elimina todo después
                if '\n' in element:
                    # Eliminar lo que sigue después del salto de línea
                    cleaned_row.append(element.split('\n')[0])
                else:
                    cleaned_row.append(element)

            # Volver a unir los elementos de la fila limpia en una sola cadena
            cleaned_row_combined = ' '.join(cleaned_row)

            # Buscar la fecha en la cadena combinada
            date_match = re.search(date_pattern, cleaned_row_combined)
            
            if date_match:
                # Extraer la fecha si se encuentra
                date = date_match.group(0)

                # Encontrar los últimos 3 valores relevantes (monto)
                last_three = cleaned_row[-3:] if len(cleaned_row) >= 3 else cleaned_row + [""] * (3 - len(cleaned_row))
                
                # Construir la fila procesada con la fecha y los últimos 3 elementos
                final_row = [date] + last_three
            else:
                # Si no se encuentra la fecha, mantener la fila original (limpia)
                final_row = cleaned_row
            
            # Añadir la fila procesada o la original a la lista de resultados
            cleaned_data.append(final_row)

        return cleaned_data