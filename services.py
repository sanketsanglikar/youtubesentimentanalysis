from googleapiclient.discovery import build
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import unicodedata
import re
import itertools
import collections
import warnings
from django.conf import settings
import os
warnings.filterwarnings('ignore')
try:
    nltk.download('stopwords')
except:
    pass


class YoutubeSentimentAnalysis:
    # api_key = 'AIzaSyAC7dHcAjttc5nhOYr9ohf9eeNZrCwtwOg'
    # video_id = 'JKeRM918XDA'
    def __init__(self, api_key, video_id):
        self.api_key = api_key
        self.video_id = video_id

    def ytScrap(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        video = youtube.commentThreads().list(part='snippet,replies', videoId=self.video_id).execute()
        comments = []
        while (video):
            for item in range(len(video['items'])):
                comments.append(video['items'][item]['snippet']['topLevelComment']['snippet']['textDisplay'])
            try:
                if 'nextPageToken' in video and len(comments) < 1001:
                    video = youtube.commentThreads().list(part='snippet', videoId=self.video_id, maxResults=50,
                                                          pageToken=video['nextPageToken']).execute()
                else:
                    break
            except:
                print("Not Much Comments")

        return comments

    def data_cleaning(self, comments):
        all_comments_no_urls = [" ".join(
            re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "",
                   each_comment).split()) for each_comment in comments]

        all_comments_no_urls = [" ".join(re.sub('(@[A-Za-z0-9_]+)', "", each_comment).split()) for each_comment in
                                all_comments_no_urls]
        all_comments_no_urls = [" ".join(re.sub('<a.*?>|</a>', "", each_comment).split()) for each_comment in
                                all_comments_no_urls]
        all_comments_no_urls = [" ".join(re.sub('<br />', '', each_comment).split()) for each_comment in
                                all_comments_no_urls]
        all_comments_no_urls = [" ".join(re.sub('</a>', '', each_comment).split()) for each_comment in all_comments_no_urls]
        all_comments_no_urls = [
            ''.join(unicodedata.normalize('NFKD', each).encode('ascii', 'ignore').decode('utf-8', 'ignore')) for each in
            all_comments_no_urls]

        words_in_comments = [comm.lower().split() for comm in all_comments_no_urls]

        return words_in_comments

    def removing_stop_words(self, words_in_comments):
        # List of all words across commnet
        all_words_no_urls = list(itertools.chain(*words_in_comments))

        # Create counter
        counts_no_urls = collections.Counter(all_words_no_urls)

        stop_words = set(stopwords.words('english'))

        comments_with_no_sw = [[word for word in comment_words if not word in stop_words]
                               for comment_words in words_in_comments]
        all_words_no_sw = list(itertools.chain(*comments_with_no_sw))

        return all_words_no_sw

    def get_comment_sentiment(self, each_comm):
        import textblob
        from textblob import TextBlob

        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(each_comm)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def saving_figure(self, all_words_no_sw):
        sentiment_score = []
        for i in range(len(all_words_no_sw)):
            sentiment_score.append(self.get_comment_sentiment(' '.join(all_words_no_sw[i])))
        scores = {'neutral': sentiment_score.count('neutral'), 'positive': sentiment_score.count('positive'),
                  'negative': sentiment_score.count('negative')}
        plt.bar(scores.keys(), scores.values())
        plt.savefig('api\static\{}_{}_sentiment.png'.format(self.api_key, self.video_id))
        data = ' '.join(each_word for each_word in all_words_no_sw)
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(data)
        plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig('api\static\{}_{}_wordcloud.png'.format(self.api_key, self.video_id))
        return None


