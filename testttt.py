#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import re
import time
import math
from decimal import *
string = """
javascript://route-redirect?route=/search/list/{slug}/{filters}/&page=2
"""

# a = 'Lot Size: 0.41 Acres'
# print(re.search("//route-redirect\?route=/search/list/{slug}/{filters}/&page=(\d+)", string).group(1))

# print(re.search("(\w+\s\w+)", string).group(1))

# b = 'NY 11803'
# print(re.search("\d+", b).group())
# exterior_features = "Built in: 1973                                Structure Type: House                                Lot Size: 1.5"
# exterior_features = "Built in: 1941                                Structure Type: House                                Lot Size: 1 Acre                                        Parking: 1 Space                    View Types:Exterior Keywords:Transaction Types:"
exterior_features = "Built in: 1950                                Structure Type: Multi-Family                                Lot Size: N/A                View Types:Exterior Keywords:"
lot_size = ""
#  109 Acres
num_unit = re.search("Lot Size:\s(\d+)\s\w+", exterior_features)
# Lot Size: 0.84 Acres
double_unit = re.search(r"Lot Size:\s(\d+.\d+)\s\w+", exterior_features)
# Lot Size: 90x140 Acres  40x100 Ft.
multi_num = re.search(r"Lot Size:\s(\d+)[x](\d+)\w+.", exterior_features)
# Lot Size: 1.5
double = re.search(r"Lot Size:\s(\d+\.\d)", exterior_features)
# Lot Size: 18,000 Sq. Ft.
sqft_lot_size = re.search(r"Lot Size:\s(\d+)\sSq. Ft.", exterior_features.replace(",", ""))
# Lot Size: 1 Acre
acre_lot_size = re.search(r"Lot Size:\s(\d+)\s\w+", exterior_features)
# Lot Size: N/A
acre_lot_size = re.search(r"Lot Size:\s(N/A)", exterior_features)

if exterior_features.find("Acres", 0, len(exterior_features)) > 0:
    if num_unit:
        lot_size = Decimal(num_unit.group(1)) * Decimal(43560)
    elif double_unit:
        lot_size = Decimal(double_unit.group(1)) * Decimal(43560)
elif double:
    lot_size = Decimal(double.group(1)) * Decimal(43560)
elif multi_num:
    multi_num_first = multi_num.group(1)
    multi_num_second = multi_num.group(2)
    lot_size = Decimal(multi_num_first) * Decimal(multi_num_second)
elif sqft_lot_size:
    lot_size = sqft_lot_size.group(1)
elif exterior_features.find("Acre", 0, len(exterior_features)) > 0:
    lot_size = Decimal(acre_lot_size.group(1)) * Decimal(43560)
elif acre_lot_size:
    lot_size = acre_lot_size.group(1)
    print(exterior_features)
print(lot_size)



