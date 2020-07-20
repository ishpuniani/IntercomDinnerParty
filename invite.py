import json
import sys
import traceback
from collections import Set
from urllib.error import URLError

from customer import Customer
from readers import FileReader, HttpReader
from utils import Utils


class Invite:

    def __init__(self, input_file_url, input_file_path, distance_threshold, intercom_latitude, intercom_longitude,
                 output_file_path):
        self.input_file_url = input_file_url
        self.input_file_path = input_file_path
        self.distance_threshold = distance_threshold
        self.intercom_latitude = intercom_latitude
        self.intercom_longitude = intercom_longitude
        self.output_file_path = output_file_path

    def create_customer_objects(self, customers_list):
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
        filtered_customers = []
        for customer in customers:
            customer_distance = Utils.great_circle_distance(customer.get_coords(),
                                                            (self.intercom_latitude, self.intercom_longitude))
            if customer_distance <= self.distance_threshold:
                filtered_customers.append(customer)
        filtered_customers = sorted(filtered_customers, key=lambda c: c.id)
        return filtered_customers

    def invite_customers(self, customers):
        """
        This function can be used to send out email invites to customers satisfying the condition!
        For now, sticking to the task and writing them out to a file.
        :param customers: List of customers to be invited
        :return: None
        """

        # Writing JSON to text files
        customers_json = [json.dumps(customer.__dict__)+'\n' for customer in customers]
        file_path = self.output_file_path
        Utils.write_to_file(file_path, customers_json)

        # Writing to CSV
        customers_csv = ["user_id,name,latitude,longitude\n"]
        for customer in customers:
            customers_csv.append(customer.csv_row())
        Utils.write_to_file(file_path.replace('txt','csv'), customers_csv)

    def execute(self):
        try:
            # Reading from File on local system
            customers_list = FileReader.read(self.input_file_path)

            # Reading from file over http
            # customers_list = HttpReader.read(self.input_file_url)

            # Creating customer objects from json
            customers = self.create_customer_objects(customers_list)

            # Filtering customers on the basis of the distance threshold
            filtered_customers = self.filter_customers_by_distance(customers)

            # Inviting customer
            self.invite_customers(filtered_customers)

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
