Las Parser
==========

Split .las file to sections with parsed data.

**Install:**
```bash
stepan@stepan-pc:~/Programms$ git clone https://github.com/stepan-perlov/las-parser
stepan@stepan-pc:~/Programms$ cd las-parser
stepan@stepan-pc:~/Programms/las-parser$ pip install .
```

**Usage:**
```bash
stepan@stepan-pc:~/Programms/las-parser$ python
```
```
Python 2.7.6 (default, Mar 22 2014, 22:59:56)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
```
```python
>>> from lasp import LasParser
>>> las = LasParser("example.las")
>>> print "\n".join(las.comments)
```
```
=========================================================================
Getting from http://www.minnelusa.com/sampledata.php
www.Minnelusa.com                   email: info@Minnelusa.com
Minnelusa Digital Well Log Data
=========================================================================
```

```python
>>> print las.version.title
```
```
Version Information
```

```python
>>> print las.version.data
```
```
{'WRAP': {'comment': 'One Line per Depth Step', 'value': 'NO'}, 'CREA': {'comment': 'LAS File Creation Date (MM-DD-YYYY)', 'value': '02-08-2006'}, 'VERS': {'comment': 'CWLS log ASCII Standard - Version 2.0', 'value': '2.0'}}
```

```python
>>> print las.version.data["VERS"]
```
```
{'comment': 'CWLS log ASCII Standard - Version 2.0', 'value': '2.0'}
```

```python
>>> print las.version.get("vErS")
```
```
{'comment': 'CWLS log ASCII Standard - Version 2.0', 'value': '2.0'}
```

```python
>>> print las.well.title
```
```
WELL Information Block
```

```python
>>> print las.well.data
```
```
{'LOC': {'Description_of': 'LOCATION', 'Data': 'SE SE 36-47N-71W', 'UNIT': None}, 'STAT': {'Description_of': 'STATE', 'Data': None, 'UNIT': 'Wyoming'}, 'COMP': {'Description_of': 'COMPANY', 'Data': 'Cramer Oil', 'UNIT': None}, 'WELL': {'Description_of': 'WELL', 'Data': '#36-16 State', 'UNIT': None}, 'STOP': {'Description_of': 'STOP DEPTH', 'Data': '10414.0000', 'UNIT': 'F'}, 'CTRY': {'Description_of': 'COUNTRY', 'Data': None, 'UNIT': 'U.S.A.'}, 'STRT': {'Description_of': 'START DEPTH', 'Data': '10180.0000', 'UNIT': 'F'}, 'STEP': {'Description_of': 'STEP', 'Data': '1.0000', 'UNIT': 'F'}, 'API': {'Description_of': 'API NUMBER', 'Data': '49-005-30258-0000', 'UNIT': None}, 'DATE': {'Description_of': 'COMPLETION DATE (MM/YY', 'Data': None, 'UNIT': '11/91'}, 'SRVC': {'Description_of': 'SERVICE COMPANY', 'Data': None, 'UNIT': None}, 'NULL': {'Description_of': 'NULL VALUE', 'Data': '-999.25', 'UNIT': None}, 'FLD': {'Description_of': 'FIELD', 'Data': None, 'UNIT': None}, 'CNTY': {'Description_of': 'COUNTY', 'Data': None, 'UNIT': 'Campbell'}}
```

```python
>>> print las.curve.title
```
```
Curve Information Block
```

```python
>>> print las.curve.data
```
```
{'DEPT': {'Curve_Description': '1 DEPTH', 'Data': None, 'UNIT': 'F'}, 'DT': {'Curve_Description': '2 SONIC DELTA-T', 'Data': None, 'UNIT': 'US/F'}, 'SP': {'Curve_Description': '4 SP CURVE', 'Data': None, 'UNIT': 'MV'}, 'GR': {'Curve_Description': '5 GAMMA RAY', 'Data': None, 'UNIT': 'GAPI'}, 'RESD': {'Curve_Description': '3 DEEP RESISTIVITY', 'Data': None, 'UNIT': 'OHMM'}}
```

```python
>>> print las.params.title
```
```
Parameter Information Block
```

```python
>>> print las.params.data
```
```
{'TOWN': {'Information': 'TOWNSHIP', 'UNIT': None, 'Value': '47N'}, 'RANG': {'Information': 'RANGE', 'UNIT': None, 'Value': '71W'}, 'EKB': {'Information': 'ELEVATION KELLY BUSHING', 'UNIT': 'F', 'Value': '4642.0000'}, 'RMF': {'Information': 'MUD FILTRATE RESISTIVITY', 'UNIT': 'OHMM', 'Value': '0.4410'}, 'SECT': {'Information': 'SECTION', 'UNIT': None, 'Value': '36'}, 'BHT': {'Information': 'BOTTOM HOLE TEMPERATURE', 'UNIT': 'DEGF', 'Value': '194.0000'}, 'RMFT': {'Information': 'MEASURE TEMPERATURE OF RMF', 'UNIT': 'DEGF', 'Value': '68.0000'}}
```

```python
>>> print las.data.title
```
```
None
```

```python
>>> print len(las.data.set)
```
```
235
```

**Analyze data with [pandas](http://pandas.pydata.org/):**
```python
>>> import pandas
>>> data = pandas.DataFrame(data=las.data.set, columns=las.data.header)
>>> print data
```
```
          Depth  Delta-T    Resist.        SP       GR+
0    10180.0000  59.9000    22.0000   45.6000  116.0000
1    10181.0000  59.9000    21.0000   49.0000  114.0000
2    10182.0000  60.5000    19.7000   53.0000  127.0000
3    10183.0000  63.5000    18.9000   55.6000  150.0000
4    10184.0000  64.5000    18.2000   58.4000  155.0000
5    10185.0000  64.6000    18.0000   62.5000  140.0000
6    10186.0000  61.5000    18.0000   64.7000  121.0000
7    10187.0000  59.2000    21.0000   66.9000  106.0000
8    10188.0000  55.9000    29.0000   69.3000   62.0000
9    10189.0000  52.1000    53.0000   71.3000   25.0000
10   10190.0000  49.1000   390.0000   73.7000    9.0000
11   10191.0000  47.8000  1501.0000   75.7000   11.0000
12   10192.0000  47.2000  2093.0000   76.7000   11.0000
13   10193.0000  47.2000  1677.0000   77.1000   10.0000
14   10194.0000  48.5000  1077.0000   77.5000    9.0000
15   10195.0000  49.6000   765.0000   77.5000    8.0000
16   10196.0000  48.3000   564.0000   77.5000    8.0000
17   10197.0000  46.9000   554.0000   77.5000    8.0000
18   10198.0000  46.6000   487.0000   77.1000   10.0000
19   10199.0000  46.8000   159.0000   76.5000   15.0000
20   10200.0000  46.7000    74.0000   75.9000   16.0000
21   10201.0000  47.8000    57.0000   74.7000   14.0000
22   10202.0000  51.2000    50.0000   73.7000   14.0000
23   10203.0000  51.6000    48.0000   71.1000   18.0000
24   10204.0000  51.1000    48.0000   67.3000   23.0000
25   10205.0000  51.4000    49.0000   63.7000   27.0000
26   10206.0000  52.3000    56.0000   60.6000   28.0000
27   10207.0000  52.3000    59.0000   57.8000   20.0000
28   10208.0000  51.5000    61.0000   53.2000   17.0000
29   10209.0000  51.2000    52.0000   48.2000   72.0000
..          ...      ...        ...       ...       ...
205  10385.0000  62.3000     9.2000  102.7000   38.0000
206  10386.0000  63.2000     8.6000   87.6000   38.0000
207  10387.0000  63.5000     8.5000   78.8000   40.0000
208  10388.0000  63.5000     9.4000   76.5000   38.0000
209  10389.0000  62.7000    11.4000   76.5000   33.0000
210  10390.0000  60.0000    14.8000   76.5000   27.0000
211  10391.0000  57.0000    19.0000   76.5000   27.0000
212  10392.0000  54.0000    40.0000   76.5000   27.0000
213  10393.0000  49.1000    89.0000   76.5000   23.0000
214  10394.0000  47.2000   134.0000   75.5000   22.0000
215  10395.0000  46.7000   220.0000   74.1000   25.0000
216  10396.0000  47.1000   193.0000   72.1000   31.0000
217  10397.0000  47.6000   122.0000   70.5000   33.0000
218  10398.0000  48.8000    96.0000   68.9000   35.0000
219  10399.0000  49.8000    81.0000   67.5000    5.0000
220  10400.0000  50.8000    75.0000   66.7000    0.0000
221  10401.0000  51.1000    75.0000   65.7000    0.0000
222  10402.0000  50.2000    97.0000   65.1000    0.0000
223  10403.0000  49.0000   167.0000   64.1000    0.0000
224  10404.0000  48.4000   315.0000   63.3000    0.0000
225  10405.0000  50.6000  1693.0000   63.1000    0.0000
226  10406.0000  50.7000  1874.0000   62.7000    0.0000
227  10407.0000  50.4000  1874.0000   62.5000    0.0000
228  10408.0000  49.9000  1874.0000   62.5000    0.0000
229  10409.0000  49.7000   591.0000   62.5000    0.0000
230  10410.0000  49.6000   208.0000   62.5000    0.0000
231  10411.0000  51.5000   134.0000   62.5000    0.0000
232  10412.0000  52.5000   116.0000   62.9000    0.0000
233  10413.0000  53.2000   113.0000   64.3000    0.0000
234  10414.0000  54.1000   156.0000   65.9000    0.0000

[235 rows x 5 columns]
```