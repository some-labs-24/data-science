import emoji
import re


def emoji_free_text(text):
    '''
    Cleans text from emojies
    '''
    emoji_list_1 = [c for c in text if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list_1)])
    return clean_text


def url_free_text(text):
    '''
    Cleans text from urls
    '''
    text = re.sub(r'http\S+', '', text)
    return text


if __name__ == "__main__":
    print(emoji_free_text("Test! 📝 https://emojipedia.org/memo/"))
    print(url_free_text("Test! 📝 https://emojipedia.org/memo/"))