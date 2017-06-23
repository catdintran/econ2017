After submitting a .pdf to econ2017, the pdfFile will be processed to .txt by xpdf program.

Task 1: to extract countryName from .txt to save as fileName
In order to do that, we need to read the file and extract chunk of text to analyze.
  1.1: get first 10 lines from .txt
    # we know that countryName usually appears in the first 10 lines of the .txt
    # to extract first 10 lines of .txt:
    with open(textFile, 'rb') as f:
        lines = f.readlines()
        limit = 10
        text = ''
        for i, l in enumerate(lines): 
            text = text + ' ' + l.replace('\n', '').replace('\xad',' ')       
            if i == limit:
                break
  1.2: 
