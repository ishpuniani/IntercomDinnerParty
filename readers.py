import urllib.request
from abc import abstractmethod
from urllib.error import URLError, HTTPError


class Reader:
    @classmethod
    @abstractmethod
    def read(cls, path):
        raise NotImplementedError


class HttpReader(Reader):
    @classmethod
    def read(cls, path):
        """
        Read text file from URL
        :param path: URL of the file
        :return: an array of lines present in the file
        """
        try:
            data = []
            f = urllib.request.urlopen(path)
            if f.getcode() < 400:
                for line in f.readlines():
                    data.append(line.strip().decode('utf-8'))
                return data
            else:
                raise URLError("Request failed: " + path)
        except HTTPError as he:
            print("HTTPError reading file from URL: " + path)
            raise he
        except URLError as ue:
            print("URLError reading file from URL: " + path)
            raise ue


class FileReader(Reader):
    @classmethod
    def read(cls, path):
        """
        Read text files present on the disk
        :param path: path of the text file on disk
        :return: an array of lines present in the file
        """
        try:
            content = []
            f = open(path, 'r')
            for line in f.readlines():
                content.append(line.strip())
            return content
        except FileNotFoundError as fe:
            print("File not found: " + path)
            raise fe
