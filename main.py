from bank_processors.bank_processor_factory import BankProcessorFactory
import os 


def main():
    bank_name = "bbva"
    
    # Build the file path dynamically based on the bank name
    file_path = os.path.join("files", bank_name.lower(), f"estado_de_cuenta_{bank_name.lower()}.pdf")
    
    if not os.path.exists(file_path):
        print(f"File for {bank_name} not found: {file_path}")
        return
  
    try:
        # Get the correct processor for the bank
        processor = BankProcessorFactory.get_processor(bank_name, file_path)
        
        # Process the file
        processed_data = processor.process()  
        
        # Define the path for the movements.txt file within the same folder as the PDF
        folder_path = os.path.dirname(file_path)
        
        
        
        
        movements_file_path = os.path.join(folder_path, "movements.txt")          
        with open(movements_file_path, 'w') as file:
            # Write each item in processed_data on a new line
            for item in processed_data:
                file.write(f"{item}\n")  # Write each item followed by a newline


    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()