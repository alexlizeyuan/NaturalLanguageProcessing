
import tweepy
# import nltk; nltk.download('popular')
from nltk.tokenize import regexp_tokenize, word_tokenize
import multidict as multidict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm


def search_tweet(bearer_token, word):

    client = tweepy.Client(bearer_token)
    query = 'ukraine lang:en -has:links -has:hashtags'
    num = 0
    result = []

    #debugging , obtaining 10 tweet
    # tweets = client.search_recent_tweets(query, max_results=10)
    # next_token = tweets.meta['next_token']
    # for tweet in tweets.data:
    #     result.append(tweet.text)
    #     num += 1

    #debug
    #obtain first 100 tweets
    tweets = client.search_recent_tweets(query, max_results=100)
    next_token = tweets.meta['next_token']
    for tweet in tweets.data:
        result.append(tweet.text)
        num += 1

    #obtain 10000 tweets
    while num <= 10000 and tweets.data != None:
        tweets = client.search_recent_tweets(query, max_results=100, next_token=next_token)
        next_token = tweets.meta['next_token']
        for tweet in tweets.data:
            result.append(tweet.text)
            num += 1

    print('current text number is: ', num)
    return result
    # new_query = query + '&' + next_token





    #TODO  use NLTK to tokenize and build frequency map of words
def tokenize_to_freq(tweet_array):
    stop_word_hash = {}
    frequency_hash = {}
    fullTermsDict = multidict.MultiDict()

    #read stopword file
    with open('stopwords.txt', encoding="utf8") as stopword_file:
        for line in stopword_file:
            stop_word_hash[line.strip()] = line.strip()
    stopword_file.close()

    for tweet in tweet_array:
        result = []
        sentence = regexp_tokenize(tweet, r'[,\.\?!"]\s*', gaps=True)
        # for item in sentence:
        #     words = word_tokenize(item)
        #     for word in words:
        #         result.append(word)
        for item in sentence:
            words = item.split()
            for word in words:
                result.append(word)

        for word in result:
            if word not in stop_word_hash:
                if word not in frequency_hash:
                    frequency_hash[word] = 1
                else:
                    frequency_hash[word] += 1

    # print(frequency_hash)
    for key in frequency_hash:
        fullTermsDict.add(key, frequency_hash[key])
    print(fullTermsDict)
    return fullTermsDict




    #TODO last, use word cloud to build a map
def makeImage(text):

    wc = WordCloud(background_color="white", max_words=1000)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()







if __name__ == '__main__':
    result = search_tweet('AAAAAAAAAAAAAAAAAAAAAFf7lAEAAAAAR%2FaSUJVzoeSFdypdbddrml2KK0k%3D2GHJauFKDTLHo9SqHy1xGhgpdszCEvYi47YTnWOzPhwALdCij3', 'today')
    makeImage(tokenize_to_freq(result))



