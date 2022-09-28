#Использование pytesseract для распознавания текста и цифр с картинок
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

def take_image(current_page, xref, pl,target_word, target_word_number):
    if (pl==0):
        image = cv2.imread("D:\\PYTHON\\Programms\\CompleteSetOfBlades2021\\ImagesForDetection\\PartOfProst.tif")
    else:
        image = cv2.imread("D:\\PYTHON\\Programms\\CompleteSetOfBlades2021\\ImagesForDetection\\C_2020_2.jpg")
    # cv2.imshow('page%s'% (current_page), cv2.resize(image, (600,800), interpolation = cv2.INTER_AREA))
    # cv2.waitKey(0)
    # или вы можете использовать подушку
    # image = Image.open("test.png")
    # получаем строку
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
        plt.imsave("D:\\PYTHON\\Programms\\CompleteSetOfBlades2021\\ImagesForDetection\\PartOfProstDetection.tiff", image_copy)
    else:
        plt.imsave("D:\\PYTHON\\Programms\\CompleteSetOfBlades2021\\ImagesForDetection\\IMGTestDetection1.jpg", image_copy)
    plt.imshow(image_copy)
    plt.show()


#Пытаемся взять данные с чертежа
print('****************')
pl = 0
if (pl==1):
    word ="менее"
    word_number= "6"

elif (pl==0):
    word ="после"
    word_number= "4"
print('Берем слово %s' % (word))
take_image(1, 1, 0, word, word_number)


