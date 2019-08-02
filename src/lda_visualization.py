import pyLDAvis
import numpy as np
import pandas as pd

from sklearn.manifold import TSNE
from gensim.models.ldamodel import LdaModel
from src.models import gensim_model, cv_lda, tfidf_nmf

# Bokeh
from bokeh.io import output_notebook, output_file
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, CustomJS, ColumnDataSource, Slider
from bokeh.layouts import column
from bokeh.palettes import all_palettes

# Visualization
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import seaborn as sns
%matplotlib inline


def get_pyldavis(filings_list, model, item_num, topic_number, stop_word_list,
                 display=False, format='html', save_to="pyLDAvis_figure", 
                 random_state=None, logger=None):  # Tested [N]

    """
    Creates an interactive pyLDAvis image for specified topic modeling option (gensim, cv_lda)
        Args:
            filings_list(list)  : List of filing in Filing object
            model(str)          : Name of topic modeling method (gensim, cv_lda)
            item_num(int)       : Item from filing object that user want to perform topic modeling on
            topic_number(int)   : Number of topic user wants to extract
            stop_word_list(list): List of stopword
            display(bool)       : Option to display on a notebook/environment
            format(str)         : Format of the output (html, json). Default is html.
            save_to(str)        : Name of output. (Default is pyLDAvis_figure)
            random_state=None   : Fix the random state of the LDA model.
            logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging is performed.
        
        Returns:
            An interactive pyLDAvis image
    """
    if logger:
        logger.info("Model the topic:")
    if model == "gensim": # Branch A
        result = gensim_model(filings_list, item_num=item_num, topic_number=topic_number, 
                              stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        
        lda_vis = pyLDAvis.gensim.prepare(result[0], result[1], result[2])

    elif model == "cv_lda": # Branch B
        result = cv_lda(filings_list, item_num=item_num, topic_number=topic_number, 
                              stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        
        lda_vis = pyLDAvis.sklearn.prepare(result[0], result[1], result[2])

    else: # Branch C
        if logger:
            logger.warning("Model input was not in accepted form")
            logger.warning("Using the default choice: CV_LDA")
        print("Model input was not in accepted form")
        print("Using the default choice: CV_LDA")
        
        result = cv_lda(filings_list, item_num=item_num, topic_number=topic_number, 
                        stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        
        lda_vis = pyLDAvis.sklearn.prepare(result[0], result[1], result[2])
        
    if display:
         pyLDAvis.display(lda_vis)

    if format == "json":
        if save_to == "pyLDAvis_figure":
            pyLDAvis.save_json(lda_vis, '{}.json'.format(save_to))
        else:
             pyLDAvis.save_json(lda_vis, save_to)
                
    elif format == "html":
        if save_to == "pyLDAvis_figure":
            pyLDAvis.save_html(lda_vis, '{}.html'.format(save_to))
        else:
            pyLDAvis.save_html(lda_vis, save_to)
    
    else:
        if logger:
            logger.warning("Wrong input for output format!")
            logger.info("Saving file to html")
        print("Wrong input for output format!")
        print("Saving file to html")
        pyLDAvis.save_html(lda_vis, save_to)
            

def get_lda_bokehvis(filings_list, model, item_num, topic_number, stop_word_list, 
                     display=False, format='html', save_to="lda_bokeh_figure.html",
                     random_state=None, logger=None):  # Tested [N]
    """
    Creates a Bokeh image for specified topic modeling option (gensim, cv_lda, tfidf_nmf)
        Args:
            filings_list(list)  : List of filing in Filing object
            model(str)          : Name of topic modeling method (gensim, cv_lda, tfidf_nmf).
            item_num(int)       : Item from filing object that user want to perform topic modeling on
            topic_number(int)   : Number of topic user wants to extract.
            stop_word_list(list): List of stopword.
            display(bool)       : Option to display on a notebook/environment. Default is False.
            format(str)         : Format of the output (html, json). Default is html.
            save_to(str)        : Name of output. Default is pyLDAvis_figure.
            random_state=None   : Fix the random state of the LDA model.
            logger (Logger)     : Logger object from the Logging package which has already been configured. If None, no logging is performed.
        
        Returns:
            An interactive Bokeh image
        """
    
    if model == "gensim": # Branch A
        result = gensim_model(filings_list, item_num=item_num, topic_number=topic_number, 
                              stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        gensim_ldamodel = result[0]
        gensim_corpus = result[1]
        
        hm = np.array([[y for (x,y) in gensim_ldamodel[gensim_corpus[i]]] for i in range(len(gensim_corpus))])
        
    elif model == "cv_lda": # Branch B
        result = cv_lda(filings_list, item_num=item_num, topic_number=topic_number, 
                        stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        
        lda_model = result[0]
        lda_tf = result[1]
        hm = lda_model.fit_transform(lda_tf)
        
    elif model == "tfidf_nmf": # Branch C
        result = tfidf_nmf(filings_list, item_num=item_num, topic_number=topic_number, 
                        stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        
        nmf_model = result[0]
        nmf_tf = result[1]
        hm = nmf_model.fit_transform(nmf_tf)
        
    else: # Branch D
        if logger:
            logger.warning("Model input was not in accepted form")
            logger.warning("Using the default choice: CV_LDA")
        print("Model input was not in accepted form")
        print("Using the default choice: CV_LDA")
        result = cv_lda(filings_list, item_num=item_num, topic_number=topic_number, 
                        stop_word_list=stop_word_list, random_state=random_state, logger=logger)
        
        lda_model = result[0]
        lda_tf = result[1]
        hm = lda_model.fit_transform(lda_tf)

    tsne = TSNE(random_state=random_state)
    tsne_embedding = tsne.fit_transform(hm)
    tsne_embedding = pd.DataFrame(tsne_embedding, columns=['x','y'])
    tsne_embedding['group'] = hm.argmax(axis=1)

    # Creating a list of color:
    new_palettes = all_palettes['Set1'][8] + all_palettes['Set3'][12] + all_palettes['Accent'][8] + all_palettes['Dark2'][8] +              all_palettes['Spectral'][11]
            
    # Make the list contain of all unique color
    new_palettes = list(set(new_palettes))

    source = ColumnDataSource(
            data=dict(
                x = tsne_embedding.x,
                y = tsne_embedding.y,
                colors = [new_palettes[i] for i in tsne_embedding.group],
                group = tsne_embedding.group,
                alpha = [0.9] * tsne_embedding.shape[0],
                size = [7] * tsne_embedding.shape[0]
            )
        )
    hover_tsne = HoverTool(tooltips=[("group", "@group")])

    tools_tsne = [hover_tsne, 'pan', 'wheel_zoom', 'reset']
    plot_tsne = figure(plot_width=700, plot_height=700, tools=tools_tsne, title='TSNE Plot')

    plot_tsne.circle('x', 'y', size='size', fill_color='colors',
                     alpha='alpha', line_alpha=0, line_width=0.01, source=source, name="10K")

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        x = data['x']
        y = data['y']
        colors = data['colors']
        alpha = data['alpha']
        group = data['group']
        year = data['year']
        size = data['size']
        for (i = 0; i < x.length; i++) {
            if (year[i] <= f) {
                alpha[i] = 0.9
                size[i] = 7
            } else {
                alpha[i] = 0.05
                size[i] = 4
            }
        }
        source.trigger('change');
    """)
    
    if display:
        show(plot_tsne)

    output_file(save_to, title="LDA Visualization")