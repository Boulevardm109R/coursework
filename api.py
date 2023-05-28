import requests


class HttpException(Exception):

    def __init__(self, status, message=''):
        self.status = status
        self.message = message

    def __str__(self):
        return f'http error: {self.status}\n{self.message}'


class ApiBasic:

    host = ''

    def _send_request(self, http_method, uri_path, params=None, json=None, response_type=None):
        response = requests.request(http_method, f'{self.host}/{uri_path}', params=params, json=json)  # отправл¤ем запрос
        if response.status_code >= 400:
            # если с сервера приходит ошибка, выбрасываем исключение
            raise HttpException(response.status_code, response.text)
        if response_type == 'json':
            response = response.json()
        return response


class VkAPI(ApiBasic):
    host = 'https://api.vk.com/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def get_user(self, user_id):
        return self._send_request(
            http_method='GET',
            uri_path='method/users.get',
            params={
                'user_id': user_id,
                'name_case': 'gen',
                **self.params
            },
            response_type='json'
        )


class YandexAPI(ApiBasic):
    host = 'https://cloud-api.yandex.net/v1/disk'