import abc


class BankProcessor(abc.ABC):
    """
    Base class for processing bank statemets.
    All specific bank processors inherit from this
    """
    def __init__(self, pdf_file: str):
        self.pdf_file = pdf_file
        
        
    @abc.abstractmethod
    def extract_data(self):
        """Extract raw data from the PDF."""
        pass

    @abc.abstractmethod
    def preprocess_data(self, raw_data):
        """Preprocess the extracted data into a standard format."""
        pass

    def process(self):
        """Complete processing pipeline."""
        raw_data = self.extract_data()
        cleaned_data = self.preprocess_data(raw_data)
        return cleaned_data