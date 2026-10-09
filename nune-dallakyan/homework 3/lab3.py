import pandas as pd
import re

# 1. Տվյալների բեռնում
df = pd.read_csv('Coachella-2015-2-DFE.csv', encoding='latin1')

# Stop words ցանկի սահմանում (ստանդարտ անգլերեն բառեր)
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 
    'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn'
}

# --- ՔԱՅԼ 1: Հաշթեգերի դուրսբերում ---
def extract_hashtags(text):
    if not isinstance(text, str):
        return []
    return re.findall(r'#\w+', text)

# --- ՔԱՅԼ 2: Էլ. փոստերի դուրսբերում ---
def extract_emails(text):
    if not isinstance(text, str):
        return []
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

# --- ՔԱՅԼ 3: Մաքրման ֆունկցիաների սահմանում ---

# a. Օգտատերերի անունների (@username) հեռացում
def remove_usernames(text):
    return re.sub(r'@\w+', '', text)

# b. Հղումների (http/https) հեռացում
def remove_links(text):
    return re.sub(r'https?://\S+', '', text)

# c. Non-ASCII նիշերի (էմոջիներ, ակցենտավորված տառեր) հեռացում
def remove_non_ascii_symbols(text):
    return text.encode('ascii', 'ignore').decode('ascii')

# d. Տեքստի փոխարկում փոքրատառերի
def to_lower(text):
    return text.lower()

# e. Stop words (հաճախ հանդիպող, ոչ ինֆորմատիվ բառերի) հեռացում
def remove_stop_words(text):
    words = text.split()
    filtered_words = [w for w in words if w.lower() not in STOP_WORDS]
    return ' '.join(filtered_words)

# f. Թվերի հեռացում
def remove_digits(text):
    return re.sub(r'\d+', '', text)

# g. Հատուկ նիշերի և կետադրության հեռացում
def remove_special_characters(text):
    return re.sub(r'[^\w\s]', '', text)

# --- ՄԱՔՐՄԱՆ ՖՈՒՆԿՑԻԱՆԵՐԻ ԿԻՐԱՌՈՒՄ ---

# Հաշթեգերի և էլ. փոստերի ավելացում նոր սյունակներում
df['hashtags'] = df['text'].apply(extract_hashtags)
df['emails'] = df['text'].apply(extract_emails)

# Մաքրված տեքստի ստացման համակցված ֆունկցիա
def clean_tweet_text(text):
    if not isinstance(text, str):
        return ""
    text = remove_usernames(text)
    text = remove_links(text)
    text = remove_non_ascii_symbols(text)
    text = to_lower(text)
    text = remove_stop_words(text)
    text = remove_digits(text)
    text = remove_special_characters(text)
    # Ավելորդ բացատների հեռացում
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Մաքրված տեքստի պահպանում նոր սյունակում
df['clean_text'] = df['text'].apply(clean_tweet_text)

# Արդյունքի ցուցադրում
print(df[['text', 'hashtags', 'emails', 'clean_text']].head())

# Մաքրված տվյալները պահպանում ենք նոր CSV ֆայլում
df.to_csv('cleaned_coachella_tweets.csv', index=False, encoding='utf-8-sig')

print("Ֆայլը հաջողությամբ պահպանվել է որպես 'cleaned_coachella_tweets.csv'")