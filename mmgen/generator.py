import logging
import datetime
import random
from mmgen.models import mystery
from mmgen.exceptions import InputConstraintException
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Generator:
    """
    Used to generate a murder mystery
    Set the appropriate options, run the generate-method and it will create a mystery object
    This object can the be used by one of the renderers to, for instance, save it to disk
    """

    options = {
        "MIN_CHARACTERS": 4,
        "MAX_CHARACTERS": 6,
        "START_DATE": -3600 * 24 * 365 * 50,
        "CURRENT_DATE": -3600 * 24 * 365 * 10,
    }

    def generate(self):
        logger.info("Generating new mystery")
        myst = mystery.Mystery()

        myst.start_date = self.options["START_DATE"]
        myst.current_date = self.options["CURRENT_DATE"]

        cfg_start_date = datetime.datetime.fromtimestamp(self.options["START_DATE"])
        cfg_current_date = datetime.datetime.fromtimestamp(self.options["CURRENT_DATE"])
        logger.info("Timespan: {0} - {1}".format(
                        cfg_start_date.strftime("%Y-%m-%d"),
                        cfg_current_date.strftime("%Y-%m-%d")
                    ))

        if self.options["CURRENT_DATE"] <= self.options["START_DATE"]:
            raise InputConstraintException("The start date must be before the current date")
        if self.options["CURRENT_DATE"] - self.options["START_DATE"] < 3600 * 24 * 365 * 18:
            raise InputConstraintException("The timespan must be at least 18 years")


        myst.num_characters = random.randint(
                            self.options["MIN_CHARACTERS"],
                            self.options["MAX_CHARACTERS"])
        myst.populate()



    def read_config(self, path):
        logger.info("Reading config file: {0}".format(path))

    def main(self, args):
        if len(args) > 1:
            self.read_config(args[1])
        self.generate()

def main(args=None):
    Generator().main(args)
