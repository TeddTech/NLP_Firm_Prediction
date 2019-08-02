import nltk
from src.preprocessing.text_extract import replace_number

test = nltk.word_tokenize("I have 10 cats and 30 dogs")
expected = ['I', 'have', '<#>', 'cats', 'and', '<#>', 'dogs']
expected2 = ['I', 'have', '<#>-cats', 'and', '<#>', 'dogs']
expected3 = ['I', 'have', '<#>', 'cats', 'and', '<#>', 'dogs']

class TestClass:

    def test_output_normal_case(self):
        """ Check if branch A of the function works (core function) """
        result = replace_number(test)
        assert result == expected, "Branch A of the function does not work"

    def test_output_type(self):
        """ Test if the function result is a list """
        result = replace_number(test)
        assert isinstance(result,list), "The result is not a list"

    def test_output_digit_string(self):
        """ Check if branch B of the function works (handle digit attaches to a string) """
        test = nltk.word_tokenize("I have 10-cats and 30 dogs")
        result = replace_number(test)
        
        assert result == expected2, "Branch B of the function does not work"
        
    def test_output_digit(self):
        """ Check if branch C of the function works (handle digit attaches to punctuation) """
        test = nltk.word_tokenize("I have 10.10 cats and 30.30 dogs")
        result = replace_number(test)
        
        assert result == expected3, "Branch C of the function does not work"
