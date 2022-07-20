import scraper
import xlsxwriter
 
workbook = xlsxwriter.Workbook('data.xlsx')
main = workbook.add_worksheet()
schedule = workbook.add_worksheet()
 
data = scraper.data
headers1 = scraper.headers1
headers2 = ["Class (CRN)"] + scraper.headers2

r, c = 0,0
for header in headers1:
    main.write(r, c, header)
    c += 1
c = 0
for header in headers2:
    schedule.write(r, c, header)
    c+=1
r, rs = 1, 1
for row in data:
    main.write(r, 0, row["CRN"])
    main.write(r, 1, row["Subj"])
    main.write(r, 2, row["Crse"])
    main.write(r, 3, row["Sec"])
    main.write(r, 4, row["Units"])
    main.write(r, 5, row["Title"])
    main.write(r, 6, row["Campus"])
    r += 1
    for day in row["Schedule"]:
        schedule.write(rs, 0, row["CRN"])
        schedule.write(rs, 1, day["StartDate"])
        schedule.write(rs, 2, day["EndDate"])
        schedule.write(rs, 3, day["Days"])
        schedule.write(rs, 4, day["Times"])
        schedule.write(rs, 5, day["Bldg"])
        schedule.write(rs, 6, day["Room"])
        rs += 1
    schedule.write(rs, 0, "")
    rs += 1

workbook.close()
print("xls file created")