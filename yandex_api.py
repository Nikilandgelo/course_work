import requests

def upload_photos(oauth_token, id_user, photos_album, photos_upload, amount = 5):
    headers = {
        "Authorization": "OAuth " + oauth_token
    }
    folder_params = {
        "path": "Пользователь " + id_user + " " + photos_album + " photos"
    }
    yandex_folder = requests.put("https://cloud-api.yandex.net/v1/disk/resources", params = folder_params
                                                                                 , headers = headers)
    if yandex_folder.status_code in range(202, 409):
        print("\nПри загрузке на ЯД что то пошло не так, проверьте корректность токена и попробуйте еще раз.")
        return
           
    if len(photos_upload) < amount:
        amount = len(photos_upload)

    for index, photo in enumerate(photos_upload[:amount]):
        photo_params = {
            "path": "Пользователь " + id_user + " " + photos_album + " photos/" + list(photo)[0] + ".jpg",
            "overwrite": "true"
        }
        yandex_file = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", params = photo_params
                                                                                          , headers = headers)
        link_for_upload = yandex_file.json().get("href")

        photo_bytes = requests.get(photo.get(list(photo)[0]).get("url")).content
        yandex_upload = requests.put(link_for_upload, files = {"file": photo_bytes})
        print(f"{index + 1}/{amount} загружено")