import json
import sys
import traceback
from urllib.error import URLError

from customer import Customer
from readers import FileReader, HttpReader
from utils import Utils


class Invite:

    def __init__(self, distance_threshold, intercom_latitude, intercom_longitude, output_file_path,
                 input_file_path=None, input_file_url=None):
        self.distance_threshold = distance_threshold
        self.intercom_latitude = intercom_latitude
        self.intercom_longitude = intercom_longitude
        self.output_file_path = output_file_path
        if input_file_url is not None:
            self.input_path = input_file_url
        elif input_file_path is not None:
            self.input_path = input_file_path
        else:
            raise AttributeError('Input file not provided')

    def create_customer_objects(self, customers_list):
        """
        Creating customer objects from a list of json
        :param customers_list: json list of all customers
        :return: list of customer objects
        """
        customers = []
        id_set = set()
        for customer_json in customers_list:
            customer = Customer.json_decoder(customer_json)
            if customer.id not in id_set:
                # Not adding duplicate customers from the list by ID.
                id_set.add(customer.id)
                customers.append(customer)
        return customers

    def filter_customers_by_distance(self, customers):
        """
        Filter customers for the list on the basis of the threshold distance
        :param customers: list of customers to be filtered
        :return: a filtered and sorted list of customers on the basis of distance
        """
        filtered_customers = []
        for customer in customers:
            customer_distance = Utils.great_circle_distance(customer.get_coords(),
                                                            (self.intercom_latitude, self.intercom_longitude))
            if customer_distance <= self.distance_threshold:
                filtered_customers.append(customer)

        filtered_customers = sorted(filtered_customers, key=lambda c: c.id)
        return filtered_customers

    def send_invites(self, customers):
        """
        This function can be used to send out email invites to customers satisfying the condition!
        For now, sticking to the task and writing them out to a file.
        :param customers: List of customers to be invited
        :return: None
        """

        if self.output_file_path.lower() == 'print':
            # for debugging and tests
            print(customers)
        else:
            # Writing JSON to text files
            customers_json = [json.dumps(customer.__dict__) for customer in customers]
            file_path = self.output_file_path
            Utils.write_to_file(file_path, customers_json)

            # Writing to CSV
            customers_csv = ["user_id,name,latitude,longitude"]
            for customer in customers:
                customers_csv.append(customer.csv_row())
            Utils.write_to_file(file_path.replace('txt','csv'), customers_csv)

    def invite_customers(self):
        try:

            if 'http' in self.input_path:
                # Reading from file over http
                customers_list = HttpReader.read(self.input_path)
            else:
                # Reading from File on local system
                customers_list = FileReader.read(self.input_path)

            # Creating customer objects from json
            customers = self.create_customer_objects(customers_list)

            # Filtering customers on the basis of the distance threshold
            filtered_customers = self.filter_customers_by_distance(customers)

            # Inviting customer
            self.send_invites(filtered_customers)

            return filtered_customers

        except KeyError as ke:
            print("KeyError encountered")
            traceback.print_exc(file=sys.stdout)
        except ValueError as ve:
            print("ValueError encounterd")
            traceback.print_exc(file=sys.stdout)
        except URLError as ue:
            print("Error getting data from url")
            traceback.print_exc(file=sys.stdout)
        except FileNotFoundError as fe:
            print("Unable to find file")
            traceback.print_exc(file=sys.stdout)
        except Exception as e:
            print("Some error occurred")
            traceback.print_exc(file=sys.stdout)
