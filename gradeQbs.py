import csv

qbs = []
with open("data/Rating_Data.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        qbs.append({'full_name': row[0], 'passing_att': row[1],
                        'passing_cmp': row[2], 'passing_ints': row[3], 'passing_tds': row[4], 'passing_yds': row[5],
                        'rushing_att': row[6], 'rushing_yds': row[7], 'rushing_tds': row[8]})


qbs.pop(0)
# Stats -> cmp_percentage, td_int_ratio, yards_per_attempt, td_attempt_ratio, int_attempt_ratio
for item in qbs[1:]:
    cmp_percentage = float(item["passing_cmp"]) / float(item["passing_att"])
    td_int_ratio = float(item["passing_tds"]) / float(item["passing_ints"])
    yards_per_attempt = float(item["passing_yds"]) / float(item["passing_att"])
    td_attempt_ratio = float(item["passing_tds"]) / float(item["passing_att"])
    int_attempt_ratio = float(item["passing_ints"]) / float(item["passing_att"])
    average_pass_yardage = float(item["passing_yds"]) / float(item["passing_cmp"])

    qb_rating_calc_1 = (cmp_percentage - .3) / .2
    qb_rating_calc_2 = (yards_per_attempt - 3) / 4
    qb_rating_calc_3 = td_attempt_ratio / .05
    qb_rating_calc_4 = (.095 - int_attempt_ratio) / .04
    qb_rating = (qb_rating_calc_1 + qb_rating_calc_2 + qb_rating_calc_3 + qb_rating_calc_4) * 100 / 6

    item.update({"cmp_percentage": cmp_percentage, "td_int_ratio": td_int_ratio, "yards_per_attempt": yards_per_attempt, "td_attempt_ratio": td_attempt_ratio, "int_attempt_ratio": int_attempt_ratio, "average_pass_yardage": average_pass_yardage, "qb_rating": qb_rating})

    # normalize all stats between 0 and 100
print qbs[0]
