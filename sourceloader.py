import inspect
import os
import re
import ConfigParser

from FourmiCrawler.sources.source import Source


class SourceLoader:
    sources = []

    def __init__(self, rel_dir="FourmiCrawler/sources"):
        """
        The initiation of a SourceLoader, selects and indexes a directory for usable sources.
        :param rel_dir: A relative path to a directory.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        path += "/" + rel_dir
        known_parser = set()

        config = ConfigParser.ConfigParser()
        config.read('sources.cfg')

        for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
            mod = __import__('.'.join([rel_dir.replace("/", "."), py]), fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if inspect.isclass(getattr(mod, x))]
            for cls in classes:
                if issubclass(cls, Source) and cls not in known_parser:
                    sourcecfg = dict()
                    if config.has_section(cls.__name__):
                        sourcecfg = dict(config.items(cls.__name__))
                    self.sources.append(cls(sourcecfg))
                    known_parser.add(cls)

    def include(self, source_names):
        """
        This function excludes all sources that don't match the given regular expressions.
        :param source_names: A list of regular expression (strings)
        """
        new = set()
        for name in source_names:
            new.update([src for src in self.sources if re.match(name, src.__class__.__name__)])
        self.sources = list(new)

    def exclude(self, source_names):
        """
        This function excludes all sources that match the given regular expressions.
        :param source_names: A list of regular expression (strings)
        """
        exclude = []
        for name in source_names:
            exclude.extend([src for src in self.sources if re.match(name, src.__class__.__name__)])
        self.sources = [src for src in self.sources if src not in exclude]

    def __str__(self):
        """
        This function returns a string with all sources currently available in the SourceLoader.
        :return: a string with all available sources.
        """
        string = ""
        for src in self.sources:
            string += "Source: " + src.__class__.__name__
            string += " - "
            string += "URI: " + src.website + "\n"
        return string
