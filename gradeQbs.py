import csv
import math

qbs = []
with open("data/Rating_Data.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        qbs.append({'full_name': row[0], 'passing_att': row[1],
                        'passing_cmp': row[2], 'passing_ints': row[3], 'passing_tds': row[4], 'passing_yds': row[5],
                        'rushing_att': row[6], 'rushing_yds': row[7], 'rushing_tds': row[8]})


qbs.pop(0)
# Stats -> cmp_percentage, td_int_ratio, yards_per_attempt, td_attempt_ratio, int_attempt_ratio
for item in qbs[0:]:
    cmp_percentage = float(item["passing_cmp"]) / float(item["passing_att"])
    td_int_ratio = float(item["passing_tds"]) / float(item["passing_ints"])
    yards_per_attempt = float(item["passing_yds"]) / float(item["passing_att"])
    td_attempt_ratio = float(item["passing_tds"]) / float(item["passing_att"])
    int_attempt_ratio = 1 - float(item["passing_ints"]) / float(item["passing_att"])
    int_atttempt_calc = float(item["passing_ints"]) / float(item["passing_att"])
    average_pass_yardage = float(item["passing_yds"]) / float(item["passing_cmp"])

    qb_rating_calc_1 = (cmp_percentage - .3) / .2
    qb_rating_calc_2 = (yards_per_attempt - 3) / 4
    qb_rating_calc_3 = td_attempt_ratio / .05
    qb_rating_calc_4 = (.095 - int_atttempt_calc) / .04
    qb_rating = (qb_rating_calc_1 + qb_rating_calc_2 + qb_rating_calc_3 + qb_rating_calc_4) * 100 / 6

    item.update({"cmp_percentage": cmp_percentage, "td_int_ratio": td_int_ratio, "yards_per_attempt": yards_per_attempt, "td_attempt_ratio": td_attempt_ratio, "int_attempt_ratio": int_attempt_ratio, "average_pass_yardage": average_pass_yardage, "qb_rating": qb_rating})

# Get data for normalization
cmp_percentages = [x["cmp_percentage"] for x in qbs]
min_cmp_percentages = min(cmp_percentages)
max_cmp_percentages = max(cmp_percentages)

td_int_ratios = [x["td_int_ratio"] for x in qbs]
min_td_int_ratios = min(td_int_ratios)
max_td_int_ratios = max(td_int_ratios)

yards_per_attempts = [x["yards_per_attempt"] for x in qbs]
min_yards_per_attempts = min(yards_per_attempts)
max_yards_per_attempts = max(yards_per_attempts)

td_attempt_ratios = [x["td_attempt_ratio"] for x in qbs]
min_td_attempt_ratios = min(td_attempt_ratios)
max_td_attempt_ratios = max(td_attempt_ratios)

int_attempt_ratios = [x["int_attempt_ratio"] for x in qbs]
min_int_attempt_ratios = min(int_attempt_ratios)
max_int_attempt_ratios = max(int_attempt_ratios)

average_pass_yardages = [x["average_pass_yardage"] for x in qbs]
min_average_pass_yardages = min(average_pass_yardages)
max_average_pass_yardages = max(average_pass_yardages)

qb_ratings = [x["qb_rating"] for x in qbs]
min_qb_ratings = min(qb_ratings)
max_qb_ratings = max(qb_ratings)

# Get overall score
for item in qbs:
    normalized_cmp_percentage = (item["cmp_percentage"] - min_cmp_percentages) / (max_cmp_percentages - min_cmp_percentages)
    normalized_td_int_ratio = math.log10(1 + 99 * ((item["td_int_ratio"] - min_td_int_ratios) / (max_td_int_ratios - min_td_int_ratios)))
    normalized_yards_per_attempts = (item["yards_per_attempt"] - min_yards_per_attempts) / (max_yards_per_attempts - min_yards_per_attempts)
    normalized_td_attempt_ratios = (item["td_attempt_ratio"] - min_td_attempt_ratios) / (max_td_attempt_ratios - min_td_attempt_ratios)
    normalized_int_attempts_ratios = (item["int_attempt_ratio"] - min_int_attempt_ratios) / (max_int_attempt_ratios - min_int_attempt_ratios)
    normalized_average_pass_yardages = (item["average_pass_yardage"] - min_average_pass_yardages) / (max_average_pass_yardages - min_average_pass_yardages)
    normalized_qb_ratings = (item["qb_rating"] - min_qb_ratings) / (max_qb_ratings - min_qb_ratings)
    norm_array = [normalized_cmp_percentage, normalized_td_int_ratio, normalized_yards_per_attempts, normalized_td_attempt_ratios, normalized_int_attempts_ratios, normalized_average_pass_yardages, normalized_qb_ratings]
    weights_array = [1, 2, 1, .5, .5, .5, 1.5]
    if item["full_name"] == "Matthew Stafford" or item["full_name"] == "Josh McCown":
        print item["full_name"]
        print normalized_cmp_percentage, normalized_td_int_ratio, normalized_yards_per_attempts, normalized_td_attempt_ratios, normalized_int_attempts_ratios, normalized_average_pass_yardages, normalized_qb_ratings
    counter = 0
    overall_score = 0
    for unit in norm_array:
        overall_score += (unit * weights_array[counter])
        counter += 1
    overall_score = overall_score / 7
    item.update({"overall_score": overall_score / 7})


overall_scores = [x["overall_score"] for x in qbs]
min_overall_scores = min(overall_scores)
max_overall_scores = max(overall_scores)

# normalize overall score between 50 and 100
for item in qbs:
    test_score = float(item["overall_score"]) * 7
    #print item["full_name"]
    #print test_score
    normalized_overall_score = (item["overall_score"] - min_overall_scores) / (max_overall_scores - min_overall_scores) * 50 + 50
    #item.update({"overall_score": test_score})
    item.update({"overall_score": normalized_overall_score})
    #print item["full_name"]
    #print normalized_overall_score

newlist = sorted(qbs, key=lambda k: k['overall_score'])
for item in newlist:
        print item["full_name"]
        print item["overall_score"]
