import re
import string


def remove_punctuation(text):
    text = "".join([i for i in str(text) if i not in string.punctuation])
    text = text.replace('\u201D', " ")
    text = text.replace('\u2018', " ")
    text = text.replace('\u2019', " ")
    text = text.replace('\u201c', " ")
    text = text.replace('\u2026', " ")
    text = re.sub(r'\.{2,}', ' ', text)

    return text


def text_reformat(text):
    # remove two or more dots
    text = re.sub(r'\.{2,}', ' ', text)
    # remove two or more letters: { bellooooo -> bello}
    text = re.sub(r'(.)\1+', r'\1\1', text)

    return text.lower()


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)

    return re.sub(emoj, '', data)


def preprocessing_steps(data):
    new_data = remove_punctuation(data)
    new_data = text_reformat(new_data)
    new_data = remove_emojis(new_data)

    return new_data


def preprocess(data):

    array = []

    for index, tweet in data.iterrows():

        # print(tweet['Text'])
        new_data = preprocessing_steps(tweet['text'])
        array.append(new_data)
        # print(new_data, "\n")

    data['text'] = array

    print("Preprocessing done")

    return data


if __name__ == '__main__':
    pass
