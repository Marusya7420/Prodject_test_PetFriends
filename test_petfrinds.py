from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и созраняем полученный ответ с кодом статуса в status, а текст ответа в result

    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Получаем api ключ и сохраняем в переменную auth_key.
    Запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets  """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pet(name='Милашка', animal_type='Метис',age='1', pet_photo = 'images/kittens.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet_info(name='Милашка', animal_type='котенок', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
# Домашнее задание - 10 дополнительных тестов
#1
"""Проверяем добавление питомца с валидными данными без фото"""
def test_post_add_new_pet_simple(name='Rino', animal_type='хомяк обыкновенный', age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# 2
""""Проверяем возможность добавить питомца с невалидными данными"""
def test_post_add_new_pet_simple_invalid_data(name=5, animal_type='', age='two'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# 3
"""Добавление питомца с заполненным только одним именем, негативный сценарий"""
def test_post_add_new_pet_simple_null_data(name="Муся", animal_type=None, age=None):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200

# 4
"""Проверяем добавление только фото питомца с валидными данными"""
def test_post_add_photo_of_pet(pet_photo = 'images/Rino.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] == pet_photo

# 5
""""Авторизация с невалидными данными (email, password)"""
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и созраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

# 6
"""Проверяем возможность получить список всех питомцев с невалидным email"""
def test_get_all_pets_with_invalid_key(filter=''):
    _, auth_key = pf.get_api_key(invalid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
# 7
"""Проверяем возможность получить с помощью  параметра filter - 'my_pets' список своих питомцев"""
def test_get_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# 8
"""Проверяем возможность удаления питомца с некорректным индексом"""
def test_unsuccessful_delete_self_pet():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
   # Берём id несуществующего питомца в списке и отправляем запрос на удаление
    pet_id = my_pets['pets'][13]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
   # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    if pet_id in len(my_pets['pets']):
        assert status == 200
    else:
        raise Exception("There is no pet with such index")

# 9
"""Проверяем возможность добавить питомца без передачи одного аргумента - фото"""
def test_post_add_invalid_new_pet(name='Милашка', animal_type='Метис',age=1, pet_photo=None):
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert 'Error' in result

# 10
"""Добвать фото питомца в другом формате"""
def test_post_add_photo_of_pet(pet_photo = 'images/KITTENS1.bmp'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status != 200
    assert 'Error' in result
