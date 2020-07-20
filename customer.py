import json


class Customer:
    @classmethod
    def json_decoder(cls, cust_json):
        try:
            cust_dict = json.loads(cust_json)
            user_id = int(cust_dict['user_id'])
            name = cust_dict['name']
            latitude = float(cust_dict['latitude'])
            longitude = float(cust_dict['longitude'])
            return Customer(user_id, name, latitude, longitude)
        except KeyError as ke:
            print("KeyError creating customer instance: " + cust_json)
            raise ke

    def __init__(self, user_id, name, latitude, longitude):
        self.id = user_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def get_coords(self):
        return (self.latitude, self.longitude)

    def get_name(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.latitude == other.latitude and self.longitude == other.longitude

    def __str__(self) -> str:
        return "user_id: {0}, name: {1}, latitude: {2}, longitude: {3}".format(self.id, self.name, self.latitude, self.longitude)

    def csv_row(self) -> str:
        return '{},{},{},{}\n'.format(self.id, self.name, self.latitude, self.longitude)
