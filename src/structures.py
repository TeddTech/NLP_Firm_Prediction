from mongoengine import *
from datetime import date


class Filing(object):  # Tested [Y]
    """
    Document class to store SEC filing data from the MongoDB database.

    Fields:
            cik (str): Company Identifier
            period (str): Date of filing
            item1 (str): Business
            item2 (str): Properties
            item3 (str): Legal Proceedings
            item4 (str): Submission of Matters to a vote of security holders
            item5 (str): Market for registrant's common equity and related stockholder matters
            item6 (str): Selected financial data
            item7 (str): Management's discussion and analysis of financial condition and results of operations
            item8 (str): Financial statements and supplementary data
            item9 (str): Changes in and disagreements with accountants on accounting and financial disclosure
            item10 (str): Directors and executive officers of the registrant
            item11 (str): Executive Compensation
            item12 (str): Security ownership of certain beneficial owners and management
            item13 (str): Certain relationships and related transactions
            item14 (str):
    """
    def __init__(self, cik, period,
                 item1=None, item2=None,item3=None,
                 item4=None, item5=None, item6=None,
                 item7=None, item8=None, item9=None,
                 item10=None, item11=None, item12=None,
                 item13=None, item14=None):

        self.cik = cik
        self.period = period
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3
        self.item4 = item4
        self.item5 = item5
        self.item6 = item6
        self.item7 = item7
        self.item8 = item8
        self.item9 = item9
        self.item10 = item10
        self.item11 = item11
        self.item12 = item12
        self.item13 = item13
        self.item14 = item14

    meta = {'allow_inheritance': False}


def filing_from_mongo(result, filter=None, logger=None):  # Tested [P]
    """
    Creates a filing object out of a result from the MongoDB database.

    Args:
        result (MongoDB query result):
        filter (list): List of valid CIKs to filter. If the CIK is not in this list, output will be an empty dict
        logger (Logger): Logger object from the Logging package which has already been configured. If none, no logging
                         is performed.
    Returns:
        (Filing) Object containing the information from the SEC filing result from MongoDB.
    """

    for k, v in result.items():

        if k != "_id":  # Branch A
            if filter:  # Branch B
                try:
                    if v['header']['CIK'] in filter:  # Branch C
                        if logger:
                            logger.info("CIK {} added into the filing list".format(v['header']['CIK']))
                        out = Filing(cik=v['header']["CIK"],
                                     period=v['header']["PERIOD"],
                                     item1=v['items']['item1'],
                                     item2=v['items']['item2'],
                                     item3=v['items']['item3'],
                                     item4=v['items']['item4'],
                                     item5=v['items']['item5'],
                                     item6=v['items']['item6'],
                                     item7=v['items']['item7'],
                                     item8=v['items']['item8'],
                                     item9=v['items']['item9'],
                                     item10=v['items']['item10'],
                                     item11=v['items']['item11'],
                                     item12=v['items']['item12'],
                                     item13=v['items']['item13'],
                                     item14=v['items']['item14'])
                    else:
                        if logger:
                            logger.info("{} not in list of valid CIKs to filter".format(v['header']['CIK']))
                        out = dict()
                except KeyError as e:
                    if logger:
                        logger.warning("Error, filing with id: {} does not appear to have a field: {}".format(result["_id"], e))
                    print("Error, filing with id: {} does not appear to have a field: {}".format(result["_id"], e))
                    out = dict()
            else:  # Branch D
                try:
                    out = Filing(cik=v['header']["CIK"],
                                 period=v['header']["PERIOD"],
                                 item1=v['items']['item1'],
                                 item2=v['items']['item2'],
                                 item3=v['items']['item3'],
                                 item4=v['items']['item4'],
                                 item5=v['items']['item5'],
                                 item6=v['items']['item6'],
                                 item7=v['items']['item7'],
                                 item8=v['items']['item8'],
                                 item9=v['items']['item9'],
                                 item10=v['items']['item10'],
                                 item11=v['items']['item11'],
                                 item12=v['items']['item12'],
                                 item13=v['items']['item13'],
                                 item14=v['items']['item14'])
                except KeyError as e:
                    if logger:
                        logger.warning("Error, filing with id: {} does not appear to have a field: {}".format(result["_id"], e))
                    print("Error, filing with id: {} does not appear to have a field: {}".format(result["_id"], e))
                    out = dict()

    return out  # There should always be at least one non-`_id` column in yash, so this will always be assigned.




