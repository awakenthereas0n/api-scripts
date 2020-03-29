# API scripts

## Expensify scripts
- `expensify_downloader.py` - Report exporter to generate POST data for report download
- `expensify_report_export.py` - Report downloader to send POST request for downloading reports

### Still needed - Setup script
#### Contents needed:
Script to copy py script files to each directory, pass env variables with start/enddates/month_year iterating for each new month.

*Copy scripts from cloned git repo to working directory*
cp expensify_report_export.py expensify_downloader.py ~/<working-dir>/<year>/<month>

*Pass env variables, iterating by year-month-day*
export userid=$USERID
export secret=$SECRET
export startDate=%Y-%M-%d
export endDate=%Y-%M-%d
export month_year=%M_%Y

*Run each script*
python expensify_report_export.py && python expensify_downloader.py > output.log 2>&1 count &

