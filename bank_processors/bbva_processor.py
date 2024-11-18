import re
from tabulate import tabulate
from bank_processors.base_processor import BankProcessor
import PyPDF2
import pdfplumber

class BBVAProcessor(BankProcessor):
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
                    #OPERACION empieza en la coordenada 475, entonces se recorta
                    #Se le quita 6% de abajo (informacion del banco no util)
                    if  i+1 > 1:
                        page = page.crop((0,page.height * 0.15 ,475, page.height*0.94))
                    else:
                        page = page.crop((0, 0 ,475, page.height*0.94))
                    try:
                        print(f"Text on page {i + 1}:")
                        text = page.extract_text()
             
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
                                date_pattern = r'\d{2}/[A-Z]{3}' 
                                
                                for row in table:
                                    row_str = ' '.join(row)

                                    if re.search(date_pattern, row_str):  
                                        extracted_text.append(row) 
                                        print(row)  
                                    
 
                            if "Detalle de Movimientos Realizados" in lines:
                                
                                capturing = True
                                start_idx = lines.index("Detalle de Movimientos Realizados") + 1
                                lines = lines[start_idx:]
                                print(f"Found 'Detalle de Movimientos Realizados' on page {i + 1}")
                        
                            if capturing:       
                                #extracted_text.extend(lines)

                                if "Total de Movimientos" in lines:
                                    capturing = False
                                    #end_idx = lines.index("Total de Movimientos")
                                    #extracted_text = extracted_text[:-len(lines) + end_idx]
                                    print(f"Found 'Total de Movimientos' on page {i + 1}")
                                    break

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
    
        
