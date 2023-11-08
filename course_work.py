import vk_api
import yandex_api
import json
import os
import copy

def create_json():
    copy_collector = copy.deepcopy(collector_photos)
    for photo in copy_collector:
        photo["file_name"] = list(photo)[0] + ".jpg"
        photo["size"] = photo.get(list(photo)[0]).get("type")
        del photo[(list(photo)[0])]
    with open(f"Пользователь_{id_answer}_{album_answer}_photos.json", "w") as file:
        json.dump(copy_collector, file, indent = 1)

    return os.path.join(os.getcwd(), f"Пользователь_{id_answer}_{album_answer}_photos.json")

while True:
    id_answer = input("\nВведите номер страницы Вконтакте откуда нужно скачать фотографии:\n")
    if id_answer.isdigit() == False:
        print("\nПохоже вы ввели не цифровой id страницы, чтобы узнать номер страницы воспользуйтесь, например: https://regvk.com/id/")
        continue

    album_answer = input("\nОткуда вы хотите сохранить фото?\n1 - со стены\n2 - с профиля\n3 - сохраненные фотографии (открытые)\n")
    if album_answer == '1':
        album_answer = "wall"
    elif album_answer == '2':
        album_answer = "profile"
    elif album_answer == '3':
        album_answer = "saved"
    else:
        print("\nНеккоректный ввод, попробуем еще раз...")
        continue
    
    print("\nПолучение фотографий из Вконтакте...")
    collector_photos = vk_api.get_photos(id_answer, album_answer)
    if collector_photos == None:
        continue

    print("Информация по полученным файлам доступна здесь - " + create_json())

    yandex_token = input("\nВведите ваш токен с Полигона Яндекс.Диска:\n")
    amount_photos = input("\nКоличество фотографий, которое вы хотите загрузить:\n")
    if amount_photos.isdigit() == False or int(amount_photos) == 0 or int(amount_photos) > len(collector_photos):
        print("\nНеккоректный ввод, будет загружено 5 (по умолчанию) фотографий или меньше если общее количество меньше 5")
        print("\nЗагрузка фотографий на ЯД, подождите...")
        yandex_api.upload_photos(yandex_token, id_answer, album_answer, collector_photos)
    else:
        print("\nЗагрузка фотографий на ЯД, подождите...")
        yandex_api.upload_photos(yandex_token, id_answer, album_answer, collector_photos, int(amount_photos))
    
    last_question = input("\nЕсли вы хотите завершить деятельность программы нажмите Q, если вы хотите повторить введите что угодно.\n")
    if last_question.upper() == "Q":
        print("\nЗавершение программы...")
        break