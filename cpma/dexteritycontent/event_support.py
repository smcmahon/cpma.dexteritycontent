# View support for aggregated events View

import calendar
from datetime import date
from datetime import datetime
from datetime import timedelta

from five import grok
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

aday = timedelta(1)


def startOfMonth(adate):
    return adate.replace(day=1)


def startOfNextMonth(adate):
    return endOfMonth(adate) + aday


def endOfMonth(adate):
    days_in_month = calendar.monthrange(adate.year, adate.month)[1]
    return adate.replace(day=days_in_month)


def cmpstart(a, b):
    return cmp(a['start'], b['start'])


class EventSupport(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')

    def siteEvents(self):
        """ return all events (as brains) that end on or after
            start of current month
        """

        pc = getToolByName(self.context, 'portal_catalog')
        start_month = date.today().replace(day=1)
        rez = pc.queryCatalog({
            "portal_type": 'standardevent',
            "review_state": ("published", "visible"),
            'end': {'query': start_month, 'range': 'min'},
            "sort_on": "start",
            "sort_order": "reverse",
            })
        events = []
        for b in rez:
            events.append({
                'title': b.Title,
                'description': b.Description,
                'start': b.start,
                'end': b.end,
                'url': b.getURL(),
                })
        return events

    def getMonths(self):
        # get up to 24 months of events, returned in a list of months:
        # [("Month, Year", [list of event dicts in start date order])]

        # build list of months with empty event lists
        today = date.today()
        months = [(startOfMonth(today), endOfMonth(today), [])]
        for i in range(1, 24):
            today = startOfNextMonth(today)
            months.append((startOfMonth(today), endOfMonth(today), []))

        # now, see which events go with which months
        events = self.siteEvents()
        for amonth in months:
            start, end, elist = amonth
            for event in events:
                estart = event['start'].date()
                eend = event['end'].date()
                if estart <= end and eend >= start:
                    # Found a winner. we'll append it to the list. But, first,
                    # copy the event so that we can fix the start date
                    # to be the beginning of the month and end date to
                    # be the end
                    event_copy = event.copy()
                    if estart < start:
                        event_copy['start'] = datetime.combine(start, event['start'].time())
                    if eend > end:
                        event_copy['end'] = datetime.combine(end, event['end'].time())
                    sday = event_copy['start'].date().day
                    eday = event_copy['end'].date().day
                    if sday == eday:
                        event_copy['drange'] = "%d" % sday
                    else:
                        event_copy['drange'] = "%d-%d" % (sday, eday)
                    elist.append(event_copy)
            elist.sort(cmpstart)
        return [(m[0].strftime('%B, %Y'), m[2]) for m in months if m[2]]

    def render(self):
        return u"Months: %s" % self.getMonths()

