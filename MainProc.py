import crawlingPackage

# init the variable and type
group = [1,2,3]

for x in group:
    group = str(x)
    output_filename = "output" + group + ".csv"

    # scraping data from website
    data = crawlingPackage.scrape(group)
    # export result to csv
    crawlingPackage.writecsv(output_filename, data)

    # get list from csv file
    # rows = crawlingPackage.getcsv(output_filename)
    # import into database
    # crawlingPackage.importdb(rows, group)