
## Test Documentation

### Contents:
|Function|Coverage|Passing|Details|
|:-:|:-:|:-:|:-:|
|`annualize()`|100%|:ballot_box_with_check:|<a href="#annualize">link</a>|
|`bi_col()`|100%|:ballot_box_with_check:|<a href="#bi_col">link</a>|
|`cv_lda()`|0%|:x:|<a href="#cv_lda">link</a>|
|`diff_col()`|100%|:ballot_box_with_check:|<a href="#diff_col">link</a>|
|`diff_label()`|100%|:ballot_box_with_check:|<a href="#diff_label">link</a>|
|`extract_topics()`|0%|:x:|<a href="#extract_topics">link</a>|
|`Filing()`|100%|:ballot_box_with_check:|<a href="#Filing">link</a>|
|`filing_from_mongo()`|25%|:x:|<a href="#filing_from_mongo">link</a>|
|`filings_to_json()`|100%|:ballot_box_with_check:|<a href="#filings_to_json">link</a>|
|`gensim_model()`|100%|:ballot_box_with_check:|<a href="#gensim_model">link</a>|
|`get_all_filings()`|40%|:ballot_box_with_check:|<a href="#get_all_filings">link</a>|
|`label_performance()`|100%|:ballot_box_with_check:|<a href="#label_performance">link</a>|
|`mrk_cap()`|100%|:ballot_box_with_check:|<a href="#mrk_cap">link</a>|
|`ratio_col()`|100%|:ballot_box_with_check:|<a href="#ratio_col">link</a>|
|`replace_number()`|0%|:ballot_box_with_check:|<a href="#replace_number">link</a>|
|`sub_col()`|100%|:ballot_box_with_check:|<a href="#sub_col">link</a>|
|`subset_cols()`|100%|:ballot_box_with_check:|<a href="#subset_cols">link</a>|
|`subset_rows()`|100%|:ballot_box_with_check:|<a href="#subset_rows">link</a>|
|`sum_ytd()`|80%|:x:|<a href="#sum_ytd">link</a>|
|`tfidf_nmf()`|0%|:x:|<a href="#tfidf_nmf">link</a>|
|`tokenize_filings()`|100%|:ballot_box_with_check:|<a href="#tokenize_filings">link</a>|
|`topics()`|100%|:ballot_box_with_check:|<a href="#topics">link</a>|
|`vol()`|100%|:ballot_box_with_check:|<a href="#vol">link</a>|



#### annualize

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_df_out_size`|Ensure that the output is the expected size|:ballot_box_with_check:|
|`test_df_contents`|Validate selected observations|:ballot_box_with_check:|

#### bi_col

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_bi_thresh`| Branch A: Check that value are of correct type when thresh hold is specified | :ballot_box_with_check:|
|`test_bi` | Branch B: Check that value of are of correct type | :ballot_box_with_check:|


#### cv_lda

|Test|Purpose|Passing|
|:-:|:-:|:-:|


#### diff_col

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_diff`|Branch A: Check that the difference computed from the function is the same as manually|:ballot_box_with_check:|
|`test_diff_pct`|Branch B: Check that percent changes also work|:ballot_box_with_check:|


#### diff_label

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_label_shift`|Branch B: Check that labels are correctly computed and shifted approporiately when using pct|:ballot_box_with_check:|
|`test_not_pct`|Branch A: Check that absolute value changes also work|:ballot_box_with_check:|


#### extract_topics

|Test|Purpose|Passing|
|:-:|:-:|:-:|


#### Filing

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_required`|Test that required items are actually required|:ballot_box_with_check:|
|`test_items`||N|


#### filing_from_mongo

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_filing_from_mongo`|Test that the `filing_from_mongo()` function is able to create a Filing object|:ballot_box_with_check:|


#### filings_to_json()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_result_len`|Check that the output Filing object has correct length|:ballot_box_with_check:|
|`test_result`|Check that the output Filing object has correct content |:ballot_box_with_check:|
|`test_json_file `|Check that the output json file has correctly created |:ballot_box_with_check:|


#### gensim_model()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_result`|Check that the function returns a list of gensim LDA model, corpus and disctionary as expected|:ballot_box_with_check:|
|`test_corpus`|Check that the function only returns the same number of topic as specified|:ballot_box_with_check:|


#### get_all_filings()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_result`|Branch A: Check that the function returns a Filing object, as expected|:ballot_box_with_check:|
|`test_limit_number`|Branch B: Check that the function only returns an equal number, or fewer filings than the limit|:ballot_box_with_check:|


#### label_performance

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_up`|Check that observations that should be labelled up are done so.|:ballot_box_with_check:|
|`test_down`|Check that observations that should be labelled down are done so|:ballot_box_with_check:|
|`test_flat`|Check that observations that should be labelled flat are done so|:ballot_box_with_check:|
|`test_different_cutoff`|Check that specifying a different cutoff does not break anything|:ballot_box_with_check:|


#### mrk_cap

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_mrk_cap`|Check as denominator approaches infinity values are zero |:ballot_box_with_check:|


#### ratio_col()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_ratio`| Checks that identical columns have a value of `1` | :ballot_box_with_check:|


#### replace_number()

|Test|Purpose|Passing|
|:-:|:-:|:-:|


#### sub_col()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_sub_col`|Check that values of identical columns is zero|:ballot_box_with_check:|


#### subset_cols()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_output`|Check that the output is the correct type (dataframe)|:ballot_box_with_check:|
|`test_cols_number`|Check that the shape of the results matches the number of columns specified|:ballot_box_with_check:|
|`test_cols_blank`|Ensure that the result dataframe is not empty|:ballot_box_with_check:|


#### subset_rows()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_csv`|Check that the input is a .csv file|:ballot_box_with_check:|
|`test_output`|Check that the output is the correct type (dataframe)|:ballot_box_with_check:|
|`test_rows_number`|Check that the shape of the results matches the number of columns specified|:ballot_box_with_check:|
|`test_rows_blank`|Ensure that the result dataframe is not empty|:ballot_box_with_check:|
|`test_rows_branch`|Ensure all branches in the function operate properly|:ballot_box_with_check:|


#### sum_ytd()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_ytd`||:ballot_box_with_check:|


#### tfidf_nmf()

|Test|Purpose|Passing|
|:-:|:-:|:-:|


#### tokenize_filings()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_result`|Check that the Filing object is correctly tokenized|:ballot_box_with_check:|


#### topics()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_topics_corpus`| Confirms corpus keeps it's order after turning it into a dataframe|:ballot_box_with_check:|


#### vol()

|Test|Purpose|Passing|
|:-:|:-:|:-:|
|`test_vol`|Confrims  rows with different ticker values then the ones above them are `NaN`|:ballot_box_with_check:|






```python

```


```python

```


```python

```


```python

```


```python

```
