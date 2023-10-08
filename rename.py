import os
import io
import re

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

foldername='target_folder'


def pdf_to_text(path):
    '''
    Converts the pdf to a string
    each line is seperated by \n
    '''
    with open(path, 'rb') as fp:
        rsrcmgr = PDFResourceManager()
        outfp = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
    text = outfp.getvalue()
    return text


def get_the_name(filename):
    '''
    Searches on the pdf to find the
    file name
    '''

    pdf_text=pdf_to_text(filename)
    for line in pdf_text.split('\n'):
        if re.search('The Name: ', line):
            return str(int(line.replace('The Name: ','')))


def get_all_files_in_folder(dir,extension):
    '''
    Returns all files in the directory
    '''

    all_files = []
    for dirpath, dirnames, filenames in os.walk(dir+"/"):
        all_files+=[os.path.join(dirpath, f) for f in filenames if f.endswith(extension)]
    return all_files


if __name__=='__main__':
    for filename in get_all_files_in_folder("./"+foldername,".pdf"):
        the_name=get_the_name(filename)
        print(the_name)
        new_name = "./"+foldername+"/"+the_name+'.pdf'
        os.rename(filename, new_name)

