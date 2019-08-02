import pandas as pd
from textblob import TextBlob
from pattern.en import modality

def extract_sentiment(filings_list, polarity=None, subjectivity=None, certainty=None, logger =None):  # Tested [N]
    """
        filings_list (list) :  List of Filings documents
        polarity(list) : List of items to be performed polarity analysis on. None by default.
        subjectivity(list) : List of items to be performed subjectivity analysis on. None by default.
        certainty(list) : List of items to be performed certainty analysis on. None by default.
        logger (Logger): Logger object from the Logging package which has already been configured. If None, no logging is performed.
    """
    if  not any([polarity,subjectivity,certainty]):
        logger.error()
        raise ValueError("At least one sentiment type must be passed.")
    temp_list = list()
    col_name_list = ['cik','period'] + ["certainty_{}".format(p) for p in certainty] + ["polarity_{}".format(p) for p in polarity]+ ["subjectivity_{}".format(p) for p in subjectivity]

    for i in range(len(filings_list)):
        cik_i = filings_list[i]['cik']
        period_i = filings_list[i]['period']
        row_i = [cik_i, period_i]
        if certainty:
            for j in range(len(certainty)):
                row_i.append(modality(filings_list[i][certainty[j]]))
        if polarity == subjectivity and polarity:
            for j in range(len(polarity)):
                row_i.append(TextBlob(filings_list[i][polarity[j]]).sentiment.polarity)
                row_i.append(TextBlob(filings_list[i][subjectivity[j]]).sentiment.subjectivity)
        elif polarity:
            for j in range(len(polarity)):
                row_i.append(TextBlob(filings_list[i][polarity[j]]).sentiment.polarity)
        elif subjectivity:
            for j in range(len(subjectivity)):
                row_i.append(TextBlob(filings_list[i][subjectivity[j]]).sentiment.subjectivity)
        temp_list.append(row_i)

    df = pd.DataFrame(temp_list,columns=col_name_list)
    return df
