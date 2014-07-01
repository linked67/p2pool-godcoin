import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc
from operator import *


@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)


@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(

godcoin=math.Object(
        P2P_PREFIX='a3d5c2f9'.decode('hex'),
        P2P_PORT=12701,
        ADDRESS_VERSION=38,
        RPC_PORT=12700,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'godcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),                           
        #SUBSIDY_FUNC=lambda nBits, height: __import__('juggalocoin_subsidy').GetBlockBaseValue(nBits, height),
        SUBSIDY_FUNC=lambda bitcoind, target: get_subsidy(bitcoind, target),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('xcoin_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('xcoin_hash').getPoWHash(data)),
        BLOCK_PERIOD=600, # s
        SYMBOL='GOD',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'godcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/godcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.godcoin'), 'godcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='',
        ADDRESS_EXPLORER_URL_PREFIX='',
        TX_EXPLORER_URL_PREFIX='',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1), 
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
