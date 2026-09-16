# Verified live against https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>
# higher_is_worse: True means rising values = more stress (for coloring/threshold logic)
# threshold: (value, label) for an OFFICIALLY documented trigger line, where one exists. None = use percentile bands instead.

SERIES = [
    # --- Housing / Mortgage ---
    {"id": "DRSFRMACBS", "label": "Mortgage Delinquency Rate", "category": "Housing & Mortgage", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "RCMFLBBALDPDPCT90P", "label": "Mortgage 90+ Days Past Due (incl. Foreclosure)", "category": "Housing & Mortgage", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "RCMFLBBALDPDPCT60P", "label": "Mortgage 60+ Days Past Due (incl. Foreclosure)", "category": "Housing & Mortgage", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "MORTGAGE30US", "label": "30-Year Fixed Mortgage Rate", "category": "Housing & Mortgage", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "CSUSHPISA", "label": "Case-Shiller Home Price Index", "category": "Housing & Mortgage", "unit": "index", "higher_is_worse": False, "threshold": None},
    {"id": "HOUST", "label": "Housing Starts", "category": "Housing & Mortgage", "unit": "thousands, SAAR", "higher_is_worse": False, "threshold": None},
    {"id": "PERMIT", "label": "Building Permits", "category": "Housing & Mortgage", "unit": "thousands, SAAR", "higher_is_worse": False, "threshold": None},
    {"id": "EXHOSLUSM495S", "label": "Existing Home Sales", "category": "Housing & Mortgage", "unit": "units, SAAR", "higher_is_worse": False, "threshold": None},

    # --- Consumer Credit ---
    {"id": "DRCCLACBS", "label": "Credit Card Delinquency Rate", "category": "Consumer Credit", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "CORCCACBS", "label": "Credit Card Charge-Off Rate", "category": "Consumer Credit", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "DRCLACBS", "label": "Consumer (Personal) Loan Delinquency Rate", "category": "Consumer Credit", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "DRALACBS", "label": "Delinquency Rate on All Bank Loans", "category": "Consumer Credit", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "TDSP", "label": "Household Debt Service Ratio", "category": "Consumer Credit", "unit": "% of disposable income", "higher_is_worse": True, "threshold": None},
    {"id": "MDSP", "label": "Mortgage Debt Service Ratio", "category": "Consumer Credit", "unit": "% of disposable income", "higher_is_worse": True, "threshold": None},

    # --- Labor Market ---
    {"id": "ICSA", "label": "Initial Jobless Claims", "category": "Labor Market", "unit": "claims/week", "higher_is_worse": True, "threshold": None},
    {"id": "IC4WSA", "label": "Initial Claims (4-Week Avg)", "category": "Labor Market", "unit": "claims/week", "higher_is_worse": True, "threshold": None},
    {"id": "CCSA", "label": "Continuing Jobless Claims", "category": "Labor Market", "unit": "claims", "higher_is_worse": True, "threshold": None},
    {"id": "UNRATE", "label": "Unemployment Rate", "category": "Labor Market", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "CIVPART", "label": "Labor Force Participation Rate", "category": "Labor Market", "unit": "%", "higher_is_worse": False, "threshold": None},
    {"id": "JTSJOL", "label": "Job Openings (JOLTS)", "category": "Labor Market", "unit": "thousands", "higher_is_worse": False, "threshold": None},
    {"id": "JTSQUR", "label": "Quits Rate", "category": "Labor Market", "unit": "%", "higher_is_worse": False, "threshold": None},
    {"id": "TEMPHELPS", "label": "Temporary Help Employment", "category": "Labor Market", "unit": "thousands", "higher_is_worse": False, "threshold": None},
    {"id": "AWHAEMAN", "label": "Avg Weekly Manufacturing Hours", "category": "Labor Market", "unit": "hours", "higher_is_worse": False, "threshold": None},
    {"id": "AHETPI", "label": "Average Hourly Earnings", "category": "Labor Market", "unit": "$/hr", "higher_is_worse": False, "threshold": None, "deflate": True},

    # --- Composite / Recession Models ---
    {"id": "SAHMREALTIME", "label": "Sahm Rule Recession Indicator", "category": "Composite Recession Models", "unit": "pp", "higher_is_worse": True, "threshold": (0.50, "Official Sahm Rule trigger (0.50)")},
    {"id": "NFCI", "label": "Chicago Fed Financial Conditions Index", "category": "Composite Recession Models", "unit": "index", "higher_is_worse": True, "threshold": (0, "Neutral line (0) — above = tighter than average")},
    {"id": "STLFSI4", "label": "St. Louis Fed Financial Stress Index", "category": "Composite Recession Models", "unit": "index", "higher_is_worse": True, "threshold": (0, "Neutral line (0) — above = above-average stress")},
    {"id": "CFNAIMA3", "label": "Chicago Fed National Activity Index (3mo avg)", "category": "Composite Recession Models", "unit": "index", "higher_is_worse": False, "threshold": (-0.70, "Historical recession-association line (-0.70)")},
    {"id": "WEI", "label": "Dallas Fed Weekly Economic Index", "category": "Composite Recession Models", "unit": "index", "higher_is_worse": False, "threshold": None},
    {"id": "USREC", "label": "NBER Recession Indicator", "category": "Composite Recession Models", "unit": "0/1", "higher_is_worse": True, "threshold": None},

    # --- Credit Markets ---
    {"id": "T10Y3M", "label": "Yield Curve (10Y - 3M)", "category": "Credit Markets", "unit": "pp", "higher_is_worse": False, "threshold": (0, "Inversion line (0) — below = inverted")},
    {"id": "BAMLH0A0HYM2", "label": "High-Yield Bond Spread", "category": "Credit Markets", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "BAA10Y", "label": "Baa Corporate Bond Spread", "category": "Credit Markets", "unit": "pp", "higher_is_worse": True, "threshold": None},
    {"id": "DRTSCILM", "label": "Bank Tightening Standards (C&I Loans)", "category": "Credit Markets", "unit": "net % tightening", "higher_is_worse": True, "threshold": (0, "Net tightening line (0) — above = net tightening")},
    {"id": "DGS10", "label": "10-Year Treasury Yield", "category": "Credit Markets", "unit": "%", "higher_is_worse": None, "threshold": None},

    # --- Business & Commercial Real Estate ---
    {"id": "DRBLACBS", "label": "Business Loan Delinquency Rate", "category": "Business & CRE", "unit": "%", "higher_is_worse": True, "threshold": None},
    {"id": "DRCRELEXFACBS", "label": "Commercial Real Estate Loan Delinquency Rate", "category": "Business & CRE", "unit": "%", "higher_is_worse": True, "threshold": None},

    # --- Production & Spending ---
    {"id": "INDPRO", "label": "Industrial Production Index", "category": "Production & Spending", "unit": "index", "higher_is_worse": False, "threshold": None},
    {"id": "NEWORDER", "label": "Core Capital Goods Orders", "category": "Production & Spending", "unit": "$M", "higher_is_worse": False, "threshold": None, "deflate": True},
    {"id": "HTRUCKSSAAR", "label": "Heavy Truck Sales", "category": "Production & Spending", "unit": "millions, SAAR", "higher_is_worse": False, "threshold": None},
    {"id": "ALTSALES", "label": "Light Vehicle Sales", "category": "Production & Spending", "unit": "millions, SAAR", "higher_is_worse": False, "threshold": None},
    {"id": "RRSFS", "label": "Real Retail & Food Services Sales", "category": "Production & Spending", "unit": "$M", "higher_is_worse": False, "threshold": None},
    {"id": "RETAILIRSA", "label": "Retail Inventory/Sales Ratio", "category": "Production & Spending", "unit": "ratio", "higher_is_worse": True, "threshold": None},
    {"id": "TSIFRGHT", "label": "Freight Transportation Services Index", "category": "Production & Spending", "unit": "index", "higher_is_worse": False, "threshold": None},
    {"id": "PCOPPUSDM", "label": "Global Copper Price", "category": "Production & Spending", "unit": "$/mt", "higher_is_worse": False, "threshold": None, "deflate": True},

    # --- Money & Macro ---
    {"id": "M2SL", "label": "M2 Money Supply", "category": "Money & Macro", "unit": "$B", "higher_is_worse": None, "threshold": None, "deflate": True},
    {"id": "GDPC1", "label": "Real GDP", "category": "Money & Macro", "unit": "$B", "higher_is_worse": False, "threshold": None},
    {"id": "PSAVERT", "label": "Personal Savings Rate", "category": "Money & Macro", "unit": "%", "higher_is_worse": False, "threshold": None},
    {"id": "UMCSENT", "label": "Consumer Sentiment (U. Michigan)", "category": "Money & Macro", "unit": "index", "higher_is_worse": False, "threshold": None},

    # --- Income & Cost of Living ---
    {"id": "PI", "label": "Personal Income", "category": "Income & Cost of Living", "unit": "$B", "higher_is_worse": False, "threshold": None, "deflate": True},
    {"id": "A229RC0", "label": "Disposable Income Per Capita", "category": "Income & Cost of Living", "unit": "$", "higher_is_worse": False, "threshold": None, "deflate": True},
    {"id": "W875RX1", "label": "Real Personal Income (ex. Transfers)", "category": "Income & Cost of Living", "unit": "$B", "higher_is_worse": False, "threshold": None},
    {"id": "MEHOINUSA672N", "label": "Real Median Household Income", "category": "Income & Cost of Living", "unit": "$", "higher_is_worse": False, "threshold": None},
    {"id": "GASREGW", "label": "Weekly Gas Price (Regular)", "category": "Income & Cost of Living", "unit": "$/gal", "higher_is_worse": True, "threshold": None, "deflate": True},
    {"id": "APU0000709112", "label": "Avg Price: Milk", "category": "Income & Cost of Living", "unit": "$/gal", "higher_is_worse": True, "threshold": None, "deflate": True},
    {"id": "APU0000702111", "label": "Avg Price: White Bread", "category": "Income & Cost of Living", "unit": "$/lb", "higher_is_worse": True, "threshold": None, "deflate": True},
    {"id": "APU0000FD3101", "label": "Avg Price: Pork Chops", "category": "Income & Cost of Living", "unit": "$/lb", "higher_is_worse": True, "threshold": None, "deflate": True},
    {"id": "APU0000710212", "label": "Avg Price: Cheddar Cheese", "category": "Income & Cost of Living", "unit": "$/lb", "higher_is_worse": True, "threshold": None, "deflate": True},
    {"id": "CUSR0000SAF11", "label": "CPI: Food at Home", "category": "Income & Cost of Living", "unit": "index", "higher_is_worse": True, "threshold": None},
    {"id": "CPIAUCNS", "label": "CPI: All Items (deflator)", "category": "Income & Cost of Living", "unit": "index", "higher_is_worse": None, "threshold": None},
]
