from glob import glob
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation
import os
from tqdm.auto import tqdm 
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('path', type=str, help='Path to directory containing PDFs')
    args = parser.parse_args()
    return args

def main(root_dir: str):
    pdfs = glob(os.path.join(root_dir, '*.pdf'))
    os.makedirs(os.path.join(root_dir,'out'), exist_ok=True)
    for pdf in tqdm(pdfs):
        fname = os.path.basename(pdf)
        reader = PdfReader(open(pdf,'rb'))

        writer = PdfWriter()

        for p in range(len(reader.pages)//4):
            pages = []
            
            for i in range(4):
                try:
                    pages.append(reader.pages[p*4+i])
                except IndexError:
                    pages.append(PageObject.create_blank_page(None, pages[0].mediabox.width, pages[0].mediabox.height))
                
            translated_page = PageObject.create_blank_page(None, pages[0].mediabox.width*2, pages[0].mediabox.height*2)

            for i in range(4):
                pages[i].add_text("Page %d" % (p*4+i+1), 10, 10)
                pages[i].add_transformation(Transformation().scale(1).translate((i%2)*pages[i].mediabox.width, (1-i//2)*pages[i].mediabox.height), expand=True)
                
                translated_page.merge_page(pages[i])
            
            writer.add_page(translated_page)

        with open(os.path.join('out/', fname), 'wb') as f:
            writer.write(f)


if __name__ == '__main__':
    args = parse_args()
    main(args.path)