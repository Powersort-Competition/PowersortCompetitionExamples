def list_of_words_bible():
    """Return a list of words from the Bible"""
    with open('helper/data/bible.txt', 'r') as f:
        return f.read().split()