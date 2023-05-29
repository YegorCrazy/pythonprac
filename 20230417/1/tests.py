import unittest
import socket
import multiprocessing
import sys
import subprocess
import time
import cowsay
import os
import signal

class TestServerMVP(unittest.TestCase):

    def GetServerResponse(self, msg):
        self.socket.sendall((msg + '\n').encode())
        response = self.socket.recv(1024).decode().strip()
        return response

    def ListenToSocket(self):
        return self.socket.recv(1024).decode().rstrip()

    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(
            target=lambda: subprocess.run([sys.executable,
                                           '-m', 'moodserver']))
        cls.proc.start()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        os.kill(cls.proc.pid, signal.SIGINT)
        cls.proc.terminate()

    def setUp(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 1337))
        login_resp = self.GetServerResponse('login testuser')
        assert login_resp == 'ok'

    def tearDown(self):
        self.socket.close()

    def testMovePlayer(self):
        resp = self.GetServerResponse('move 1 0')
        assert resp == 'Moved to (1, 0)'

    def testAddMonster(self):
        resp = self.GetServerResponse('addmon default aaa 1 0 100')
        assert resp == 'Added monster to (1, 0) saying aaa'
        resp = self.GetServerResponse('move 1 0')
        assert resp == 'Moved to (1, 0)'
        resp = self.ListenToSocket()
        assert resp == cowsay.cowsay('aaa')

    def testAttackMonster(self):
        resp = self.GetServerResponse('addmon default aaa 0 1 100')
        assert resp == 'Added monster to (0, 1) saying aaa'
        resp = self.GetServerResponse('move 0 1')
        assert resp == 'Moved to (0, 1)'
        resp = self.ListenToSocket()
        assert resp == cowsay.cowsay('aaa')
        resp = self.GetServerResponse('attack default axe')
        assert resp == 'Attacked default with axe, damage 20 hp'
