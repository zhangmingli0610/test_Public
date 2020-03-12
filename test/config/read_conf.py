# coding = utf-8
import yaml
import os


def get_value(name):
    curPath = os.path.dirname(os.path.dirname(__file__))
    yamlPath = os.path.join(curPath, r'config\conf.yaml')
    with open(yamlPath) as f:
        y = f.read()
    token = yaml.load(y, Loader=yaml.FullLoader)
    return token[name]


def write_token(token):
    curPath = os.path.dirname(os.path.dirname(__file__))
    yamlPath = os.path.join(curPath, r'config\conf.yaml')
    with open(yamlPath, 'r', encoding='utf-8') as f:
        y = f.read()
    alldata = yaml.load(y, Loader=yaml.FullLoader)
    alldata['token'] = token
    with open(yamlPath, 'w', encoding='utf-8') as ff:
        yaml.dump(alldata, ff)



if __name__ == '__main__':
    write_token('12345678')
    token = get_value('url')
    print(token)

