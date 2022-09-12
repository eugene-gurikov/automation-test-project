import requests


class ApiCall:

    def get_item_id(self, api_url, cookie, expected_items_amount):
        body = {'cookie': cookie, 'flag': 'true'}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(f"{api_url}viewcart", json=body, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            items_list = response_json['Items']
            assert len(items_list) == expected_items_amount
            return response_json['Items'][0]['prod_id']
        else:
            AssertionError(f"Api call failed: {response.status_code} error")

    def get_item_details(self, api_url, item_id):
        body = {'id': item_id}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(f"{api_url}view", json=body, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            AssertionError(f"Api call failed: {response.status_code} error")