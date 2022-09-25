#Использование pytesseract для распознавания текста с картинок
#https://waksoft.susu.ru/2021/05/18/kak-s-pomoshhyu-python-raspoznat-tekst-v-izobrazheniyah/

#pip install pytesseract

#1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

#2. Note the tesseract path from the installation. Default installation path at the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

#3. pip install pytesseract

#4. Set the tesseract path in the script before calling image_to_string:

#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe' fdg

#Удивительно, не правда ли? И это еще не все!
# Вы можете передать параметр lang функциям image_to_string()
# или image_to_data(), чтобы упростить распознавание текста на других языках,
# а не только на английском. Можно использовать функцию image_to_boxes(),
# которая распознает символы и границы их местоположения, пожалуйста,
# обратитесь к официальной документации и доступным языкам для получения дополнительной информации.

import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import fitz

pdf_document = fitz.open("pdf\\PDFOfImage.pdf")
for current_page in range(len(pdf_document)):
    # for image in pdf_document.getPageImageList(current_page):
    for image in pdf_document.get_page_images(current_page):

        xref = image[0]
        pix = fitz.Pixmap(pdf_document, xref)
        print('****************')
        print('Страница %s' % (current_page))
        # читать изображение с помощью OpenCV
        image = cv2.imread("images\\page%s-%s.png"% (current_page, xref))
        #cv2.imshow('page%s'% (current_page), cv2.resize(image, (600,800), interpolation = cv2.INTER_AREA))
        #cv2.waitKey(0)
        # или вы можете использовать подушку
        # image = Image.open("test.png")
        # получаем строку
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        string = pytesseract.image_to_string(image, lang = 'rus')
        # печатаем
        print(string)

        # чтобы нарисовать сделаем копию изображения
        image_copy = image.copy()
        # слово для поиска
        target_word = "по"
        # получить все данные из изображения
        data = pytesseract.image_to_data(image, lang = 'rus', output_type=pytesseract.Output.DICT)

        # получить все вхождения нужного слова
        word_occurences = [i for i, word in enumerate(data["text"]) if word.lower() == target_word]

        #Теперь нарисуем вокруг найденного слова рамку
        for occ in word_occurences:
            # извлекаем ширину, высоту, верхнюю и левую позицию для обнаруженного слова
            w = data["width"][occ]
            h = data["height"][occ]
            l = data["left"][occ]
            t = data["top"][occ]
            # определяем все точки окружающей рамки
            p1 = (l, t)
            p2 = (l + w, t)
            p3 = (l + w, t + h)
            p4 = (l, t + h)
            # рисуем 4 линии (прямоугольник)
            image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
            image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
            image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
            image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)
        #Сохраним полученное изображение
        plt.imsave("images\\all_customer_words.png%s-%s.png"% (current_page, xref), image_copy)
        plt.imshow(image_copy)
        plt.show()