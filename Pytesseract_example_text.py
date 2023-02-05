#Использование pytesseract для распознавания текста с картинок
#https://waksoft.susu.ru/2021/05/18/kak-s-pomoshhyu-python-raspoznat-tekst-v-izobrazheniyah/

#pip install pytesseract

#1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

#2. Note the tesseract path from the installation. Default installation path at the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

#3. pip install pytesseract

#4. Set the tesseract path in the script before calling image_to_string:

#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe' fdg

#pip install python-docx - для сохранение в ворд

#Текст очень хреновый, скрин с телефона и пропечатан плохо

import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import fitz
import docx

def take_image(current_page, xref, pl,mydoc):
    if (pl==0):
        image = cv2.imread("images\\page%s-%s.png" % (current_page, xref))
    else:
        image = cv2.imread("D:\\PYTHON\\Programms\\CompleteSetOfBlades2021\\IMGTest.jpg")
    # cv2.imshow('page%s'% (current_page), cv2.resize(image, (600,800), interpolation = cv2.INTER_AREA))
    # cv2.waitKey(0)
    # или вы можете использовать подушку
    # image = Image.open("test.png")
    # получаем строку
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    string = pytesseract.image_to_string(image, lang='rus')
    # печатаем
    print(string)
    mydoc.add_paragraph(string)




#Пытаемся взять данные с чертежа
if (1==0):
    print('****************')
    word ="3"
    print('Берем слово %s' % (word))
    take_image(1, 1, 1,word)

pdf_document = fitz.open("pdf\\slaids.pdf")
#pdf_document = fitz.open("pdf\\Text_handwritten.pdf")
index = 0
mydoc = docx.Document()
print(len(pdf_document))
for current_page in range(len(pdf_document)):
    # for image in pdf_document.getPageImageList(current_page):
    for image in pdf_document.get_page_images(current_page):
        #if (index == 2):
        xref = image[0]
        pix = fitz.Pixmap(pdf_document, xref)
        print('****************')
        print('Страница %s' % (current_page))
        # читать изображение с помощью OpenCV
        take_image(current_page, xref, 0,mydoc)
        index+=1

#mydoc.save("pdf\\Text_handwritten.docx")
mydoc.save("pdf\\slaids.docx")
