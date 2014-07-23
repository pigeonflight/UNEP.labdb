import json
import urllib
from bs4 import BeautifulSoup
from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest

 
#############################
### supporting functions
#############################
class LabImporter:
    """ An Importer that imports Labs into the UNEP website 
       You should be able to do the following:
       li = LabImporter(context,request)
       li.create_lab_folder()
       lab = li.create_lab(u"My Lab")
 """
    def __init__(self,portal):
        self.query_url = "http://carrcu.org/components/com_uneplabsdatabase/labinfo.php?labid=%(page)s" 
        #portal_url = getToolByName(context, "portal_url")
        self.portal = portal #portal_url.getPortalObject()

    def create_lab_folder(self):
        try:
            lab_folder = self.portal.invokeFactory('Folder', 'labs')
            self.lab_folder = lab_folder
            print("lab folder created")
        except BadRequest:
            self.lab_folder = self.portal['labs']
            print("lab folder already existed")

    def create_lab(self,lab_name):
        lab = createContentInContainer(
              self.lab_folder, u"UNEP.labdb.lab", title=lab_name
              )
        return lab

class LabScraper:
    """ A Scraper that queries the CARRCU website """

    def __init__(self):
        self.query_url = "http://carrcu.org/components/com_uneplabsdatabase/labinfo.php?labid=%(page)s" 

    def query_companies(self,string,searchtype="company"):
        self.prepare_query(string,searchtype)
        self.run_query()

    def prepare_query(self):
        _query = self._query = {
                  "page":1
                  }
        query = self.build_query(_query)
        page = self.make_page(query)
        

    def run_query(self):
        labs = []
        # we use page count to determine
        # if we have any results
        # get all results
        for page_number in range(1,72):
            #print "doing page %s" % page_number
            lab = self.get_results_for_page(page_number)
            #print "there are %s results" % len(results)
            #for result in results: print result["company_name"],",",
            labs.append(lab)
        self.labs = json.dumps(labs)

    
    @property
    def results(self):
        if self.companies:
            return self.companies
        return []

    def build_query(self,query):
        """ takes a query dictionary
            containing the page number
            and the search string
        """
        return self.query_url % query
     
    def make_page(self,query):
        f = urllib.urlopen(query)
        page = BeautifulSoup(f)
        return page
     
     
    def get_results_for_page(self,page_number):
        self._query['page'] = page_number
        query = self.build_query(self._query)
        page = self.make_page(query)
        # iteratively build lab list
        rows = page.find_all('tr')
        data = {}
        for row in rows:
            value = row.find('td').get_text()
            key = row.find('th').get_text()
            key = key.strip().encode('ascii','ignore')
            value = value.strip().encode('ascii','ignore')
            data[key] = value
        return data
 

def main():
    #############################
    #
    # usage: orcquery.py [-h] --name NAME [--type {company,business}]
    #
    # Query Business Names from the ORCJamaica Website
    #
    # optional arguments:
    # -h, --help            show this help message and exit
    # --name NAME, -n NAME  A business name or part of a business name to search
    #                    on
    # --type {company,business}, -t {company,business}
    #                    Type of search, defaults to "company", set to
    #                    "business" to search by business name
    #
    #############################
    

    ls = LabScraper()
    #find all companies that start with "a"
    ls.prepare_query()
    ls.run_query()
    print ls.labs
 
if __name__ == "__main__":
    main()
        
