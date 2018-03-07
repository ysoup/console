import yaml


def test():
    stream = open('config.yaml', 'r')
    x = yaml.load(stream)
    print(x)




if __name__== "__main__":
    test()