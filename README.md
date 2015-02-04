ST interactive monitor
-------------------

Runing interactive monitor:
- Install flask
- Put .root file with histograms for each sector to the data/ folder. Pay attention, that histograms in your tuple should be named using schema <Something>_<SectorName>, i.e. VeryInterestingHist_TTaURegionA22
- run runInteractiveMap.py:
"""
python runInteractiveMap.py
"""
- open http://127.0.0.1:5000/index in your browser.
- PROFIT!
