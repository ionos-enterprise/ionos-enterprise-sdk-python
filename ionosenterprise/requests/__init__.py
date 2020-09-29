from .dicts import dicts
from .datacenter import datacenter
from .server import server
from .cdrom import cdrom
from .contract import contract
from .firewall import firewall
from .group import group
from .image import image
from .ipblock import ipblock
from .lan import lan
from .loadbalancer import loadbalancer
from .location import location
from .nic import nic
from .request import request
from .resource import resource
from .share import share
from .snapshot import snapshot
from .user import user
from .volume import volume
from .k8s import k8s
from .k8s_config import k8s_config
from .k8s_nodepools import k8s_nodepools
from .pccs import pccs
from .backupunit import backupunit
from .s3key import s3key
from coreadaptor.AuthAdaptor import AuthAdaptor
from ionosenterprise import __version__

class IonosEnterpriseRequests(
    dicts,
    datacenter,
    server,
    cdrom,
    contract,
    firewall,
    group,
    image,
    ipblock,
    lan,
    loadbalancer,
    location,
    nic,
    request,
    resource,
    share,
    snapshot,
    user,
    volume,
    k8s,
    k8s_config,
    k8s_nodepools,
    pccs,
    backupunit,
    s3key
):
    def get_api_client(self):
        auth_adaptor = AuthAdaptor(self.username, self.password).get_api_client()
        auth_adaptor.user_agent = "ionos-cloud-sdk-python-compat/%s" % __version__
        return auth_adaptor

    def get_api_instance(self, apiClass):
        return apiClass(self.get_api_client())


__all__ = ['IonosEnterpriseRequests']
