"""Scraper for Eleventh Circuit of Appeals
CourtID: ca11
Court Short Name: ca11
Reviewer: Mike Lissner
History:
 - 2018-07-25: Created by Taylor Higgins
"""
from lxml import html
from datetime import datetime
from juriscraper.OralArgumentSite import OralArgumentSite
from juriscraper.lib.string_utils import titlecase 
'''Titlecases input text
    This filter changes all words to Title Caps, and attempts to be clever
    about *un*capitalizing SMALL words like a/an/the in the input.
    The list of "SMALL words" which are not capped comes from
    the New York Times Manual of Style, plus 'vs' and 'v'.
    This will fail if multiple sentences are provided as input and if the
    first word of a sentence is a SMALL_WORD.
    List of "BIG words" grows over time as entries are needed.'''
    

from juriscraper.lib.string_utils import convert_date_string
'''Sanitize date string and convert into standard date object
    :param date_string: A string to convert to a datetime object.
    :param fuzzy: whether fuzzy string matching should be used, as defined by
    dateutil.
    :param datetime: If True, return a datetime object. If false, cast to a
    date.
    :return: datetime or date object, depending on the datetime parameter.
    '''


#http://www.ca11.uscourts.gov/oral-argument-recordings

class Site(OralArgumentSite):
    def __init__(self, *args, **kwargs):
        super(Site, self).__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.url = 'http://www.ca11.uscourts.gov/oral-argument-recordings'
        self.method = 'POST'
        self.uses_selenium = False
        # Not sure if I'll create a backscraper yet.
        self.back_scrape_iterable = None
        """
            Required fields - InsanityExceptions will be thrown if omitted.
            Remove this comment before submission.
        """
    def _get_download_urls(self):
        """ WORKS! Working on getting and testing the right xpath, I don't want it too specific as
        to disallow cycling through all of them. can i do div and class instead like beautiful soup? """
        path = '//*[@class="jp-jplayer jp-player--loaded-processed"]//@src'
        #jp-jplayer jp-player--loaded-processed is div class name then link is in audio src
        #//*[@id="jp_audio_0"]
        #//*[@id="jplayer-node-1349-field-oar-audio-file-1535402067"]
        
        return list(self.html.xpath(path))

    def _get_case_names(self):
        """ WORKS"""
        case_names = []
        for case in self.html.xpath('//td[@class="views-field views-field-field-oar-case-name-long fix-width-30"]/text()'):
        #//*[@id="block-system-main"]/div/div/div[3]/table/tbody/tr[1]/td[2]
        #can't start with tr because class name is odd and then even so two not one
            s = html.tostring(case, method='text',encoding='unicode')
            #case_names.append(titlecase(s)) #not needed since not all caps
            #we want it to be like Nadim v. Jenny yeah?
            case_names.append(s)
        #print case_names
        return case_names


    def _get_case_dates(self):
        """ This is an example of a date field. Note that the format string
            will likely need to be updated to  match the date formats
            on the site you are scraping. The datetime formats can be found
            here: http://docs.python.org/2/library/datetime.html
        """
        path = '//td[@class="views-field views-field-field-oral-argument-date"]/span[@class="date-display-single"]/text()'
        #//*[@id="block-system-main"]/div/div/div[3]/table/tbody/tr[1]/td[3]/span
        return [convert_date_string(data_string) for date_string in self.html.xpath(path)]
        #why first return in list, second in array third in nothing?


    def _get_docket_numbers(self):
        """ Worked"""

        path = '//td[@class="views-field views-field-title fix-width-7"]/text()'

        return list(self.html.xpath(path))









        