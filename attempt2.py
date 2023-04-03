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
customer_name_pattern = r'(?<=[a-zA-Z0-9])\s*((?:Mr|Ms|Mrs)\.\s?[a-zA-Z]+(?:\s[a-zA-Z]\s[a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+))'
guarantor_name_pattern = r"\)(?:\s+)((?:Mr|Ms|Mp|Dr|Miss|Mrs)\.?\s*\w+\s+(?:\w\.\s+)?\w+(?:\s+\w+)?)" 
monthly_principal_reduction_pattern = r"\((?:Monthly|Month|Monthly Principal)[^)]*?([\d\.]+\s?%)\)"
purchase_value_reduction_pattern =  r"\((?:Purchase|Purch|Purcha)[^)]*?([\d\.]+%)\)"
down_payment_regex = r'(?:\$|#|&)(.*?)%(.*?)%'
city_and_state_pattern = r"(?:[A-Za-z]+\s*[.,]\s*[A-Za-z]+)(?=\s*[$#&])"
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
    print(loan_)
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
    percentage_1 = w2n.word_to_num(ds2[1].split(".")[0])
    if "." in ds2[1] :
        percentage_2 = w2n.word_to_num(ds2[1].split(".")[1])
        percentage_2nd.append(str(percentage_1)+"."+str(percentage_2)+" %")
    else :
        percentage_2nd.append(w2n.word_to_num(ds2[1]))

    

    # some calculation
    numerical_values.append(numeric_value)
    num_1 = w2n.word_to_num(ds1[1])
    time_1 = w2n.word_to_num(ds2[0].split("Years")[0])
    
    # red_val = numeric_value-((num_1*numeric_value)/100)
    # reduced_values.append(red_val)
    downPayment.append(num_1)
    loan_period.append(time_1)
    percent_1 = percentage_1+(percentage_2/100)
    annual_interest.append(percent_1)



def remove_first_words(text):
    short_name = text[0:14]
    if 'X' in short_name:
        short_name= short_name.replace(' X ','')
        text  = short_name + text[14:]
    # print(text)
    pattern = re.compile(r'^(\s*\S+\s+)(\S{2,}\s+|\S\s+\S+\s+)', re.MULTILINE)
    return pattern.sub('', text)


pattern = re.compile(guarantor_ref_pattern, re.S)

matches = pattern.findall(data.replace('\n',' X '))

# print(matches)
# print(len(matches))
# Remove initial names
required_substrings = []
for match in matches:
    title, guarantor_info, _ = match
    cleaned_info = remove_first_words(guarantor_info).strip()
    # print(cleaned_info)
    required_substrings.append(cleaned_info)

# print(required_substrings)

customer_reference = ["V12 V 2 27 492 A5 49"]
guarantor_reference = []

for cleaned_text in required_substrings:
    lines = cleaned_text.split('X')
    # print(lines)
    if len(lines) == 2 :
        guarantor_reference.append(lines[0])
        customer_reference.append(lines[1])
    elif len(lines) ==3 and lines[2] == '':
        guarantor_reference.append(lines[0])
        customer_reference.append(lines[1])
    elif len(lines) == 3 :
        guarantor_reference.append(lines[0] + '' + lines[1])
        customer_reference.append(lines[2])
    elif len(lines) == 4:
        guarantor_reference.append(lines[0] + '' + lines[1])
        customer_reference.append(lines[2] + '' + lines[3])

def separate_names(name):
    name = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', name)
    return name
initial_names = re.findall(customer_name_pattern, data.replace('\n',''), re.MULTILINE)
print(initial_names)
# print(initial_names)
customer_names = []
for name in initial_names:
    # Insert a space between two consecutive capital letters after the first name not working
    corrected_name = separate_names(name)
    customer_names.append(corrected_name)
# print(customer_names)

states = re.findall(city_and_state_pattern, data)

# print(states)
city_and_state_pattern_list = []
for c in states:
    if "," in c :
        dt = c.split(",")
    elif "." in c :
        dt = c.split(".")
    city_and_state_pattern_list.append(str(dt[0]+" , "+dt[1]).upper())
# print(city_and_state_pattern_list)
monthly_principal_reduction_pattern_list = re.findall(monthly_principal_reduction_pattern, data.replace('\n',''),re.MULTILINE)
total_interest_reduction_pattern_list = re.findall(total_interest_reduction_pattern, data.replace('\n',''),re.MULTILINE)
purchase_value_reduction_pattern_list = re.findall(purchase_value_reduction_pattern, data.replace('\n',''),re.MULTILINE)
# print(purchase_value_reduction_pattern_list)

g_n = re.findall(guarantor_name_pattern, data)
guarantor_name_pattern_list= []
for i in g_n:
    guarantor_name_pattern_list.append(i.replace('\n',''))
# print(guarantor_name_pattern_list)



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
    title_pattern = r"^(Mrs|Mr|Ms|Dr|Miss|Prof)(?!\.)"

# Replace the matched title with the title followed by a period and space
    name = re.sub(title_pattern, r"\1. ", name)
    name_parts = name.split('.')
    if len(name_parts)==3:
        title = name_parts[0].upper() +name_parts[1].upper().lstrip()
        rest_of_name = '  '.join(name_parts[2].split(' ')).upper()
    else :
        title = name_parts[0].upper().lstrip()
        rest_of_name = '  '.join(name_parts[1].split(' ')).upper()

    
    formatted_name = f"{title}.{rest_of_name}"
    return formatted_name

def format_names_list(names_list):
    return [format_name(name) for name in names_list]


customer_reference = replace_spaces_in_reference_numbers(customer_reference)
customer_names = format_names_list(customer_names)
# print(guarantor_name_pattern_list)
guarantor_name_pattern_list = format_names_list(guarantor_name_pattern_list)
# print(guarantor_name_pattern_list)
guarantor_reference = replace_spaces_in_reference_numbers(guarantor_reference)

pmi = []
property_val=[]
interest_after_reductionss = []
loan_list = []
interest_per = []
loan_list_monthly = []
# reduced_values = []
# numerical_values = []
# downPayment = []
# loan_period = []
# annual_interest = []
# print(numerical_values)

def decimal_to_currency(value):
    # Format the value with commas as thousands separators and 2 decimal places
    formatted_value = "{:,.2f}".format(value)

    # Replace commas with ',  ' (comma followed by two spaces)
    formatted_value = formatted_value.replace(",", ",  ")

    # Add the dollar sign followed by a space at the beginning of the string
    formatted_value = "$  " + formatted_value

    return formatted_value

def pmi_insurance_rate(loan_p, loan_period):
    rate = "NA"
    if 0.01 <= loan_p <= 80:
        pass
    elif 80.01 <= loan_p <= 85:
        if 1 <= loan_period <= 20:
            rate = 0.19
        elif 21 <= loan_period <= 30:
            rate = 0.32
    elif 85.01 <= loan_p <= 90:
        if 1 <= loan_period <= 20:
            rate = 0.23
        elif 21 <= loan_period <= 30:
            rate = 0.52
    elif 90.01 <= loan_p <= 95:
        if 1 <= loan_period <= 20:
            rate = 0.26
        elif 21 <= loan_period <= 30:
            rate = 0.78
    elif 95.01 <= loan_p <= 97:
        if 1 <= loan_period <= 20:
            rate = 0.79
        elif 21 <= loan_period <= 30:
            rate = 0.90
    elif 97.01 <= loan_p <= 100:
        pass

    return rate

def property_insurance_rate(loan_p, loan_period):
    rate = 0

    if 0.01 <= loan_p <= 84.99:
        if 1 <= loan_period <= 25:
            rate = 0.32
        elif 26 <= loan_period <= 30:
            rate = 0.32
    elif loan_p == 85:
        if 1 <= loan_period <= 25:
            rate = 0.21
        elif 26 <= loan_period <= 30:
            rate = 0.32
    elif 85.01 <= loan_p <= 90:
        if 1 <= loan_period <= 25:
            rate = 0.41
        elif 26 <= loan_period <= 30:
            rate = 0.52
    elif 90.01 <= loan_p <= 95:
        if 1 <= loan_period <= 25:
            rate = 0.67
        elif 26 <= loan_period <= 30:
            rate = 0.78
    elif 95.01 <= loan_p <= 100:
        rate = "NA"

    return rate

for i in range(0,len(numerical_values)):
    red_percent = float(purchase_value_reduction_pattern_list[i].split("%")[0])
    mon_percent = float(monthly_principal_reduction_pattern_list[i].split("%")[0])
    tot_percent = float(total_interest_reduction_pattern_list[i].split("%")[0])
    if(red_percent>100):
        red_percent/=100
    if(mon_percent>100):
        mon_percent/=100
    if(tot_percent>100):
        tot_percent/=100
    # print(str(numerical_values[i])+"-"+str(red_percent)+"*"+str(numerical_values[i]))                
    reduced_value = numerical_values[i]-(numerical_values[i]*(red_percent/100))
    reduced_values.append(reduced_value)
    down_payment_value = reduced_value-(reduced_value*(downPayment[i]/100))
    loan_list.append(down_payment_value)
    loan_amount = down_payment_value/(loan_period[i]*12)
    loan_amount =  (loan_amount*(mon_percent/100))
    loan_list_monthly.append(loan_amount)
    interest_ = down_payment_value*(annual_interest[i]/100)
    interest_after_reduction = (interest_*tot_percent/100)*loan_period[i]
    interest_after_reductionss.append(interest_after_reduction)
    roi = 0.0
    loan_p = 100-float(percentage_[i].split("%")[0])
    rate = property_insurance_rate(loan_p,loan_period[i])
    if rate != "NA":
        property_val.append((loan_list[i]*rate)/1200)
    else :
        property_val.append("NA")
    rate_pmi = pmi_insurance_rate(loan_p,loan_period[i])
    if rate_pmi != "NA":
        pmi.append((loan_list[i]*rate)/100)
    else :
        pmi.append("NA")
# print(reduced_values)
# print(loan_list)
# print(loan_list_monthly)
# print(interest_after_reductionss)

# print(max_length)
# print(len(city_and_state_pattern_list))
with open("output_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Customer Reference Number", "Customer Name", "City And State", "Purchase Value AND Down Payment", "Loan Period AND Annual Interest In Percentage", "Guarantor Name", "Guarantor Reference Number","Loan amount AND Principal" ,"Total Interest for Loan period and Property TAX for Loan Period","Property Insurance Per Month and PMI per annum"])
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
            # print(str(i))
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

             
        final_red = ""
        if len(reduced_values) <= i:
            final_red = "NA"
        else:
            final_red = decimal_to_currency(reduced_values[i])


        final_loan = ""
        if len(loan_list) <= i:
            final_loan = "NA"
        else:
            final_loan = decimal_to_currency(loan_list[i])

        
        principal = ""
        if len(loan_list_monthly) <= i:
            principal = "NA"
        else:
            principal = decimal_to_currency(loan_list_monthly[i])

        final_interest = ""
        if len(interest_after_reductionss) <= i:
            final_interest = "NA"
        else:
            final_interest = decimal_to_currency(interest_after_reductionss[i])
        
        
        pmi_value = ""
        if len(pmi) <= i or pmi[i]=="NA":
            pmi_value = "NA"
        else:
            pmi_value = decimal_to_currency(pmi[i])

        prop_val = ""
        if len(property_val) <= i or property_val[i]=="NA":
            prop_val = "NA"
        else:
            prop_val = decimal_to_currency(property_val[i])
        
        output_row = [customer_reference_val, 
        customer_names_val,
         city_val, final_red+
         " AND "+p1,
         time_years+"  AND  "+ str(p2), 
         g_val,
          g_ref_val,
          final_loan+" AND "+principal
          ,final_interest+" AND "+ "NA",prop_val+" AND "+pmi_value]

        writer.writerow(output_row)
