
from bank_processors.base_processor import BankProcessor
from bank_processors.bbva_processor import BBVAProcessor
from bank_processors.banbajio_processor import BanbajioProcessor
from bank_processors.banregio_processor import BanregioProcessor
from bank_processors.banorte_processor import BanorteProcessor
from bank_processors.banamex_processor import BanamexProccesor
class BankProcessorFactory:
    """
    A factory class to dynamically instantiate the correct bank processor.
    """
    processors = {
        "bbva": BBVAProcessor,
        "banbajio" : BanbajioProcessor,
        "banregio": BanregioProcessor,
        "banorte": BanorteProcessor,
        "banamex": BanamexProccesor
    }

    @staticmethod
    def get_processor(bank_name: str, pdf_file: str) -> BankProcessor:
        """
        Returns an instance of the appropriate bank processor based on the bank name.
        
        :param bank_name: The name of the bank (e.g., "BankA", "BankB")
        :param pdf_file: Path to the PDF file to be processed
        :return: An instance of the appropriate BankProcessor subclass
        """
        processor_class = BankProcessorFactory.processors.get(bank_name)
        if not processor_class:
            raise ValueError(f"No processor available for bank: {bank_name}")
        
        return processor_class(pdf_file)
