#!/usr/bin/env python
"""
Fourmi, a web scraper build to search specific information for a given compound (and it's pseudonyms).

Usage:
    fourmi search <compound>
    fourmi [options] search <compound>
    fourmi [options] [--include=<sourcename> | --exclude=<sourcename>] search <compound>
    fourmi list
    fourmi [--include=<sourcename> | --exclude=<sourcename>] list
    fourmi -h | --help
    fourmi --version

Options:
    --attributes=<regex>            Include only that match these regular expressions split by a comma. [default: .*]
    -h --help                       Show this screen.
    --version                       Show version.
    --verbose                       Verbose logging output.
    --log=<file>                    Save log to an file.
    -o <file> --output=<file>       Output file [default: results.*format*]
    -f <format> --format=<format>   Output formats (supported: csv, json, jsonlines, xml) [default: csv]
    --include=<regex>               Include only sources that match these regular expressions split by a comma.
    --exclude=<regex>               Exclude the sources that match these regular expressions split by a comma.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
import docopt

from FourmiCrawler.spider import FourmiSpider
from utils.configurator import Configurator
from utils.sourceloader import SourceLoader


def setup_crawler(compound, settings, source_loader, attributes):
    """
    This function prepares and start the crawler which starts the actual search on the internet
    :param compound: The compound which should be searched
    :param settings: A scrapy settings object
    :param source_loader: A fully functional SourceLoader object which contains only the sources that should be used.
    :param attributes: A list of regular expressions which the attribute names should match.
    """
    spider = FourmiSpider(compound=compound, selected_attributes=attributes)
    spider.add_sources(source_loader.sources)
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def search(docopt_arguments, source_loader):
    """
    The function that facilitates the search for a specific compound.
    :param docopt_arguments: A dictionary generated by docopt containing all CLI arguments.
    :param source_loader: An initiated SourceLoader object pointed at the directory with the sources.
    """
    conf = Configurator()
    conf.start_log(docopt_arguments["--log"], docopt_arguments["--verbose"])
    conf.set_output(docopt_arguments["--output"], docopt_arguments["--format"])
    setup_crawler(docopt_arguments["<compound>"], conf.scrapy_settings, source_loader, docopt_arguments["--attributes"].split(','))
    reactor.run()


# The start for the Fourmi Command Line interface.
if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='Fourmi - V0.5.0')
    loader = SourceLoader()

    if arguments["--include"]:
        loader.include(arguments["--include"].split(','))
    elif arguments["--exclude"]:
        loader.exclude(arguments["--exclude"].split(','))

    if arguments["search"]:
        search(arguments, loader)
    elif arguments["list"]:
        print "-== Available Sources ==-"
        print str(loader)
