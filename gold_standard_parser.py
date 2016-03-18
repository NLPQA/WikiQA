__author__ = 'laceyliu'
# team_id	qns_id	article_title	path	qns_difficulty_by_questioner	qns_text	is_disfluent?	is_bad_qns?	answer	qns_difficulty_by_answerer
import sys, collections

gold_path = "./data/view_team_qnsans.php"
data_path = "./data/"


def buildMap():
    global questions, answers, paths
    questions = collections.defaultdict(list)
    answers = collections.defaultdict(dict)
    paths = {}
    first = 0
    prev_id = ""

    with open(gold_path, 'r') as f:
        lines = f.read().splitlines()
    f.close()

    i = 2
    while i < len(lines):
        line = lines[i]

        values = line.split('\t')

        if values[6] == "True" or values[7] == "True":
            i += 2
            continue
        if values[8] == "too hard":
            i += 2
            continue

        title, path, diff, quest, ans = values[2], values[3],values[4], values[5], values[8]
        if len(ans) == 0:
            i += 2
            continue

        questions[title].append((quest, diff))
        answers[title][quest] = ans
        paths[title] = path
        i += 2



def findAns(title, question):
    if title in answers:
        if question in answers[title]:
            sys.stdout.write(answers[title][question]+'\n')
        else:
            sys.stdout.write( "Ans not found\n")
    else:
        sys.stdout.write( "Article not found\n")

def retrieveQues(title, type=None):
    qs = []
    if title in questions:
        for q in questions[title]:
            #sys.stdout.write(q[0]+'\t'+q[1]+'\n')
            if type is not None and q[0].startswith(type):
                sys.stdout.write(q[0]+'\n')
                qs.append(q[0])
            elif type is None:
                sys.stdout.write(q[0]+'\n')
                qs.append(q[0])
        return qs
    else:
        sys.stdout.write( "article not found \n")

def findPath(title):
    if title in paths:
        return(data_path+paths[title]+'.htm')
    else:
        sys.stdout.write( "article not found \n")


buildMap()

qs = retrieveQues("Cancer_(constellation)")

for q in qs:
    print q
    findAns("Cancer_(constellation)", q)

# findAns("Slumdog_Millionaire", "Did the film gross $12 million in Japan?")
print findPath("Cancer_(constellation)")


