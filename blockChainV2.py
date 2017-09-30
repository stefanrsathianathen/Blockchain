from flask import Flask
from flask import request
import json
import requests
node = Flask(__name__)


#stuff for blockchain
import hashlib as hasher
import datetime as date

class Block:
	def __init__(self, index, timestamp, data, previousHash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previousHash = previousHash
		self.hash = self.hashBlock()

	def hashBlock(self):
		sha = hasher.sha256()
		sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previousHash).encode('utf-8'))
		return sha.hexdigest()

def createGenesisBlock():
	return Block(0, date.datetime.now(), {
	             "proof-of-work": 9,
	             "transactions": None}, "0")

def newBlock(lastBlock):
	thisIndex = lastBlock.index + 1
	thisTimestamp = date.datetime.now()
	thisData = "Hey! I'm block " + str(thisIndex)
	thisHash = lastBlock.hash
	return Block(thisIndex,thisTimestamp,thisData,thisHash)


#Blockchain
blockchain = []
blockchain.append(createGenesisBlock())


#transactions on this node
thisNodesTransactions = []

minerAddress = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

#store all other peers so we can communicate with them
peerNodes = []
mining = True

@node.route('/txion', methods=['POST'])
def transaction():
	if request.method == 'POST':
		#each new post request
		# get the new transaction data
		newTxion = request.get_json()
		#add it to the nodes transactions list
		thisNodesTransactions.append(newTxion)

		print("New transaction")
		print("From: {}".format(newTxion['from']))
		print("To: {}".format(newTxion['to']))
		print("Amount: {}\n".format(newTxion['amount']))
		#transaction was successful
		return "Transaction will be added to the blockchain soon!"

@node.route('/mine', methods = ['GET'])
def mine():
	#get last proof of work
	lastBlock = blockchain[len(blockchain) - 1]
	lastProof = lastBlock.data['proof-of-work']
	# find the proof of work for the current block 
	# being mined
	proof = proofOfWork(lastProof)
	thisNodesTransactions.append({"from": "network", "to": minerAddress, "amount": 1})
	newBlockData = {
		"proof-of-work": proof,
		"transactions": list(thisNodesTransactions)
	}
	newBlockIndex = lastBlock.index + 1
	newBlockTimeStamp = thisTimestamp = date.datetime.now()
	lastBlockHash = lastBlock.hash
	#empty transaction list
	thisNodesTransactions[:] = []
	#create new block
	minedBlock = Block(newBlockIndex, newBlockTimeStamp,newBlockData, lastBlockHash)
	blockchain.append(minedBlock)

	return json.dumps({
	                  "index": newBlockIndex,
	                  "timestamp": str(newBlockTimeStamp),
	                  "data": newBlockData,
	                  "hash": lastBlockHash
	                  }) + "\n"


@node.route('/blocks', methods=['GET'])
def getBlocks():
	# chainToSend = blockchain
	# #convert our blocks to dict so we can send as json 
	# for block in chainToSend:
	# 	blockIndex = str(block.index)
	# 	blockTimeStamp = str(block.timestamp)
	# 	blockData = str(block.data)
	# 	blockHash = str(block.hash)
	# 	block = {
	# 		"index": blockIndex,
	# 		"timestamp": blockTimeStamp,
	# 		"data": blockData,
	# 		"hash": blockHash
	# 	}
	# #send the chain to who ever requested
	# chainToSend = json.dumps(chainToSend)
	# return chainToSend

	chainToSend = blockchain
	blocklist = ""
	for i in range(len(chainToSend)):
		block = chainToSend[i]
		blockIndex = str(block.index)
		blockTimeStamp = str(block.timestamp)
		blockData = str(block.data)
		blockHash = str(block.hash)
		assembled = json.dumps({
		    "index": blockIndex,
			"timestamp": blockTimeStamp,
			"data": blockData,
			"hash": blockHash
		                       })
		if blocklist == "":
			blocklist = assembled
		else:
			blocklist += assembled
		return blocklist

def findNewChains():
	#Get the blockchains of every other node
	otherChains = []
	for nodeUrl in peerNodes:
		#Get their chain using a get request
		block = requests.get(nodeUrl + "/blocks").content
		#convert to python dict
		block = json.loads(block)
		#add it to our list
		otherChains.append(block)
	return otherChains

def consensus():
	# Get the blocks from other nodes
	otherChains = findNewChains()
	#if our chain isnt the longest
	#make our chain store the longest
	longestChain = blockchain
	for chain in otherChains:
		if len(longestChain) < len(chain):
			longestChain = chain
	# If the longest chain wasn't our
	# set our chain to the longest
	blockchain = longestChain

def proofOfWork(lastProof):
	#variable to use to find next proof of work
	incrementor = lastProof + 1
	#keep incrementing the incrementor until
	#it's equal to a number divisible by 9
	# and the proof of work of the previous
	#block in the chain

	while not(incrementor % 9 == 0 and incrementor % lastProof == 0):
		incrementor += 1

	#Once that number is found,
	# we can return it as proof
	# of our work
	return incrementor

node.run()
