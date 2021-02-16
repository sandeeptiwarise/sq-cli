import requests
import contextlib
import OpenSSL.crypto
import os
import requests
import ssl
import tempfile

class CQCAdapter:
    CQC_SANDBOX_URL = "https://dev.ironbridgeapi.com/api"

    def __init__(self):
        pass


    @classmethod
    @contextlib.contextmanager
    def pfx_to_pem(cls, pfx_path, pfx_password):
        ''' Decrypts the .pfx file to be used with requests. '''
        with tempfile.NamedTemporaryFile(suffix='.pem') as t_pem:
            f_pem = open(t_pem.name, 'wb')
            pfx = open(pfx_path, 'rb').read()
            p12 = OpenSSL.crypto.load_pkcs12(pfx, pfx_password)
            f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
            f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
            ca = p12.get_ca_certificates()
            if ca is not None:
                for cert in ca:
                    f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
            f_pem.close()
            yield t_pem.name

    @classmethod
    def testConnection(cls):
        with CQCAdapter.pfx_to_pem('/Users/mayanksharma/Downloads/CQC_testing_cert.pfx', '$Friday345') as cert:
        # requests.post(url, cert=cert, data=payload)
            res = requests.get(f"{CQCAdapter.CQC_SANDBOX_URL}/testconnection", cert=cert)
            print(res.text)

    @classmethod
    def getInfo(cls):
        with CQCAdapter.pfx_to_pem('/Users/mayanksharma/Downloads/CQC_testing_cert.pfx', '$Friday345') as cert:
            # requests.post(url, cert=cert, data=payload)
            res = requests.get(f"{CQCAdapter.CQC_SANDBOX_URL}/getinfo", cert=cert)
            print(res.text)

    @classmethod
    def setupClient(cls):
        with CQCAdapter.pfx_to_pem('/Users/mayanksharma/Downloads/CQC_testing_cert.pfx', '$Friday345') as cert:
            # requests.post(url, cert=cert, data=payload)
            res = requests.get(f"{CQCAdapter.CQC_SANDBOX_URL}/setupclient", cert=cert)
            print(res.text)

    @classmethod
    def demoWorkflow(cls):
        key = fetch_key()
        key = base64.decode(key)
        # how to decapsulate the key??
        decapsulated_key = decapsulate_key(key)
