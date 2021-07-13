from securewei.detectors.reentrancy.reentrancy import Reentrancy

class Data:
    filename = ''
    def __init__(self):
        self.filename='message.sol'


print('test')

filename='message.sol'
result=Reentrancy.detect(filename)
print(result)