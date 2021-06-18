#from pprint import pprint
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
AD_answers1 = ["coach5", "coach6", "coach2"]
VI_answers1 = ["coach5", "coach6", "coach2"]
DE_answers1 = ["coach5", "coach6", "coach2"]
AD_answers2 = ["He cheated me in a game of poker earlier cost me a lot of money. Don't like him very much.",
               "Only met him on this trip didn't lokr him very much though.",
               "Known him for a few years now we're good friends."]
VI_answers2 = ["Yeah we were friends. met him in school we have ben giod friwnds ever since.",
               "We were froend but ended upon bsd terms earlier this year.", "Only met him on this trip seems nice."]
DE_answers2 = ["no only met him on this trp seemed nnoce though", "No I don't know him.",
               "Met him through a mutual friend a while back been good friends ever since."]
AD_answers3 = ["I might have seen Vikrum going out of his room, looked suspicious.",
               "I saw vikram argoing with him earlier and I saw him near his room at night as well.",
               "I was talking to delfina and she seemed to dislike him very much."]
VI_answers3 = ["I think I remmember seeing Adeola arguing with him looked like she was angry at him.", "No didn't see anything.",
               "Saw delphina leave his room late at night."]
DE_answers3 = ["I recall seeing him and Adeola arguing earlier in the day",
               "I saw vikram fighting with him earlier in the day.", "No haven't seen anything"]

AD_answers = []
VI_answers = []
DE_answers = []
# start of chatbot loop
while active:
    info_list = list(victim_info)
    if to_be_questioned:  # is non-empty
        suspect = to_be_questioned.pop()
        print("Hello" + " " + suspect)
        question = "where were you between 5pm and 6pm?"
        if suspect == "Adeola":
            reply1 = random.choice(AD_answers1)
            AD_answers.append(reply1)
        elif suspect == "Vikram":
            reply1 = random.choice(VI_answers1)
            VI_answers.append(reply1)
        else:
            reply1 = random.choice(DE_answers1)
            DE_answers.append(reply1)
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
        if suspect == "Adeola":
            reply2 = random.choice(AD_answers2)
            AD_answers.append(reply2)
        elif suspect == "Vikram":
            reply2 = random.choice(VI_answers2)
            VI_answers.append(reply2)
        else:
            reply2 = random.choice(DE_answers2)
            DE_answers.append(reply2)

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
        if suspect == "Adeola":
            reply3 = random.choice(AD_answers3)
            AD_answers.append(reply3)
        elif suspect == "Vikram":
            reply3 = random.choice(VI_answers3)
            VI_answers.append(reply3)
        else:
            reply3 = random.choice(DE_answers3)
            DE_answers.append(reply3)

        if "adeola" in reply3.lower().split():
            AD_likelihood += 1
        elif "delfina" in reply3.lower().split():
            DE_likelihood += 1
        elif "vikram" in reply3.lower().split():
            VI_likelihood += 1

    else:
        print("Adeola: ")
        print(AD_answers)
        print("Vikram: ")
        print(VI_answers)
        print("Delfina: ")
        print(DE_answers)
        print(AD_likelihood)
        print(VI_likelihood)
        print(DE_likelihood)
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
            if "might" in DE_answers[2].lower().split() or "think" in DE_answers[2].lower().split():
                print("Delfinas suspicions were unreliable")
            if "might" in AD_answers[2].lower().split() or "think" in AD_answers[2].lower().split():
                print("Adeolas suspicions were unreliable")
            if "might" in VI_answers[2].lower().split() or "think" in VI_answers[2].lower().split():
                print("Vikrams suspicions were unreliable")

