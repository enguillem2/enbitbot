import os
import pprint

en_var = os.environ['ZK_SYNC_LIBRARY_PATH']
PermissionError(f"envar: {en_var}")
from zksync_sdk import ZkSyncLibrary
lib = ZkSyncLibrary()