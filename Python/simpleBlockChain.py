import hashlib as hasher
import datetime as date
#block 
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
	return Block(0, date.datetime.now(), "Genesis Block", "0")

def newBlock(lastBlock):
	thisIndex = lastBlock.index + 1
	thisTimestamp = date.datetime.now()
	thisData = "Hey! I'm block " + str(thisIndex)
	thisHash = lastBlock.hash
	return Block(thisIndex,thisTimestamp,thisData,thisHash)

blockchain = [createGenesisBlock()]
previous_block = blockchain[0]
num_of_blocks_to_add = 20

for i in range(0, num_of_blocks_to_add):
  block_to_add = newBlock(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  # Tell everyone about it!
  print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print ("Hash: {}\n".format(block_to_add.hash))