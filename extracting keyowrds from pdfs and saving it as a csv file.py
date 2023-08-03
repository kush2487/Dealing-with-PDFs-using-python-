

import re
import csv
from pdftextract import XPdf
import PyPDF2


pdf_files = 'output1.pdf'#put your pdf name which is in the same directory 
keywords = ["Campaign ID:","Taxable Amount","Total Amount","Page Number"]#put your keywords that you want ot extract



def extract_infos(file, i, keywords:list):

    pdf = XPdf(file)
    txt = pdf.to_text(just_one=i ,keep_layout=True)
    row = []
    # getting the keywords information


    for keyword in keywords:
        # search for the keyword
        pattern = "{} (.+)\r".format(keyword) # extracting the wanted info
        regex = re.compile(pattern, flags=re.I| re.M)
        m = regex.search(txt)
        if m is not None:
            m = m.groups()[0].strip(' /\r') # strip unwanted space and characters
        row.append(m)
    row.append(i+1)
    return row


def main(files:list, fname:str, headers:list):
    """extract the wanted info from a bunch of pdf files and save them as csv file"""
    with open(fname, "w") as wf:
        writer = csv.writer(wf)
        writer.writerow(headers)

        with open(files, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)

                for page_num in range(num_pages):
                    #it fetches the keyword according to the page and returns it as a header 
                    row = extract_infos(files, page_num ,headers)
                    writer.writerow(row)


    print("[DONE]", "writed {} rows to {}.".format(num_pages, fname))

main(pdf_files, "stocks23.csv", keywords)