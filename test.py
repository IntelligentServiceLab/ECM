import csv

import numpy as np
from numpy.core.fromnumeric import choose
import pandas as pd
import random
import os
import time
import random as rdn
import queue
from numpy.core.numeric import Inf, Inf

def a_star():
    # taxiIo = 'D:/Workspaces/ECM/yhfexp/yhfexp/yhf/data/Taxi_070220/Taxi_105'

    # stationsIo = 'D:/Workspaces/ECM/yhfexp/yhfexp/yhf/data/station3000.csv'
    # # stationsIo = '..\..\..\..\data\station1000.csv'
    # stationsIo = '..\..\..\..\data\station2000.csv'

    # taxiIo = 'D:/Workspaces/ECM/yhfexp/yhfexp/yhf/data/beijing_user_final_data.csv'
    # stationsIo = 'D:/Workspaces/ECM/yhfexp/yhfexp/yhf/data/beijing_station_final_data.csv'
    taxiIo = 'beijing_user_final_data.csv'
    stationsIo = 'beijing_station_final_data.csv'

    # stations = pd.read_csv(stationsIo, usecols=[0, 1],
    #                        names=['latitude', 'lontitude'])
    stations = pd.read_csv(stationsIo, usecols=[1, 2])
    b = open(taxiIo)
    b.readline()
    taxi = []
    for a in b:
        a = a.split(",")
        a = a[2:4]
        # del a[0:2]
        # del a[-3]
        # del a[-2]
        # del a[-1]
        for i in range(len(a)):
            a[i] = float(a[i])
        # a[0], a[1] = a[1], a[0]
        taxi.append(a)
    # taxi = taxi[1:]

    star = rdn.randint(0, len(taxi)-10)
    # star = 10
    startpoint = taxi[star]
    endpoint = taxi[star+rdn.randint(150, 200)]
    # endpoint = taxi[20]
    need = random.random() * 20 + 10


    def dist(x, y):
        return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


    station_dict={}
    station_pos2id={}
    filtered_stations = []
    for i in range(len(stations)):

        x = stations.loc[i]
        station_dict[str(i)] = []

        xy = []
        for j in x:
            xy.append(float(j))
            station_dict[str(i)].append(float(j))
            pos=str(np.array(station_dict[str(i)]))
            station_pos2id[pos]=i
        filtered_stations.append(xy)
    filtered_stations.pop(0)

    tmin = tmax = float()
    pmin = 0.5
    pmax = 1
    for s in filtered_stations:
        for st in filtered_stations:
            tmin = min(tmin, dist(s, st))
            tmax = max(tmax, dist(s, st))

    C = np.zeros(
        shape=(len(filtered_stations), len(filtered_stations)))
    B = np.zeros(
        shape=(len(filtered_stations), len(filtered_stations)))
    T = np.zeros(
        shape=(len(filtered_stations), len(filtered_stations)))
    P = np.zeros(
        shape=(len(filtered_stations), len(filtered_stations)))
    L = np.zeros(
        shape=(len(filtered_stations)))

    for i in range(len(filtered_stations)):
        L[i] = 10+20*random.random()
        for j in range(len(filtered_stations)):
            tij = dist(filtered_stations[i], filtered_stations[j])
            tij = (tij-tmin)/(tmax-tmin)
            T[i][j] = tij

        for j in range(len(filtered_stations)):
            pij = 0.5*random.random()+0.5
            pij = (pij-pmin)/(pmax-pmin)
            P[i][j] = pij
    # print(P)
    for m in range(len(B)):
        for n in range(len(B[0])):
            B[m][n] = 6*random.random()+4

    for m in range(len(T)):
        for n in range(len(T[0])):
            C[m][n] = 0.9*T[m][n] + 0.1*P[m][n]

    choose_station = list(filtered_stations)
    cacl = 10+random.random()*20

    sourceES = [Inf, Inf]
    sourceID = int()
    targetES = [Inf, Inf]
    targetID = int()
    found_start=False
    found_end=False
    for i in range(len(filtered_stations)):
        if not found_start:
            if dist(startpoint, filtered_stations[i]) < dist(startpoint, sourceES) and L[i] >= need:
                sourceES = filtered_stations[i]
                sourceID = i
                # found_start=True
        if not found_end:
            if dist(endpoint, filtered_stations[i]) < dist(endpoint, targetES) and L[i] >= need:
                targetES = filtered_stations[i]
                targetID = i
                # found_end=True
        if found_start and found_end:
            break
    print(startpoint, sourceES, sourceID)
    print(endpoint, targetES, targetID)
    b = Inf
    q = random.random()*8
    t = float()
    # A*
    networkCost = 0
    start_time = time.clock()
    frontier = queue.PriorityQueue()
    frontier.put((0, [sourceES, sourceID]))
    came_from = dict()
    cost_so_far = dict()
    came_from[sourceID] = None
    cost_so_far[sourceID] = 0
    answer = []
    while not frontier.empty():
        current = frontier.get()[1]
        answer.append(current)
        if current[1] == targetID:
            break
        for i in range(len(filtered_stations)):
            if filtered_stations[i] == current:
                continue
            new_cost = cost_so_far[current[1]] + C[current[1], i]
            if i not in cost_so_far:
                cost_so_far[i] = new_cost
                priority = new_cost + C[i][targetID]
                frontier.put((priority, [filtered_stations[i], i]))
                came_from[i] = current[1]
    calc_time = (time.clock()-start_time)
    print("end")

    a_starList=[]
    for i in range(len(answer) - 1):
        a_starList.append(answer[i][1])
        b = min(b, B[answer[i][1]][answer[i + 1][1]])
        networkCost=networkCost+ C[answer[i][1]][answer[i + 1][1]]
    t = q/b

    with open("Astar.txt" ,'w') as f:
        f.write(str(a_starList))
    print("a* is:",a_starList)
    print("answer is:",answer)
    print("networkCost:", networkCost)
    return answer,networkCost,station_dict,station_pos2id,C

    print("传输时间：", t)

    print("计算时间：", calc_time)

if __name__=="__main__":
    def calcCost(cost,road):
        c=0
        for i in range(len(road)-1):
            c=c+cost[road[i]][road[i+1]]
        return c


    # networkCost: 94.21208510408806
    lista=[1172, 1691, 1947, 1290, 768, 1039, 1451, 1076, 933, 1703, 703, 2436, 2145, 1420, 1145, 1341, 1446, 519, 1334, 2239, 895, 2125, 2714, 2684, 1782, 560, 1298, 658, 1752, 1626, 2595, 2041, 1728, 1611, 2458, 811, 1351, 596, 1205, 618, 1566, 1376, 1185, 1077, 2228, 526, 1789, 2345, 476, 2381, 1419, 681, 470, 1563, 1261, 1894, 1291, 2723, 678, 1435, 2612, 2604, 1304, 1381, 708, 2650, 1055, 92, 1294, 1911, 1395, 1629, 2482, 934, 2194, 1428, 2358, 2694, 1634, 2342, 2013, 1891, 1582, 2003, 1410, 2499, 2702, 825, 270, 1372, 2087, 1247, 1151, 820, 1046, 2674, 2203, 2445, 160, 2554, 2107, 1345, 2331, 1296, 421, 1709, 2421, 466, 2112, 2052, 2116, 1241, 504, 1143, 518, 1301, 2286, 1973, 2384, 1342, 542, 1481, 1009, 1718, 234, 532, 1679, 686, 1900, 1270, 1969, 1979, 1118, 1388, 1465, 1128, 1012, 997, 2218, 1025, 2161, 1004, 142, 348, 2141, 416, 2323, 887, 1638, 196, 2243, 1484, 962, 797, 1586, 500, 281, 780, 2413, 387, 1404, 1360, 291, 640, 1433, 555, 1243, 551, 2372, 1677, 241, 514, 792, 1941, 189, 296, 1646, 2677, 1477, 2510, 929, 2641, 478, 2536, 675, 1514, 1987, 1810, 2272, 1357, 2071, 1459, 767, 2113, 335, 599, 597, 472, 2255, 989, 1678, 1879, 2449, 2042, 585, 791, 1235, 1822, 300, 2159, 1003, 2538, 218, 130, 1812, 766, 522, 907, 2325, 2417, 1627, 1354, 2269, 855, 2676, 1983, 1138, 493, 2366, 1760, 1411, 1599, 2374, 955, 1901, 2516, 1770, 1922, 2483, 187, 1069, 2585, 1595, 808, 2746, 47, 1319, 2348, 2317, 347, 798, 1881, 152, 1757, 425, 720, 778, 124, 2547, 641, 2579, 1785, 2553, 636, 920, 1961, 1014, 2213, 283, 1635, 885, 1797, 2727, 473, 1238, 1211, 475, 1952, 418, 144, 757, 1953, 1335, 1031, 2185, 722, 21, 615, 653, 2701, 2408, 2048, 949, 2130, 1885, 219, 2578, 1213, 2149, 1038, 709, 1167, 845, 1283, 589, 1183, 1556, 2070, 1527, 1286, 507, 1445, 372, 1749, 1324, 2193, 2481, 1630, 2375, 2669, 2189, 2503, 586, 1606, 697, 2659, 1202, 1531, 742, 2542, 2169, 2460, 2280, 1111, 1741, 1666, 1048, 2140, 1313, 1591, 799, 1472, 2368, 982, 1642, 2122, 1141, 2137, 1405, 2708, 1392, 857, 1938, 1396, 1378, 2442, 831, 433, 25, 1930, 1819, 1880, 981, 659, 314, 1775, 1229, 332, 603, 1476, 1479, 975, 88, 365, 1673, 400, 1742, 156, 179, 968, 2376, 1730, 2624, 938, 1931, 2044, 1848, 1690, 872, 1546, 1942, 1547, 861, 1489, 1005, 2294, 2327, 2411, 2522, 108, 1119, 2089, 1182, 1322, 1251, 1188, 1041, 339, 959, 2166, 1631, 1263, 793, 378, 2120, 2241, 2388, 2167, 1784, 1802, 1181, 16, 2199, 2353, 2056, 1865, 2053, 362, 2424, 1548, 523, 1539, 229, 1457, 1116, 1499, 2469, 1645, 2473, 1722, 980, 1889, 2409, 173, 325, 2661, 718, 1838, 2264, 948, 146, 1510, 1132, 821, 2419, 2492, 1914, 2490, 2216, 1081, 2679, 1470, 726, 2321, 2236, 1310, 844, 2095, 2518, 2066, 1114, 1358, 1348, 1258, 802, 2397, 455, 63, 2215, 516, 380, 2160, 424, 1672, 926, 1854, 1170, 2495, 1688, 1585, 2024, 998, 2452, 2605, 1429, 2546, 1054, 2170, 2324, 545, 1533, 2341, 1292, 1052, 1664, 2485, 430, 154, 385, 14, 1485, 992, 1710, 2563, 284, 2401, 2706, 1986, 1071, 1549, 945, 1239, 2277, 2378, 1994, 326, 485, 1769, 2734, 394, 1105, 2260, 1177, 1331, 245, 2172, 1299, 2362, 987, 748, 947, 42, 919, 459, 2252, 663, 1974, 841, 544, 2224, 2690, 764, 1273, 1603, 1464, 2655, 1554, 2134, 991, 2446, 691, 1522, 672, 569, 2035, 2438, 2190, 1257, 1771, 2652, 498, 1366, 1240, 40, 1330, 2725, 1686, 1715, 1886, 452, 1255, 874, 334, 1811, 1121, 2635, 1723, 921, 993, 2275, 489, 2032, 1774, 2279, 1933, 2402, 756, 2036, 2119, 2441, 1960, 979, 647, 2556, 1608, 2288, 2022, 2738, 598, 103, 2270, 1995, 574, 1616, 1897, 1136, 2744, 1735, 2728, 1976, 952, 803, 1072, 1980, 1970, 1637, 2591, 2257, 2486, 1204, 2281, 2423, 29, 739, 2711, 1671, 165, 1875, 1373, 1320, 2079, 833, 517, 1082, 2211, 2527, 1496, 1303, 1413, 1555, 1461, 1835, 258, 169, 2745, 1551, 1505, 543, 2069, 2599, 1767, 1425, 2545, 765, 2318, 1203, 1687, 1935, 2171, 1765, 957, 2425, 728, 2182, 1649, 1864, 2583, 2689, 1619, 2609, 269, 2029, 1859, 520, 1559, 996, 10, 616, 1448, 575, 1513, 617, 2387, 661, 2011, 2091, 2552, 2084, 674, 228, 267, 434, 1614, 1026, 2525, 2747, 312, 2322, 2562, 625, 866, 590, 651, 511, 2618, 2340, 367, 738, 546, 644, 65, 2031, 878, 1386, 264, 1553, 1148, 447, 2570, 81, 2476, 1492, 1991, 1224, 2100, 1654, 2606, 101, 360, 205, 222, 512, 214, 320, 2418, 1201, 1902, 2200, 2209, 2092, 1967, 1694, 1112, 68, 1888, 2515, 340, 1402, 203, 576, 280, 815, 577, 2038, 233, 117, 2267, 1080, 1884, 1001, 868, 1575, 393, 2121, 1602, 898, 375, 963, 760, 930, 1656, 122, 1361, 565, 2743, 432, 2058, 2666, 467, 822, 813, 614, 1088, 1746, 2634, 2558, 2068, 2208, 897, 263, 1779, 451, 1989, 413, 1502, 2083, 317, 1503, 1721, 2178, 1036, 925, 2005, 1500, 2156, 922, 1173, 51, 1844, 28, 1237, 2596, 457, 812, 1520, 1271, 2109, 761, 2646, 1137, 2665, 1904, 308, 572, 2420, 1144, 406, 2315, 200, 2248, 2471, 2721, 33, 1932, 671, 2621, 964, 950, 2229, 2479, 2299, 2133, 247, 1787, 1053, 2047, 2733, 1693, 2306, 1504, 1353, 967, 327, 1561, 1817, 239, 1207, 850, 164, 469, 1364, 966, 1913, 752, 2737, 2007, 685, 2390, 2541, 1265, 2333, 1368, 879, 1250, 2603, 208, 279, 696, 759, 1377, 328, 1329, 71, 2696, 1062, 1878, 2611, 1339, 1990, 2343, 2192, 2380, 1516, 843, 904, 2463, 304, 2026, 1971, 22, 2477, 1106, 1843, 1127, 1783, 770, 536, 1217, 1791, 2592, 319, 366, 1176, 2300, 480, 688, 159, 564, 1168, 1122, 2086, 896, 541, 129, 914, 2206, 899, 1813, 2732, 369, 2251, 1216, 2642, 2532, 17, 713, 1439, 2600, 1282, 1110, 1719, 958, 2645, 2399, 2489, 1526, 1174, 2010, 719, 1040, 2009, 1681, 877, 1862, 2115, 2671, 1850, 1612, 1397, 2632, 261, 1317, 1618, 1423, 721, 1307, 1028, 1968, 533, 1550, 1744, 1828, 313, 1896, 2693, 302, 1444, 1714, 172, 2406, 946, 2432, 1536, 2724, 525, 550, 48, 199, 1453, 1120, 1197, 579, 2039, 186, 1829, 1367, 1705, 458, 1570, 1762, 2188, 1186, 2146, 175, 1521, 736, 1768, 1589, 43, 2265, 1597, 2183, 1737, 86, 737, 1956, 972, 783, 1834, 94, 2127, 2361, 2462, 2474, 1044, 936, 477, 465, 1906, 1633, 634, 13, 566, 364, 212, 1761, 1552, 679, 1866, 699, 2435, 30, 1748, 2114, 683, 252, 747, 2004, 1352, 527, 573, 1034, 210, 706, 1624, 790, 1668, 330, 277, 26, 974, 1164, 859, 464, 1912, 832, 135, 559, 2297, 2594, 1466, 2377, 1825, 2153, 549, 1517, 1206, 461, 2439, 2586, 170, 1278, 749, 680, 1371, 581, 2310, 642, 1698, 2364, 2472, 1530, 2163, 531, 570, 2025, 1498, 754, 2494, 1152, 2687, 2308, 995, 630, 990, 883, 1107, 700, 2617, 2526, 1109, 1387, 1601, 1625, 1086, 1579, 125, 1191, 52, 2237, 1955, 445, 1149, 2529, 2240, 1921, 1029, 601, 1965, 1198, 1226, 510, 143, 2050, 643, 153, 1297, 1469, 148, 580, 410, 1494, 932, 2103, 1773, 237, 479, 1926, 1060, 343, 440, 771, 657, 1882, 2244, 2187, 204, 171, 769, 256, 1872, 1409, 1680, 1857, 2105, 1311, 2648, 1375, 381, 716, 174, 1532, 1475, 1590, 1758, 528, 2502, 2195, 2572, 415, 1663, 561, 746, 2014, 2431, 2524, 595, 2568, 858, 1349, 1275, 2016, 622, 1380, 2207, 1998, 316, 1560, 2075, 2293, 2304, 2630, 1636, 1338, 1806, 1984, 1519, 2019, 1125, 609, 1795, 2716, 411, 287, 1794, 1584, 1147, 1139, 2234, 2385, 537, 1115, 1355, 15, 1101, 119, 978, 1793, 1000, 1944, 1214, 1632, 1486, 969, 474, 2088, 213, 185, 1389, 2567, 1165, 1745, 288, 2456, 2094, 2601, 2082, 2232, 587, 188, 98, 428, 772, 994, 1316, 431, 710, 274, 1050, 1277, 2076, 1356, 2710, 2135, 1006, 1154, 1091, 1431, 1013, 530, 2198, 2587, 1130, 113, 1985, 2351, 582, 2142, 1269, 1432, 1662, 1720, 2311, 444, 2226, 2363, 629, 1583, 1605, 2508, 1876, 632, 1033, 161, 83, 1869, 306, 404, 176, 483, 2262, 1262, 1159, 2006, 2513, 1572, 1084, 2412, 1657, 1295, 670, 1272, 840, 1975, 2111, 2451, 2484, 1495, 2576, 2686, 2273, 1369, 1804, 1786, 322, 1020, 776, 2663, 1920, 2051, 1726, 1094, 1458, 1665, 1302, 1027, 1936, 712, 1707, 1326, 1600, 2749, 450, 786, 2227, 535, 1651, 1940, 2181, 1892, 750, 509, 2023, 286, 2222, 743, 1135, 2731, 1100, 2059, 1436, 2699, 1650, 2590, 2077, 547, 1569, 2531, 2285, 1242, 2544, 1846, 2102, 1647, 2507, 392, 2700, 158, 1943, 1021, 1193, 2316, 1166, 627, 271, 2564, 2625, 818, 890, 338, 96, 1963, 12, 916, 2158, 290, 1434, 2204, 781, 2740, 1160, 773, 1704, 114, 44, 1208, 2284, 619, 1267, 2444, 1613, 2289, 2046, 2697, 1315, 905, 1731, 2249, 491, 1483, 2258, 928, 115, 2750, 1727, 2498, 1244, 2106, 1855, 1905, 1717, 1456, 1999, 333, 2336, 2110, 785, 1895, 1873, 1509, 592, 1493, 611, 2150, 268, 1558, 937, 1660, 1815, 1382, 1993, 1805, 1190, 1523, 1407, 973, 2533, 1218, 118, 2055, 1874, 986, 2338, 2561, 45, 613, 255, 2539, 860, 324, 2090, 1733, 796, 1596, 2132, 1153, 2465, 2478, 272, 423, 223, 2008, 684, 774, 1708, 819, 1929, 2346, 95, 1285, 662, 2751, 1422, 1253, 1871, 2644, 940, 607, 1343, 1108, 2616, 939, 1073, 89, 1117, 621, 1734, 1604, 888, 724, 41, 775, 2098, 217, 635, 39, 2124, 1222, 2405, 1661, 2359, 2078, 1958, 2520, 1641, 23, 2220, 2332, 704, 232, 371, 1867, 1837, 492, 1808, 2355, 1426, 1385, 717, 2136, 2427, 1937, 1161, 162, 139, 1178, 468, 2497, 588, 558, 727, 1796, 382, 2367, 1079, 1506, 2339, 1325, 211, 1042, 1833, 838, 2660, 167, 871, 608, 2320, 1538, 1639, 956, 2337, 508, 435, 521, 136, 865, 2379, 2018, 1150, 954, 1274, 1393, 184, 1909, 2575, 482, 1711, 54, 935, 454, 694, 1740, 1051, 1126, 1861, 384, 2426, 2291, 1463, 1780, 341, 1948, 740, 853, 1996, 352, 762, 2000, 1362, 2373, 2720, 2651, 1945, 917, 194, 1490, 2620, 1587, 689, 1670, 70, 1102, 345, 397, 2555, 2179, 151, 2428, 149, 1418, 1609, 1124, 443, 2748, 909, 1598, 73, 1245, 1187, 1192, 1849, 1163, 1997, 282, 1365, 562, 1223, 1408, 1333, 163, 1518, 1863, 1210, 1249, 624, 157, 2155, 2729, 2101, 779, 1487, 436, 2683, 1524, 1212, 2735, 646, 87, 2569, 132, 2709,1288]
    listb=[1172, 2225, 1895, 244, 0, 1505, 1289, 1133, 1288]
    listc=[1172,1288]
    # networkCost is:0.8822605677206579
    _,_,_,_,C=a_star()
    print("a_star:",str(calcCost(C,lista)))
    print("RL:",str(calcCost(C,listb)))
    print("direcr:",str(calcCost(C,listc)))