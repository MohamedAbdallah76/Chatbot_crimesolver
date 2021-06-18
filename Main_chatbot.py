# from pprint import pprint
import random
import nltk
import vaderSentiment.vaderSentiment as vd

victim_info = {("name", "moh"),
               ("location", "coach5"),
               ("time", "5pm-6pm")}

victim = "Moh"
suspects = ["Adeola", "Vikram", "Delfina"]
active = True
to_be_questioned = ["Adeola", "Vikram", "Delfina"]
AD_likelihood = 0
VI_likelihood = 0
DE_likelihood = 0
AD_answer = []
VI_answer = []
DE_answer = []
# start of chatbot loop
while active:
    info_list = list(victim_info)
    if to_be_questioned:  # is non-empty
        suspect = to_be_questioned.pop()
        print("Hello" + " " + suspect)
        question = "where were you between 5pm and 6pm?"
        reply1 = input(question)
        # checks if location of suspect and victim matches
        if "coach5" == reply1.lower():
            if suspect == "Adeola":
                AD_likelihood += 1
            elif suspect == "Vikram":
                VI_likelihood += 1
            else:
                DE_likelihood += 1
        # checks if suspect has any negative feeling toward the victim
        question = "Do you have any relation to Moh?"
        reply2 = input(question)

        analyzer = vd.SentimentIntensityAnalyzer()
        tokens_reply = nltk.word_tokenize(reply2)
        sentiments = []
        for i in tokens_reply:
            sentiments.append(analyzer.polarity_scores(i)["compound"])
        avg_sentiment = sum(sentiments) / len(sentiments)
        if avg_sentiment < 0:
            if suspect == "Adeola":
                AD_likelihood += 1
            elif suspect == "Vikram":
                VI_likelihood += 1
            else:
                DE_likelihood += 1
        # checks if any of the suspect suspect the others
        question = "Do you suspect any one?"
        reply3 = input(question)
        if suspect == "Adeola":
            AD_answer.append(reply3)
        elif suspect == "Vikram":
            VI_answer.append(reply3)
        else:

            DE_answer.append(reply3)

        if "adeola" in reply3.lower().split():
            AD_likelihood += 1
        elif "delfina" in reply3.lower().split():
            DE_likelihood += 1
        elif "vikram" in reply3.lower().split():
            VI_likelihood += 1

    else:
        question = "got any questions about the case?"
        helpRequest = input(question)
        if helpRequest == "no":
            active = False
            continue

        stemmer = nltk.stem.lancaster.LancasterStemmer()
        stemmed = stemmer.stem(helpRequest)
        tokens = nltk.word_tokenize(stemmed)

        if "who" in tokens:
            # checks for highest likelihood score
            if AD_likelihood > DE_likelihood and AD_likelihood > VI_likelihood:
                print("Most likely suspect Adeola")
            elif DE_likelihood > AD_likelihood and DE_likelihood > VI_likelihood:
                print("Most likely suspect Delfina")
            elif DE_likelihood == AD_likelihood == VI_likelihood:
                print("Most likely all suspects collaborated in the murder")
            elif VI_likelihood > AD_likelihood and VI_likelihood > DE_likelihood:
                print("Most likely suspect Vikram")
            elif VI_likelihood == AD_likelihood:
                print("Most likely suspect Vikram and Adeola collaborated")
            elif AD_likelihood == DE_likelihood:
                print("Most likely suspect Delfina and Adeola collaborated")
            elif VI_likelihood == DE_likelihood:
                print("Most likely suspect Vikram and Delfina collaborated")

        if "doubt" in tokens or "lie" in tokens:
            # check for uncertainty in the suspects answers
            if "might" in DE_answer[0].lower().split() or "think" in DE_answer[0].lower().split():
                print("Delfinas suspicions were unreliable")
            if "might" in AD_answer[0].lower().split() or "think" in AD_answer[0].lower().split():
                print("Adeolas suspicions were unreliable")
            if "might" in VI_answer[0].lower().split() or "think" in VI_answer[0].lower().split():
                print("Vikrams suspicions were unreliable")
