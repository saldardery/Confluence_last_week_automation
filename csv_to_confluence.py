from atlassian import Confluence
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
from jira import JIRA

## GET VALUES FROM JIRA
jira = JIRA('https://jira.pscoe.vmware.com/', auth=('saldardery', 'Ahly_12345'))
in_progress = jira.search_issues('((project = MCOEA AND issuetype = Project AND status in (Backlog, Execution)) OR (project = "Project Atlantic - Modernization COE " AND "Migration Process" = Accelerated AND "Assessment Status" = In-progress AND status in (BACKLOG, EXECUTION)) )AND (product != "NSX - Standalone Migration") ',maxResults=1000)
pipeline=issues = jira.search_issues ('((project = MCOEA AND issuetype = Project AND status in (Approved, "SOW Prep", "SOW Approval & Signature")) OR (project = "Project Atlantic - Modernization COE " AND "Migration Process" = Accelerated AND ("Assessment Status" != In-progress OR "Assessment Status" != Completed))) AND created >= startOfWeek()',maxResults=1000)
pipeline_count=len(pipeline)
in_progress_count = len(in_progress)




# Create a Confluence object with your credentials and URL
confluence = Confluence(url="https://confluence.pscoe.vmware.com", username="saldardery", password='@hly_91!Ahly_91!')
page_id = "126594086"

# Define the ID of the existing confluence page
# Define the content of the table excerpt
table_content = f"""
<ac:structured-macro ac:name="table-excerpt" ac:schema-version="1">
  <ac:parameter ac:name="atlassian-macro-output-type">INLINE</ac:parameter>
  <ac:parameter ac:name="name">last_week_result</ac:parameter>
  <ac:rich-text-body>
    <table>
      <tbody>
        <tr>
          <th>Pipeline</th>
          <th>In progress</th>
        </tr>
        <tr>
          <td>{pipeline_count}</td>
          <td>{in_progress_count}</td>
        </tr>
      </tbody>
    </table>
  </ac:rich-text-body>
</ac:structured-macro>
"""

# Get the current version of the page
response = confluence.get_page_by_id(page_id,"body.storage")
#print(response)
#page_version = response["version"]["number"]

# Update the page with the table excerpt appended at the end of the body
response = confluence.update_page(
    page_id=page_id,
    title=response["title"],
    body=table_content,
    #version=page_version + 1,
)
