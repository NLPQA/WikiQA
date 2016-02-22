__author__ = 'laceyliu'
# team_id	qns_id	article_title	path	qns_difficulty_by_questioner	qns_text	is_disfluent?	is_bad_qns?	answer	qns_difficulty_by_answerer
import sys, collections

gold_path = "../data/view_team_qnsans.txt"
data_path = "../data/sp_data/"



def buildMap():
    global questions, answers, paths
    questions = collections.defaultdict(list)
    answers = collections.defaultdict(dict)
    paths = {}
    first = 0
    prev_id = ""

    with open(gold_path, 'r') as f:
        for line in f:
            if first == 0:
                first = 1
                continue
            values = line.split('\t')
            if values[1] == prev_id:
                continue
            else:
                prev_id = values[1]
            if values[6] == "True" or values[7] == "True":
                continue
            if values[8] == "too hard":
                continue

            title, path, diff, quest, ans = values[2], values[3],values[4], values[5], values[8]

            questions[title].append((quest, diff))
            answers[title][quest] = ans
            paths[title] = path

    f.close()


def findAns(title, question):
    if title in answers:
        if question in answers[title]:
            sys.stdout.write(answers[title][question]+'\n')
        else:
            sys.stdout.write( "Ans not found\n")
    else:
        sys.stdout.write( "Article not found\n")

def retrieveQues(title):
    if title in questions:
        for q in questions[title]:
            sys.stdout.write(q[0]+'\t'+q[1]+'\n')
    else:
        sys.stdout.write( "article not found \n")

def findPath(title):
    if title in paths:
        return(data_path+paths[title]+'.txt')
    else:
        sys.stdout.write( "article not found \n")


buildMap()
# retrieveQues("Slumdog_Millionaire")
# findAns("Slumdog_Millionaire", "Did the film gross $12 million in Japan?")
# findPath("Slumdog_Millionaire")


