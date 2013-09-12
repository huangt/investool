import ystockquote
import csv

#print ystockquote.get_price('GOOG')
#print ystockquote.get_all('MSFT')
#print ystockquote.get_book_value('GOOG')

csvfile = open('nasdaqlist.csv', 'rb')
reader = csv.reader(csvfile)

rownum = 0
stocksymbols = []
stockDetails =[]
for row in reader:
    # Save header row.
    if rownum == 0:
        header = row
    else:
        #print row
        stocksymbols.append(row[0])
        stockDetails.append(row)
             
    rownum += 1
 
csvfile.close()

results = []
for stockDetail in stockDetails:
    symbol = stockDetail[0]
    price = float(ystockquote.get_price(symbol))
    bookvalue = float(ystockquote.get_book_value(symbol))
    halfBook = bookvalue * 0.5
    if (price <= halfBook):
        print ', '.join(stockDetail)
        results.append(symbol)

print len(results)
