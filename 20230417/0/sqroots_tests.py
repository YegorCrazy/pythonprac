import unittest
import sqroots
import sqroots_client
import multiprocessing
import socket
import time
import asyncio

class TestSqroots(unittest.TestCase):

    def test_0(self):
        self.assertEqual(sqroots.sqroots("1 2 3"), "")

    def test_1(self):
        self.assertEqual(sqroots.sqroots("1 -2 1"), "1.0")

    def test_2(self):
        self.assertEqual(sqroots.sqroots("1 -3 2"), "1.0 2.0")

    def test_exception_1(self):
        with self.assertRaises(ValueError):
            sqroots.sqroots("1 1")

    def test_exception_2(self):
        with self.assertRaises(ZeroDivisionError):
            sqroots.sqroots("0 1 1")


class TestSqrootsServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=sqroots.serve)
        cls.proc.start()
        time.sleep(1)
        cls.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.s.connect(('localhost', 1337))

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.s.close()

    def test_server_0(self):
        self.assertEqual(sqroots_client.sqrootnet("1 2 3", self.s), "")

    def test_server_1(self):
        self.assertEqual(sqroots_client.sqrootnet("1 -2 1", self.s), "1.0")

    def test_server_2(self):
        self.assertEqual(sqroots_client.sqrootnet("1 -3 2", self.s), "1.0 2.0")

    def test_server_exception_1(self):
        self.assertEqual(sqroots_client.sqrootnet("1 2", self.s), "")

    def test_server_exception_2(self):
        self.assertEqual(sqroots_client.sqrootnet("0 1 1", self.s), "")

