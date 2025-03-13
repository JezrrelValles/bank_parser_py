from setuptools import setup, find_packages

setup(
    name="bank_parser_py",
    version="0.1.0",
    author="Adrian Rivas",
    description="Preprocessing python program for invoices",
    url="https://github.com/AdrianRvzz/bank_parser_py",
    packages=find_packages(),
    install_requires=[
        'cffi==1.17.1',
        'charset-normalizer==3.4.0',
        'cryptography==43.0.3',
        'pdfminer.six==20231228',
        'pdfplumber==0.11.4',
        'pillow==11.0.0',
        'pycparser==2.22',
        'PyPDF2==3.0.1',
        'pypdfium2==4.30.0',
        'setuptools==75.5.0',
        'tabulate==0.9.0',
    ],
)
