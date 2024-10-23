// GMSH geometry file for substrate and resistors
// Variables: 
lcs = 200.0;
// SUBSTRATE POINTS:
Point(1) = {-2750.0, -2750.0, 0, lcs};
Point(2) = {2750.0, -2750.0, 0, lcs};
Point(3) = {2750.0, 2750.0, 0, lcs};
Point(4) = {-2750.0, 2750.0, 0, lcs};
// SUBSTRATE LINES:
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Physical Line("Boundary_1") = {1};
Physical Line("Boundary_2") = {2};
Physical Line("Boundary_3") = {3};
Physical Line("Boundary_4") = {4};
// SUBSTRATE SURFACE
Curve Loop(1) = {1, 2, 3, 4};
Physical Surface("Substrate", 1) = {1};  // Substrate

// RESISTOR POINTS:
lcr = 22.0;
Point(5) = {-2401.0, 2379.0, 0, lcr};
Point(6) = {-2379.0, 2379.0, 0, lcr};
Point(7) = {-2379.0, 2460.0, 0, lcr};
Point(8) = {-2401.0, 2460.0, 0, lcr};
// RESISTOR LINES:
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 5};
// RESISTOR CURVE
Curve Loop(2) = {5, 6, 7, 8};
// RESISTOR PLANE SURFACE:
Plane Surface(2) = {2};
Physical Surface("Resistor_1", 2) = {2};  // Resistor 1

// RESISTOR POINTS:
lcr = 57.0;
Point(9) = {-2406.0, 1703.0, 0, lcr};
Point(10) = {-2349.0, 1703.0, 0, lcr};
Point(11) = {-2349.0, 1998.0, 0, lcr};
Point(12) = {-2406.0, 1998.0, 0, lcr};
// RESISTOR LINES:
Line(9) = {9, 10};
Line(10) = {10, 11};
Line(11) = {11, 12};
Line(12) = {12, 9};
// RESISTOR CURVE
Curve Loop(3) = {9, 10, 11, 12};
// RESISTOR PLANE SURFACE:
Plane Surface(3) = {3};
Physical Surface("Resistor_2", 3) = {3};  // Resistor 2

// RESISTOR POINTS:
lcr = 77.0;
Point(13) = {-1700.0, 2064.0, 0, lcr};
Point(14) = {-1623.0, 2064.0, 0, lcr};
Point(15) = {-1623.0, 2298.0, 0, lcr};
Point(16) = {-1700.0, 2298.0, 0, lcr};
// RESISTOR LINES:
Line(13) = {13, 14};
Line(14) = {14, 15};
Line(15) = {15, 16};
Line(16) = {16, 13};
// RESISTOR CURVE
Curve Loop(4) = {13, 14, 15, 16};
// RESISTOR PLANE SURFACE:
Plane Surface(4) = {4};
Physical Surface("Resistor_3", 4) = {4};  // Resistor 3

// RESISTOR POINTS:
lcr = 42.0;
Point(17) = {-1039.0, 2251.0, 0, lcr};
Point(18) = {-997.0, 2251.0, 0, lcr};
Point(19) = {-997.0, 2465.0, 0, lcr};
Point(20) = {-1039.0, 2465.0, 0, lcr};
// RESISTOR LINES:
Line(17) = {17, 18};
Line(18) = {18, 19};
Line(19) = {19, 20};
Line(20) = {20, 17};
// RESISTOR CURVE
Curve Loop(5) = {17, 18, 19, 20};
// RESISTOR PLANE SURFACE:
Plane Surface(5) = {5};
Physical Surface("Resistor_4", 5) = {5};  // Resistor 4

// RESISTOR POINTS:
lcr = 27.0;
Point(21) = {-1494.0, 903.0, 0, lcr};
Point(22) = {-1467.0, 903.0, 0, lcr};
Point(23) = {-1467.0, 1072.0, 0, lcr};
Point(24) = {-1494.0, 1072.0, 0, lcr};
// RESISTOR LINES:
Line(21) = {21, 22};
Line(22) = {22, 23};
Line(23) = {23, 24};
Line(24) = {24, 21};
// RESISTOR CURVE
Curve Loop(6) = {21, 22, 23, 24};
// RESISTOR PLANE SURFACE:
Plane Surface(6) = {6};
Physical Surface("Resistor_5", 6) = {6};  // Resistor 5

// RESISTOR POINTS:
lcr = 126.0;
Point(25) = {-1093.0, 1114.0, 0, lcr};
Point(26) = {-967.0, 1114.0, 0, lcr};
Point(27) = {-967.0, 1379.0, 0, lcr};
Point(28) = {-1093.0, 1379.0, 0, lcr};
// RESISTOR LINES:
Line(25) = {25, 26};
Line(26) = {26, 27};
Line(27) = {27, 28};
Line(28) = {28, 25};
// RESISTOR CURVE
Curve Loop(7) = {25, 26, 27, 28};
// RESISTOR PLANE SURFACE:
Plane Surface(7) = {7};
Physical Surface("Resistor_6", 7) = {7};  // Resistor 6

// RESISTOR POINTS:
lcr = 20.0;
Point(29) = {661.0, 1808.0, 0, lcr};
Point(30) = {681.0, 1808.0, 0, lcr};
Point(31) = {681.0, 1994.0, 0, lcr};
Point(32) = {661.0, 1994.0, 0, lcr};
// RESISTOR LINES:
Line(29) = {29, 30};
Line(30) = {30, 31};
Line(31) = {31, 32};
Line(32) = {32, 29};
// RESISTOR CURVE
Curve Loop(8) = {29, 30, 31, 32};
// RESISTOR PLANE SURFACE:
Plane Surface(8) = {8};
Physical Surface("Resistor_7", 8) = {8};  // Resistor 7

// RESISTOR POINTS:
lcr = 237.0;
Point(33) = {530.0, 727.0, 0, lcr};
Point(34) = {767.0, 727.0, 0, lcr};
Point(35) = {767.0, 1170.0, 0, lcr};
Point(36) = {530.0, 1170.0, 0, lcr};
// RESISTOR LINES:
Line(33) = {33, 34};
Line(34) = {34, 35};
Line(35) = {35, 36};
Line(36) = {36, 33};
// RESISTOR CURVE
Curve Loop(9) = {33, 34, 35, 36};
// RESISTOR PLANE SURFACE:
Plane Surface(9) = {9};
Physical Surface("Resistor_8", 9) = {9};  // Resistor 8

// RESISTOR POINTS:
lcr = 203.0;
Point(37) = {-93.0, -354.0, 0, lcr};
Point(38) = {110.0, -354.0, 0, lcr};
Point(39) = {110.0, 354.0, 0, lcr};
Point(40) = {-93.0, 354.0, 0, lcr};
// RESISTOR LINES:
Line(37) = {37, 38};
Line(38) = {38, 39};
Line(39) = {39, 40};
Line(40) = {40, 37};
// RESISTOR CURVE
Curve Loop(10) = {37, 38, 39, 40};
// RESISTOR PLANE SURFACE:
Plane Surface(10) = {10};
Physical Surface("Resistor_9", 10) = {10};  // Resistor 9

// RESISTOR POINTS:
lcr = 94.0;
Point(41) = {-2216.0, -569.0, 0, lcr};
Point(42) = {-2122.0, -569.0, 0, lcr};
Point(43) = {-2122.0, -113.0, 0, lcr};
Point(44) = {-2216.0, -113.0, 0, lcr};
// RESISTOR LINES:
Line(41) = {41, 42};
Line(42) = {42, 43};
Line(43) = {43, 44};
Line(44) = {44, 41};
// RESISTOR CURVE
Curve Loop(11) = {41, 42, 43, 44};
// RESISTOR PLANE SURFACE:
Plane Surface(11) = {11};
Physical Surface("Resistor_10", 11) = {11};  // Resistor 10

// RESISTOR POINTS:
lcr = 59.0;
Point(45) = {-733.0, -505.0, 0, lcr};
Point(46) = {-674.0, -505.0, 0, lcr};
Point(47) = {-674.0, -363.0, 0, lcr};
Point(48) = {-733.0, -363.0, 0, lcr};
// RESISTOR LINES:
Line(45) = {45, 46};
Line(46) = {46, 47};
Line(47) = {47, 48};
Line(48) = {48, 45};
// RESISTOR CURVE
Curve Loop(12) = {45, 46, 47, 48};
// RESISTOR PLANE SURFACE:
Plane Surface(12) = {12};
Physical Surface("Resistor_11", 12) = {12};  // Resistor 11

// RESISTOR POINTS:
lcr = 169.0;
Point(49) = {951.0, -1114.0, 0, lcr};
Point(50) = {1120.0, -1114.0, 0, lcr};
Point(51) = {1120.0, -429.0, 0, lcr};
Point(52) = {951.0, -429.0, 0, lcr};
// RESISTOR LINES:
Line(49) = {49, 50};
Line(50) = {50, 51};
Line(51) = {51, 52};
Line(52) = {52, 49};
// RESISTOR CURVE
Curve Loop(13) = {49, 50, 51, 52};
// RESISTOR PLANE SURFACE:
Plane Surface(13) = {13};
Physical Surface("Resistor_12", 13) = {13};  // Resistor 12

// RESISTOR POINTS:
lcr = 31.0;
Point(53) = {-1472.0, -1114.0, 0, lcr};
Point(54) = {-1441.0, -1114.0, 0, lcr};
Point(55) = {-1441.0, -1048.0, 0, lcr};
Point(56) = {-1472.0, -1048.0, 0, lcr};
// RESISTOR LINES:
Line(53) = {53, 54};
Line(54) = {54, 55};
Line(55) = {55, 56};
Line(56) = {56, 53};
// RESISTOR CURVE
Curve Loop(14) = {53, 54, 55, 56};
// RESISTOR PLANE SURFACE:
Plane Surface(14) = {14};
Physical Surface("Resistor_13", 14) = {14};  // Resistor 13

// RESISTOR POINTS:
lcr = 30.0;
Point(57) = {-1470.0, -1203.0, 0, lcr};
Point(58) = {-1440.0, -1203.0, 0, lcr};
Point(59) = {-1440.0, -1139.0, 0, lcr};
Point(60) = {-1470.0, -1139.0, 0, lcr};
// RESISTOR LINES:
Line(57) = {57, 58};
Line(58) = {58, 59};
Line(59) = {59, 60};
Line(60) = {60, 57};
// RESISTOR CURVE
Curve Loop(15) = {57, 58, 59, 60};
// RESISTOR PLANE SURFACE:
Plane Surface(15) = {15};
Physical Surface("Resistor_14", 15) = {15};  // Resistor 14

// RESISTOR POINTS:
lcr = 32.0;
Point(61) = {-1463.0, -1318.0, 0, lcr};
Point(62) = {-1431.0, -1318.0, 0, lcr};
Point(63) = {-1431.0, -1241.0, 0, lcr};
Point(64) = {-1463.0, -1241.0, 0, lcr};
// RESISTOR LINES:
Line(61) = {61, 62};
Line(62) = {62, 63};
Line(63) = {63, 64};
Line(64) = {64, 61};
// RESISTOR CURVE
Curve Loop(16) = {61, 62, 63, 64};
// RESISTOR PLANE SURFACE:
Plane Surface(16) = {16};
Physical Surface("Resistor_15", 16) = {16};  // Resistor 15

// RESISTOR POINTS:
lcr = 243.0;
Point(65) = {-336.0, -2262.0, 0, lcr};
Point(66) = {-93.0, -2262.0, 0, lcr};
Point(67) = {-93.0, -1537.0, 0, lcr};
Point(68) = {-336.0, -1537.0, 0, lcr};
// RESISTOR LINES:
Line(65) = {65, 66};
Line(66) = {66, 67};
Line(67) = {67, 68};
Line(68) = {68, 65};
// RESISTOR CURVE
Curve Loop(17) = {65, 66, 67, 68};
// RESISTOR PLANE SURFACE:
Plane Surface(17) = {17};
Physical Surface("Resistor_16", 17) = {17};  // Resistor 16

// RESISTOR POINTS:
lcr = 21.0;
Point(69) = {1714.0, -1818.0, 0, lcr};
Point(70) = {1735.0, -1818.0, 0, lcr};
Point(71) = {1735.0, -1757.0, 0, lcr};
Point(72) = {1714.0, -1757.0, 0, lcr};
// RESISTOR LINES:
Line(69) = {69, 70};
Line(70) = {70, 71};
Line(71) = {71, 72};
Line(72) = {72, 69};
// RESISTOR CURVE
Curve Loop(18) = {69, 70, 71, 72};
// RESISTOR PLANE SURFACE:
Plane Surface(18) = {18};
Physical Surface("Resistor_17", 18) = {18};  // Resistor 17

// RESISTOR POINTS:
lcr = 14.0;
Point(73) = {1961.0, -1900.0, 0, lcr};
Point(74) = {1975.0, -1900.0, 0, lcr};
Point(75) = {1975.0, -1842.0, 0, lcr};
Point(76) = {1961.0, -1842.0, 0, lcr};
// RESISTOR LINES:
Line(73) = {73, 74};
Line(74) = {74, 75};
Line(75) = {75, 76};
Line(76) = {76, 73};
// RESISTOR CURVE
Curve Loop(19) = {73, 74, 75, 76};
// RESISTOR PLANE SURFACE:
Plane Surface(19) = {19};
Physical Surface("Resistor_18", 19) = {19};  // Resistor 18

// RESISTOR POINTS:
lcr = 29.0;
Point(77) = {1653.0, -2169.0, 0, lcr};
Point(78) = {1682.0, -2169.0, 0, lcr};
Point(79) = {1682.0, -2036.0, 0, lcr};
Point(80) = {1653.0, -2036.0, 0, lcr};
// RESISTOR LINES:
Line(77) = {77, 78};
Line(78) = {78, 79};
Line(79) = {79, 80};
Line(80) = {80, 77};
// RESISTOR CURVE
Curve Loop(20) = {77, 78, 79, 80};
// RESISTOR PLANE SURFACE:
Plane Surface(20) = {20};
Physical Surface("Resistor_19", 20) = {20};  // Resistor 19

// RESISTOR POINTS:
lcr = 35.0;
Point(81) = {1762.0, -2166.0, 0, lcr};
Point(82) = {1797.0, -2166.0, 0, lcr};
Point(83) = {1797.0, -2046.0, 0, lcr};
Point(84) = {1762.0, -2046.0, 0, lcr};
// RESISTOR LINES:
Line(81) = {81, 82};
Line(82) = {82, 83};
Line(83) = {83, 84};
Line(84) = {84, 81};
// RESISTOR CURVE
Curve Loop(21) = {81, 82, 83, 84};
// RESISTOR PLANE SURFACE:
Plane Surface(21) = {21};
Physical Surface("Resistor_20", 21) = {21};  // Resistor 20

// RESISTOR POINTS:
lcr = 31.0;
Point(85) = {1889.0, -2117.0, 0, lcr};
Point(86) = {1920.0, -2117.0, 0, lcr};
Point(87) = {1920.0, -2039.0, 0, lcr};
Point(88) = {1889.0, -2039.0, 0, lcr};
// RESISTOR LINES:
Line(85) = {85, 86};
Line(86) = {86, 87};
Line(87) = {87, 88};
Line(88) = {88, 85};
// RESISTOR CURVE
Curve Loop(22) = {85, 86, 87, 88};
// RESISTOR PLANE SURFACE:
Plane Surface(22) = {22};
Physical Surface("Resistor_21", 22) = {22};  // Resistor 21

// SUBSTRATE SURFACE WITH HOLES:
Plane Surface(1) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22};
Field[1] = Distance;
Field[1].CurvesList = {9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88};
Field[1].NumPointsPerCurve = 100;
Field[2] = Threshold;
Field[2].InField = 1;
Field[2].LcMin = 31.0;
Field[2].LcMax = 200.0;
Field[2].DistMin = 0.1;
Field[2].DistMax = 1.0;
Background Field = 2;

Mesh 2;
Save "layoutMesh.msh";
