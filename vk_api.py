import requests
import datetime

vk_app_token = 'vk1.a.nTqlcDC95ZcRoPbWiZVXyDs8Kikr98kk65OM_lRjmLU4ABpD6PE22YyWu370yjSjZGPH-YYCPCvlpnuUvo6xFKQnS_MHQacsl6fpDoZmHAiRDVRwaYNqdNvWCL-SrIY7UWrwLxlASrB7eavJvmBpgiju9ZEukFHyz5wOAA6ZiNE1MUtyEZRA2r-USrHZX12vxKHDkMvvbneKPKuI6wEEMQ'

def get_photos(user_id, album_id):  
    photos_params = {"access_token": vk_app_token,
    "owner_id": user_id,
    "album_id": album_id,
    "extended": 1,
    "v": "5.154"
    }
    vk_photos = requests.get("https://api.vk.com/method/photos.get", params = photos_params)
    if list(vk_photos.json())[0] == "error":
        print("\nПри получении фотографий что то пошло не так, проверьте правильность номера страницы или наличие фотографий в выбранном альбоме.")
        return
    
    list_photos = []
    for photo in vk_photos.json().get("response").get("items"):
        photo.get("sizes").sort(key = lambda x: x["width"], reverse = True)

        for sorted_photo in list_photos:
            if str(photo.get("likes").get("count")) in sorted_photo:
                unix_to_date = str(datetime.datetime.fromtimestamp(photo.get("date"))).replace("-", ".").replace(":", ".")
                list_photos.append({str(photo.get("likes").get("count")) + " " + unix_to_date : photo.get("sizes")[0]})
                break
        else:
            list_photos.append({str(photo.get("likes").get("count")) : photo.get("sizes")[0]})
            
    return list_photos