import re
import pandas as pd
import csv
import inflect
from word2number import w2n

p = inflect.engine()

# Read data from file
with open('extract.txt', 'r') as f:
    data = f.read()

guarantor_ref_pattern = r'\b(Mr|Mrs|Dr|Ms|MrXs)\b((?:(?!\().)*)(?=\b(Mr|Mrs|Dr|Ms|MrXs)\b)' 
customer_name_pattern = r'(?<=[a-zA-Z0-9])\s*((?:Mr|Ms|Mrs)\.[a-zA-Z]+(?:\s[a-zA-Z]\s[a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+))'
guarantor_name_pattern = r"\)(?:\s+)((?:Mr|Ms|Mp|Dr|Miss|Mrs)\.?\s*\w+\s+(?:\w\.\s+)?\w+(?:\s+\w+)?)" 
monthly_principal_reduction_pattern = r"\((?:Monthly|Month|Monthly Principal)[^)]*?([\d\.]+\s?%)\)"
purchase_value_reduction_pattern =  r"\((?:Purchase|Purch|Purcha)[^)]*?([\d\.]+%)\)"
down_payment_regex = r'(?:\$|#)(.*?)%(.*?)%'
city_and_state_pattern = r"(?:[A-Za-z]+\s*[.,]\s*[A-Za-z]+)(?=\s*[$#])"
customer_ref_pattern = r"(?<=\n)(?:\d+\s*[A-Za-z]*\s*)+(?=\s*(?:Ms|Mr|Miss|Dr))"
total_interest_reduction_pattern = r"\((?:To|Tot|Total)[^)]*?([\d\.]+%)\)"



reduced_values = []
numerical_values = []
downPayment = []
loan_period = []
annual_interest = []

time_p = []
money_ = []
percentage_ = []
percentage_2nd = []
down_payment_load_period = re.findall(down_payment_regex,data.replace('\n',''), re.MULTILINE)
for item in down_payment_load_period:
    loan_ = item[0]
    tme = item[1]
    pattern = r'([a-z])([A-Z])'
    matches = re.findall(pattern, loan_)
    for match in matches:
        loan_ = loan_.replace(''.join(match), match[0] + ' ' + match[1])
    
    matches = re.findall(pattern, tme)
    for match in matches:
        tme = tme.replace(''.join(match), match[0] + ' ' + match[1])    
    text = loan_+" % "+tme
    data_1 = text.split("%")
    ds1 = data_1[0].split("AND")
    ds2 = data_1[1].split("AND")
    dollar_str, cent_str = ds1[0].split('Dollars and ')[0], ds1[0].split('Dollars and ')[1]
# Convert the dollar value to a numeric value using word2number
    dollar_num = w2n.word_to_num(dollar_str)
# Convert the cent value to a numeric value using word2number
    cent_num = w2n.word_to_num(cent_str.split("Cents")[0])
# Combine the dollar and cent values into a single float
    numeric_value = dollar_num + cent_num / 100.0
    money_.append("$ " +str(numeric_value))

    percentage_.append(str(w2n.word_to_num(ds1[1]))+"%")
    time_p.append(str(w2n.word_to_num(ds2[0].split("Years")[0]))+"  Years  ")
    # percentage_1 = w2n.word_to_num(ds2[1].split(".")[0])
    # percentage_2 = w2n.word_to_num(ds2[1].split(".")[1])
    # percentage_2nd.append(str(percentage_1)+"."+str(percentage_2)+" %")

    # # some calculation

    # num_1 = w2n.word_to_num(ds1[1])
    # time_1 = w2n.word_to_num(ds2[0].split("Years")[0])
    
    # # red_val = numeric_value-((num_1*numeric_value)/100)
    # # reduced_values.append(red_val)
    # downPayment.append(num_1)
    # loan_period.append(time_1)
    # percent_1 = percentage_1+(percentage_2/100)
    # annual_interest.append(percent_1)



def remove_first_words(text):
    pattern = re.compile(r'^(\s*\S+\s+)(\S{2,}\s+|\S\s+\S+\s+)', re.MULTILINE)
    return pattern.sub('', text)


pattern = re.compile(guarantor_ref_pattern, re.S)

matches = pattern.findall(data.replace('\n','X'))
print(len(matches))
# Remove initial names
required_substrings = []
for match in matches:
    title, guarantor_info, _ = match
    cleaned_info = remove_first_words(guarantor_info).strip()
    required_substrings.append(cleaned_info)

# print(required_substrings)

customer_reference = ["42Y52E52724272460 495"]
guarantor_reference = []

for cleaned_text in required_substrings:
    lines = cleaned_text.split('X')
    if len(lines) == 2:
        guarantor_reference.append(lines[0])
        customer_reference.append(lines[1])
    if len(lines) == 3:
        guarantor_reference.append(lines[0] + '' + lines[1])
        customer_reference.append(lines[2])
    elif len(lines) == 4:
        guarantor_reference.append(lines[0] + '' + lines[1])
        customer_reference.append(lines[2] + '' + lines[3])


def separate_names(name):
    name = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', name)
    return name
initial_names = re.findall(customer_name_pattern, data.replace('\n',''), re.MULTILINE)
customer_names = []
for name in initial_names:
    # Insert a space between two consecutive capital letters after the first name not working
    corrected_name = separate_names(name)
    customer_names.append(corrected_name)
# print(customer_names)

states = re.findall(city_and_state_pattern, data)
# print(city_and_state_pattern_list)
city_and_state_pattern_list = []
for c in states:
    if "," in c :
        dt = c.split(",")
    elif "." in c :
        dt = c.split(".")
    city_and_state_pattern_list.append(str(dt[0]+" , "+dt[1]).upper())
 
monthly_principal_reduction_pattern_list = re.findall(monthly_principal_reduction_pattern, data.replace('\n',''),re.MULTILINE)
total_interest_reduction_pattern_list = re.findall(total_interest_reduction_pattern, data.replace('\n',''),re.MULTILINE)
purchase_value_reduction_pattern_list = re.findall(purchase_value_reduction_pattern, data.replace('\n',''),re.MULTILINE)

g_n = re.findall(guarantor_name_pattern, data)
guarantor_name_pattern_list= []
for i in g_n:
    guarantor_name_pattern_list.append(i.replace('\n',''))
print(guarantor_name_pattern_list)



# # create a list of the lists
lists = [customer_reference, city_and_state_pattern_list, monthly_principal_reduction_pattern_list, guarantor_name_pattern_list,guarantor_reference,customer_names,total_interest_reduction_pattern_list,total_interest_reduction_pattern_list]

# find the maximum length of the lists and compile a string from each of them
max_length = max([len(lst) for lst in lists])


def replace_spaces_in_reference_numbers(strings_list):
    updated_strings = []
    for s in strings_list:
        updated_string = s.replace(" ", "   ")
        updated_strings.append(updated_string)
    return updated_strings

def format_name(name):
    name_parts = name.split('.')
    title = name_parts[0].upper()
    rest_of_name = '  '.join(name_parts[1].split(' ')).upper()
    formatted_name = f"{title}.{rest_of_name}"
    return formatted_name

def format_names_list(names_list):
    return [format_name(name) for name in names_list]


customer_reference = replace_spaces_in_reference_numbers(customer_reference)
customer_names = format_names_list(customer_names)
with open("output_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Customer Reference Number", "Customer Name", "City And State", "Purchase Value AND Down Payment", "Loan Period AND Annual Interest In Percentage", "Guarantor Name", "Guarantor Reference Number"])
    for i in range(max_length):
        if len(customer_reference) <= i:
            customer_reference_val = "NA"
        else:
            customer_reference_val = customer_reference[i]

        if len(customer_names) <= i:
            customer_names_val = "NA"
        else:
            customer_names_val = customer_names[i]

        if len(city_and_state_pattern_list) <= i:
            city_val = "NA"
        else:
            city_val = city_and_state_pattern_list[i]

        if len(purchase_value_reduction_pattern_list) <= i:
            purchase_value = "NA"
        else:
            purchase_value = purchase_value_reduction_pattern_list[i]

        if len(total_interest_reduction_pattern_list) <= i:
            total_value = "NA"
        else:
            total_value = total_interest_reduction_pattern_list[i]

        if len(guarantor_name_pattern_list) <= i:
            g_val = "NA"
        else:
            g_val = guarantor_name_pattern_list[i]

        if len(guarantor_reference) <= i:
            g_ref_val = "NA"
        else:
            g_ref_val = guarantor_reference[i]

# time_p = []
# money_ = []
# percentage_ = []
# percentage_2nd = []
        time_years = ""
        if len(time_p) <= i:
            time_years = "NA"
        else:
            time_years = time_p[i] 


        time_money_val = ""
        if len(money_) <= i:
            time_money_val = "NA"
        else:
            time_money_val = money_[i]  


        p1 = ""
        if len(percentage_) <= i:
            p1 = "NA"
        else:
            p1 = percentage_[i] 


        p2 = ""
        if len(percentage_2nd) <= i:
            p2 = "NA"
        else:
            p2 = percentage_2nd[i]            

        output_row = [customer_reference_val, customer_names_val, city_val,time_money_val +" AND "+p1, time_years+"  AND  "+p2, g_val, g_ref_val]
        writer.writerow(output_row)
