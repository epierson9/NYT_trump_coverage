from urllib2 import urlopen
import datetime
import json
from IPython import embed
from pylab import *
import random
api_key = YOUR_API_KEY_HERE#'d2df0ae1341502ab27bfaf2693816071:13:63151714'
for headline_string in ['headlines', 'posts']:
    for query in ['clinton', 'trump', 'obama', 'cruz', 'kasich', 'sanders']:
        date = datetime.date(2016, 4, 16)
        n_posts = []
        dates = []
        datestrings = []
        fig, ax = subplots(figsize = [15, 3])
        monthsFmt = DateFormatter('%Y/%m')
        assert(headline_string in ['posts', 'headlines'])
        for i in range(50):
            datestring = str(date).replace('-', '')
            previous_datstring = str(date - datetime.timedelta(days=7)).replace('-', '')
            datestrings.append(datestring)
            if headline_string == 'posts':
                url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=%s&begin_date=%s&end_date=%s&api-key=%s' % (query, previous_datstring, datestring, api_key)
            elif headline_string == 'headlines':
                url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=headline:"%s"&begin_date=%s&end_date=%s&api-key=%s' % (query, previous_datstring, datestring, api_key)
            page = urlopen(url)
            data = page.read()
            d = json.loads(data)
            headlines = [d['response']['docs'][i]['headline'] for i in range(len(d['response']['docs']))]
            headlines = [a['main'] for a in headlines]
            if len(headlines) >= 1:
                random_headline = random.choice(headlines)
            else:
                random_headline = ''
            print '%-10s %5i %10s %10s %40s ' % (date, d['response']['meta']['hits'], query, headline_string, random_headline)
            n_posts.append(d['response']['meta']['hits'])
            dates.append(date)
            date = date - datetime.timedelta(days=7)
        ax.plot_date(dates, n_posts, '-')
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_major_formatter(monthsFmt)
        filename = '%s_%s_query.json' % (headline_string, query.replace(' ', '_'))
        json.dump({'datestrings':datestrings, 'n_posts':n_posts}, open(filename, 'w+'))
        ylabel(('Number of %s about %s' % (headline_string, query)).title())


        savefig('N_%s_%s.png' % (query, headline_string), format = 'png', dpi = 300)
