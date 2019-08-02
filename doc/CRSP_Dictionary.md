## CRSP Dictionary [Offical Guide](http://www.crsp.com/files/data_descriptions_guide_0.pdf)

**'PERMNO'** -- CRSP’s permanent issue identifier. One PERMNO belongs to only one PERMCO. One PERMCO can have one or more PERMNOs.

**'date',**

'NAMEENDT'-- Last Date of Name **(Company Survival)**

'SHRCD' -- Share Code

'EXCHCD' -- Exchange Code

**'SICCD'** -- Standard Industrial Classification (SIC) Code

'NCUSIP' -- CUSIP (Committee on Uniform Security Identification Procedures) identifier

'TICKER' -- Ticker Symbol

'COMNAM' -- Company Name

'SHRCLS' -- Share Class

'TSYMBOL' -- Trading Ticker Symbol

'NAICS' -- North American Industry Classification System (NAICS) Code

'PRIMEXCH' -- Primary Exchange

'TRDSTAT' -- Trading Status

'SECSTAT' -- Security Status

'PERMCO' -- Primary Permanent Identifiers

'ISSUNO' -- NASDAQ Issue Number

'HEXCD' -- Exchange Code - Header

**'HSICCD'** -- Standard Industrial Classification (SIC) Code - Header

'CUSIP' -- Committee on Uniform Security Identification Procedures and the nine-digit, alphanumeric CUSIP numbers that are used to identify securities, including municipal bonds.,

'DCLRDT' -- Distribution Declaration Date is the date (in
YYYYMMDD format) on which the board of directors
declared a distribution. If a declaration cannot be
found, then this date is set to zero.,

'DLAMT' -- Amount After Delisting is the value of a security
after it delists from an exchange. The amount can
be either an off-exchange price, an off-exchange
price quote, or the sum of a series of distribution
payments. The Amount After Delisting is used to
calculate the Delisting Return.,

'DLPDT' -- Delisting Date of Next Available Information is the integer date (in YYYYMMDD format) of a security’s
Delisting Price - the price or quote found after
delisting. This date is set to zero if the security is still
active. It is also set to zero if the final value of the
security is determined by one or more distributions or
if the value of the security is unknown after suspension
of trading or after delisting.,

'DLSTCD' -- Delisting Code Header is the issue’s delisting status at the end of the file. See Delisting Code for additional information. ,

'NEXTDT' -- Delisting Date of Next Available Information is the integer date (in YYYYMMDD format) of a security’s
Delisting Price - the price or quote found after
delisting. This date is set to zero if the security is still
active. It is also set to zero if the final value of the
security is determined by one or more distributions or
if the value of the security is unknown after suspension
of trading or after delistin,

'PAYDT' -- Payment Date is the integer date in YYYYMMDD
format upon which dividend checks are mailed
or other distributions are made. It is set to zero if
unavailable. For a merger, exchange or total liquidation
where the company disappeared Payment Date is, by
convention, set equal to the date of the last price or
Delisting Date,

'RCRDDT' -- Record Date is the record date on which the
stockholder must be registered as holder of record on
the stock transfer records of the company in order
to receive a particular distribution directly from the
company. This integer date is coded as YYYYMMDD,
and set to 0 if unavailable.,

'SHRFLG' -- Shares Outstanding Observation Flag is an integer value indicating the source of the shares outstanding
observation,

'HSICMG' -- SIC Code Header, Major Group, -- Header SIC Major Group.

'HSICIG' -- SIC Code Header, Industry Group -- Header SIC Industry Group

'DISTCD' -- CRSP describes company distributions and corporate actions in the distribution history with a 4-digit code. The first digit describes the type of distribution. The second digit describes the payment method. The third
digit augments the type denoted by the first digit. The
fourth digit provides information regarding the tax
status of the distribution for details,

**'DIVAMT'** - Dividend Cash Amount,

'FACPR' -- FACTOR TO ADJUST PRICE IN PERIOD, Is equal to: $(s(t) - s(t’))/s(t’) = (s(t)/s(t’)) - 1$

'FACSHR' -- Factor to Adjust Shares Outstanding is an adjustment to Shares Outstanding observations due to a distribution event.

'ACPERM' -- PERMNO of acquiring company,

'ACCOMP' -- PERMCO of acquiring company,

'NWPERM' -- New PERMNO after a delisting event,

'DLRETX' -- Delisting Return Without Dividends is the return
of a security after it has delisted from NYSE, NYSE
MKT, NASDAQ, or ARCA.

'DLPRC' -- Delisting Price,

'DLRET' -- Delisting Return

'TRTSCD'-- Daily ITEMID, One-digit integer describing the trading status of an issue listed on NASDAQ, at the end of each period reported

**'NMSIND'**-- Daily ITEMID, One-digit integer code indicating an issue's membership within the NASDAQ Market tier system (NASDAQ National Market Indicator)

'MMCNT' -- Daily ITEMID, Number of registered market makers for an issue trading on NASDAQ, at the end of the period reported.
 This contains a 0 if there are no active market makers at that time, or if the date falls in December of 1982 for a NASD Company Number less than 1025, or in February of 1986

'NSDINX' -- NASDAQ INDEX CODE, Integer code indicating the issue’s classification within NASD’s internal business description categories, at the end of each period reported.
 This field is not available between April, 1998 and February, 2000.

**'BIDLO'** --  Lowest trading price during the day, or the closing bid if trading price not available. Bid identified by a leading dash

**'ASKHI'** -- Ask or High Price is the highest trading price during the day, or the closing ask price on days when the closing price is not available.

**'PRC'** -- Price or Bid/Ask Average is the closing price or the bid/ask average for a trading day 'VOL', -- CRSP item functions use a standard notation for specifying a
set of data items. The notation allows selection by group or item. Examples are bal_ann or sale;at or prc;ret;vol or sale.*

**'RET'** -- Return?

**'BID'** -- BID price ?

**'ASK'** -- ASK price?

**'SHROUT'** -- Shares Outstanding

**'CFACPR'**-- cumulative factor to adjust price -- Factor Adjusted price

'CFACSHR' -- cumulative factor to adjusting shares in holdings data -- Factor to Adjust Shares Outstanding

**'OPENPRC'** -- Open price, Daily open prices are available for securities traded on NYSE, NYSE MKT, and NASDAQ exchanges beginning June 15, 1992.

**'NUMTRD'** -- NASDAQ Number of Trades (daily only)

'RETX'-- Day-to-day capital appreciation of a security, calculated as a change in price, or bid/ask average if prices not available -- Return Without Dividends

'vwretd'-- Total Return Value-Weighted Index

'vwretx'-- Return (Excluding Dividends) on Value-Weighted Index

'ewretd'-- Total Return Equal-Weighted Index

'ewretx'-- Return (Excluding Dividends) on Equal-Weighted Index

**'sprtrn'** -- S&P 500 Composite Index Return
