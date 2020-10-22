import schedule

from analyze_tweets import classify_tweets

def job():
    print("This is a test")

def classify():
    classify_tweets()
    print("Finished classifying")

schedule.every(5).minutes.do(classify)
# schedule.every(1).minutes.do(job())

while True:
    schedule.run_pending()

