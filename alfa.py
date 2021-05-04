import functools
import inspect
import grpc
import grpc._channel
import etcd3.etcdrpc as etcdrpc
import etcd3.watch as watch
import sqlite3
def _handle_errors(f):
    if inspect.isgeneratorfunction(f):
        def handler(*args, **kwargs):
            try:
                for data in f(*args, **kwargs):
                    yield data
            except grpc.RpcError as exc:
                _translate_exception(exc)
    else:
        def handler(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except grpc.RpcError as exc:
                _translate_exception(exc)

    return functools.wraps(f)(handler)
class Etcd3Client(object):
    def __init__(self, host='localhost', port=2379,
                 ca_cert=None, cert_key=None, cert_cert=None, timeout=None,
                 user=None, password=None, grpc_options=None):

        self._url = '{host}:{port}'.format(host=host, port=port)
        self.metadata = None

        cert_params = [c is not None for c in (cert_cert, cert_key)]
        if ca_cert is not None:
            if all(cert_params):
                credentials = self._get_secure_creds(
                    ca_cert,
                    cert_key,
                    cert_cert
                )
                self.uses_secure_channel = True
                self.channel = grpc.secure_channel(self._url, credentials,
                                                   options=grpc_options)
            elif any(cert_params):
                # some of the cert parameters are set
                raise ValueError(
                    'to use a secure channel ca_cert is required by itself, '
                    'or cert_cert and cert_key must both be specified.')
            else:
                credentials = self._get_secure_creds(ca_cert, None, None)
                self.uses_secure_channel = True
                self.channel = grpc.secure_channel(self._url, credentials,
                                                   options=grpc_options)
        else:
            self.uses_secure_channel = False
            self.channel = grpc.insecure_channel(self._url,
                                                 options=grpc_options)

        self.timeout = timeout
        self.call_credentials = None

        cred_params = [c is not None for c in (user, password)]

        if all(cred_params):
            self.auth_stub = etcdrpc.AuthStub(self.channel)
            auth_request = etcdrpc.AuthenticateRequest(
                name=user,
                password=password
            )

            resp = self.auth_stub.Authenticate(auth_request, self.timeout)
            self.metadata = (('token', resp.token),)
            self.call_credentials = grpc.metadata_call_credentials(
                EtcdTokenCallCredentials(resp.token))

        elif any(cred_params):
            raise Exception(
                'if using authentication credentials both user and password '
                'must be specified.'
            )

        self.kvstub = etcdrpc.KVStub(self.channel)
        self.watcher = watch.Watcher(
            etcdrpc.WatchStub(self.channel),
            timeout=self.timeout,
            call_credentials=self.call_credentials,
            metadata=self.metadata
        )
        self.clusterstub = etcdrpc.ClusterStub(self.channel)
        self.leasestub = etcdrpc.LeaseStub(self.channel)
        self.maintenancestub = etcdrpc.MaintenanceStub(self.channel)
        self.transactions = Transactions()
    @_handle_errors
    def snapshot(self, file_obj):
        """Take a snapshot of the database.

        :param file_obj: A file-like object to write the database contents in.
        """
        snapshot_request = etcdrpc.SnapshotRequest()
        snapshot_response = self.maintenancestub.Snapshot(
            snapshot_request,
            self.timeout,
            credentials=self.call_credentials,
            metadata=self.metadata
        )

        for response in snapshot_response:
            file_obj.write(response.blob)
