EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 7800 5000 0    60   Italic 0
Thru-Hole Connector
$Comp
L Connector:4P4C J1
U 1 1 612DA9FB
P 4950 2800
F 0 "J1" H 5007 3267 50  0000 C CNN
F 1 "4P4C" H 5007 3176 50  0000 C CNN
F 2 "Connector_RJ:RJ14_Connfly_DS1133-S4_Horizontal" V 4950 2850 50  0001 C CNN
F 3 "~" V 4950 2850 50  0001 C CNN
	1    4950 2800
	1    0    0    -1  
$EndComp
$Comp
L RPi_Hat:RPi_GPIO J2
U 1 1 5516AE26
P 7500 2700
AR Path="/5516AE26" Ref="J2"  Part="1" 
AR Path="/5515D395/5516AE26" Ref="J2"  Part="1" 
F 0 "J2" H 8250 2950 60  0000 C CNN
F 1 "RPi_GPIO" H 8250 2850 60  0000 C CNN
F 2 "RPi_Hat:Pin_Header_Straight_2x20" H 7500 2700 60  0001 C CNN
F 3 "" H 7500 2700 60  0000 C CNN
	1    7500 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 3200 7300 3200
Wire Wire Line
	9550 2400 9550 3400
Wire Wire Line
	9550 3400 9200 3400
Wire Wire Line
	6750 3450 6750 4100
Wire Wire Line
	6750 4100 7300 4100
Wire Wire Line
	6250 3300 7300 3300
$Comp
L Device:C C2
U 1 1 61648B12
P 6750 4350
F 0 "C2" H 6865 4396 50  0000 L CNN
F 1 "C 1uF" H 6865 4305 50  0000 L CNN
F 2 "Capacitor_THT:C_Rect_L11.0mm_W3.4mm_P10.00mm_MKT" H 6788 4200 50  0001 C CNN
F 3 "~" H 6750 4350 50  0001 C CNN
	1    6750 4350
	1    0    0    -1  
$EndComp
Connection ~ 6750 4200
Wire Wire Line
	6750 4200 7300 4200
$Comp
L Device:C C1
U 1 1 616494FC
P 6400 4450
F 0 "C1" H 6515 4496 50  0000 L CNN
F 1 "C 1uF" H 6515 4405 50  0000 L CNN
F 2 "Capacitor_THT:C_Rect_L11.0mm_W3.4mm_P10.00mm_MKT" H 6438 4300 50  0001 C CNN
F 3 "~" H 6400 4450 50  0001 C CNN
	1    6400 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 4500 6750 4600
Connection ~ 6750 4600
Wire Wire Line
	6750 4600 7300 4600
Wire Wire Line
	5850 4600 6400 4600
Wire Wire Line
	9550 2400 5850 2400
Wire Wire Line
	5850 2400 5850 2900
Wire Wire Line
	5850 2900 5350 2900
Wire Wire Line
	6200 2700 5350 2700
Wire Wire Line
	6200 2700 6200 3200
Wire Wire Line
	6250 2600 5350 2600
Wire Wire Line
	6250 2600 6250 3300
Wire Wire Line
	6100 3400 6100 2800
Wire Wire Line
	6100 2800 5350 2800
Wire Wire Line
	5350 4300 5850 4300
Wire Wire Line
	5350 3550 5850 3550
Connection ~ 6400 4600
Wire Wire Line
	6400 4600 6750 4600
Wire Wire Line
	6400 4300 6400 3450
Wire Wire Line
	6400 3450 6750 3450
$Comp
L Connector:4P4C J4
U 1 1 612DBA2C
P 4950 4400
F 0 "J4" H 5007 4867 50  0000 C CNN
F 1 "4P4C" H 5007 4776 50  0000 C CNN
F 2 "Connector_RJ:RJ14_Connfly_DS1133-S4_Horizontal" V 4950 4450 50  0001 C CNN
F 3 "~" V 4950 4450 50  0001 C CNN
	1    4950 4400
	1    0    0    -1  
$EndComp
Connection ~ 5850 4300
Wire Wire Line
	5850 4300 5850 4600
Wire Wire Line
	5350 4200 6750 4200
Wire Wire Line
	5850 3550 5850 4300
Connection ~ 6400 3450
Wire Wire Line
	7300 3400 6100 3400
$Comp
L Connector:4P4C J3
U 1 1 612DB4DC
P 4950 3650
F 0 "J3" H 5007 4117 50  0000 C CNN
F 1 "4P4C" H 5007 4026 50  0000 C CNN
F 2 "Connector_RJ:RJ14_Connfly_DS1133-S4_Horizontal" V 4950 3700 50  0001 C CNN
F 3 "~" V 4950 3700 50  0001 C CNN
	1    4950 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 3450 6400 3450
$EndSCHEMATC
