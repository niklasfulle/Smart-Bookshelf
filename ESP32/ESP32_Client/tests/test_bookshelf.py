"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from utils.json_data_reader import json_data_reader
from hardware.bookshelf import bookshelf


class TestBookshelf:
    """
    -
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40000 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50000}}'
    bookshelf_config: str = '{"name": "bookshelf_name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'

    def test_Bookshelf1(self):
        """
        -
        """
        ip = json_data_reader(self.client_config, ["connection", "ip"], 2)
        bookshelf_name = json_data_reader(self.bookshelf_config, ["name"], 2)
        shelving_units = json_data_reader(self.bookshelf_config, ["shelving_units"], 2)

        Bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

        assert Bookshelf_object.name == "bookshelf_name1"
        assert Bookshelf_object.ip == "127.0.0.1"
        assert len(Bookshelf_object.ledstripes) == 8
        assert Bookshelf_object.ledstripes[0].order == 1
        assert Bookshelf_object.ledstripes[0].length == 50
        assert Bookshelf_object.ledstripes[7].order == 8
        assert Bookshelf_object.ledstripes[7].length == 50
