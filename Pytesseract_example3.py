#Использование pytesseract для распознавания текста и цифр с картинок
#Простые чертежи с PDF

import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import fitz
import numpy as np

def take_image(image, current_page, xref, pl,target_word, target_word_number):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    string = pytesseract.image_to_string(image, lang='rus')
    # печатаем
    print(string)

    # чтобы нарисовать сделаем копию изображения
    image_copy = image.copy()
    # слово для поиска
    #target_word = "по"
    # получить все данные из изображения
    data = pytesseract.image_to_data(image, lang='rus', output_type=pytesseract.Output.DICT)

    # Повышенние резкости изображения:
    #enhancer1 = ImageEnhance.Sharpness(image)
    #factor1 = 0.01  # чем меньше, тем больше резкость
    #im_s_1 = enhancer1.enhance(factor1)

    text_number = pytesseract.image_to_string(image, config='--psm 6 -c tessedit_char_whitelist=0123456789,. ')
    print("********")
    print(text_number)
    data_number = pytesseract.image_to_data(image, config='--psm 6 -c tessedit_char_whitelist=0123456789,. ', output_type=pytesseract.Output.DICT)
    #text = pytesseract.image_to_string(image, config='--psm 6 -c tessedit_char_whitelist=0123456789,. ').split('\n')
    #print(text)

    # получить все вхождения нужного слова
    word_occurences = [i for i, word in enumerate(data["text"]) if word.lower() == target_word] #word.lower() == target_word
    word_occurences_numbers = [i for i, word in enumerate(data_number["text"]) if word.lower() == target_word_number] #word.lower() == target_word_number
    # Теперь нарисуем вокруг найденного слова рамку
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
    for occ in word_occurences_numbers:
        # извлекаем ширину, высоту, верхнюю и левую позицию для обнаруженного слова
        w = data_number["width"][occ]
        h = data_number["height"][occ]
        l = data_number["left"][occ]
        t = data_number["top"][occ]
        # определяем все точки окружающей рамки
        p1 = (l, t)
        p2 = (l + w, t)
        p3 = (l + w, t + h)
        p4 = (l, t + h)
        # рисуем 4 линии (прямоугольник)
        image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 255), thickness=2)
        image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 255), thickness=2)
        image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 255), thickness=2)
        image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 255), thickness=2)
    # Сохраним полученное изображение
    if (pl == 0):
        plt.imsave("images\\saveChest %s.tiff" % (current_page), image_copy)

    plt.imshow(image_copy)
    plt.show()


#Пытаемся взять данные с чертежа
pdf_document = fitz.open("pdf\\Чертежи_шестерни0001.pdf")
index = 0
pl = 0
for current_page, page in enumerate(pdf_document.pages()):
        zoom = 1
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        imgData = pix.tobytes()
        #imgData = pix.getPNGData()
        # save image from opencv
        nparr = np.frombuffer(imgData, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if (pl == 1):
            word = "нв"
            word_number = "8"

        elif (pl == 0):
            word = "е"
            word_number = "2"

        print('****************')
        print('Страница %s' % (current_page))
        take_image(img, current_page, 1, pl, word, word_number)



