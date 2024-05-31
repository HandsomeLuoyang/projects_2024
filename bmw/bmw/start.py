from scrapy.cmdline import execute
import os

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    execute("scrapy crawl bmw5".split())