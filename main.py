import json
import csv
from functools import reduce

data = []
test_lines = 10

with open('911_Calls_for_Service.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # print(reader.fieldnames)  'zip_code' 'neighborhood'
    for row in reader:
        data.append(row)

# Remove rows with bad data in both zip_code and neighborhood, keep if either has data
non_blank_zips_neighborhoods = list(filter(lambda x: x["zip_code"] != "0" or x["neighborhood"] not in ['', ' ', '\n', None], data))
print(f"Total Non-blank locational services: {len(non_blank_zips_neighborhoods)}\n")

# average total response time - Step-by-step vs. reduce
print("Average Total Response Time: Step-by-step")
trt = 0
num = 0
for row in non_blank_zips_neighborhoods:
    val = row["totalresponsetime"]
    if val not in [None, '', ' ']:
        trt += float(val)
        num += 1

print(trt)
print(num)
print(trt/num)

print("\nAverage Total Response Time: Filter Method")

valid_trt_list = list(filter(lambda row: row["totalresponsetime"] not in [None, '', ' '], non_blank_zips_neighborhoods))
summed_trt = reduce(lambda row1, row2: row1 + float(row2["totalresponsetime"]), valid_trt_list, 0)
num_trt = len(valid_trt_list)

print(summed_trt)
print(num_trt)
print(summed_trt/num_trt)
print("")

# -

# average dispatch time - Step-by-step vs. reduce
print("Average Dispatch Time: Step-by-step")

dt = 0
num = 0
for row in non_blank_zips_neighborhoods:
    if row["dispatchtime"] not in [None, '', ' ']:
        dt += float(row["dispatchtime"])
        num += 1

print(dt)
print(num)
print(dt/num)

print("\nAverage Dispatch Time: Filter Method")

valid_dt_list = list(filter(lambda row: row["dispatchtime"] not in [None, '', ' ', '\n'], non_blank_zips_neighborhoods))
summed_dt = reduce(lambda row1, row2: row1 + float(row2["dispatchtime"]), valid_dt_list, 0)
num_dt = len(valid_dt_list)

print(summed_dt)
print(num_dt)
print(summed_dt/num_dt)
print("")

# -

# average total time
print("Average Total Time: Step-by-step")

tt = 0
num = 0
for row in non_blank_zips_neighborhoods:
    if row["totaltime"] not in [None, '', ' ']:
        tt += float(row["totaltime"])
        num += 1

print(tt)
print(num)
print(tt/num)

print("\nAverage Total Time: Filter Method")

valid_tt_list = list(filter(lambda row: row["totaltime"] not in [None, '', ' ', '\n'], non_blank_zips_neighborhoods))
summed_tt = reduce(lambda row1, row2: row1 + float(row2["totaltime"]), valid_tt_list, 0)
num_tt = len(valid_tt_list)

print(summed_tt)
print(num_tt)
print(summed_tt/num_tt)
print("")

# -

# Model of Neighborhood

nb_data_cln1 = list(filter(lambda row: row["neighborhood"] not in [None, '', ' ', '\n'], non_blank_zips_neighborhoods))
nb_data_cln2 = list(filter(lambda row: row["totalresponsetime"] not in [None, '', ' ', '\n'], nb_data_cln1))
nb_data_cln3 = list(filter(lambda row: row["dispatchtime"] not in [None, '', ' ', '\n'], nb_data_cln2))
nb_data_cleaned = list(filter(lambda row: row["totaltime"] not in [None, '', ' ', '\n'], nb_data_cln3))


nbs = list(set(row["neighborhood"] for row in nb_data_cleaned))

neighborhoods_dict = {}
for nb in nbs:
    nb_list = list(filter(lambda row: row["neighborhood"] == nb, nb_data_cleaned))
    neighborhoods_dict[nb] = nb_list

# avg total response time per nb, avg dispatch time per nb, avg total time per nb as list of dictionaries
neighborhoods_averages = {}
for nb in sorted(neighborhoods_dict):
    print(nb)
    summed_nb_trt = reduce(lambda row1, row2: row1 + float(row2["totalresponsetime"]), neighborhoods_dict[nb], 0)
    nb_trt_len = len(neighborhoods_dict[nb])
    avg_trt = summed_nb_trt / nb_trt_len
    print("Average Total Response Time: " + str(avg_trt))

    summed_nb_dt = reduce(lambda row1, row2: row1 + float(row2["dispatchtime"]), neighborhoods_dict[nb], 0)
    nb_dt_len = len(neighborhoods_dict[nb])
    avg_dt = summed_nb_dt / nb_dt_len
    print("Average Dispatch Time: " + str(avg_dt))

    summed_nb_tt = reduce(lambda row1, row2: row1 + float(row2["totaltime"]), neighborhoods_dict[nb], 0)
    nb_tt_len = len(neighborhoods_dict[nb])
    avg_tt = summed_nb_tt / nb_tt_len
    print("Average Total Time: " + str(avg_tt) + "\n")

    neighborhoods_averages[nb] = {"Average Total Response Time": avg_trt, "Average Dispatch Time": avg_dt, "Average Total Time": avg_tt}

with open("output_file.txt", 'w') as outfile:
    # json.dump(json.dumps(neighborhoods_averages, indent=4), outfile)  # comes with text output, valid but not intended use
    json.dump(neighborhoods_averages, outfile)  # Intended function call to obtain desired JSON output
