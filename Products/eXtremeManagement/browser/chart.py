from zope import interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from xm.booking.timing.interfaces import IActualHours

from Products.eXtremeManagement.config import GRAPHS
from chart_api import Chart, LINE


class IChartView(interface.Interface):
    """Interface for charts"""

    def has_data():
        """test to see if there is any data to show"""

    def velocity_chart(self):
        """Draws the ammount of work estimated versus the ammount of work
           done
        """


class ChartView(BrowserView):

    def has_data(self):
        if not GRAPHS:
            return False
        if self.context.portal_type == 'Project':
            return len(self.get_iterations()) > 1
        return False

    def get_iterations(self):
        #XXX FIX ME, I AM TOO TIME EXPENSIVE
        iterations = [i for i in self.context.contentValues()
                              if i.portal_type=='Iteration']
        return iterations

    def get_total_estimate_iteration(self, iteration):
        #XXX FIX ME, I AM TOO TIME EXPENSIVE
        total = 0.0
        for story in [i for i in iteration.contentValues()
                              if i.portal_type=='Story']:
            if story.getRoughEstimate():
                total += story.getRoughEstimate()
        return total

    def velocity_chart(self):
        iterations = self.get_iterations()
        estimate_data = []
        work_data = []
        estimate_max = 0
        work_max = 0
        for iter in iterations:
            # XXX self.get_total_estimate_iteration(iter) should be doable
            #      in a neater way, just like IActualHours(iter).actual_time
            iter_total = int(self.get_total_estimate_iteration(iter)+0.5)
            work_total = int((IActualHours(iter).actual_time / 8.0) + 0.5)
            estimate_data.append(iter_total)
            work_data.append(work_total)
            estimate_max = max([iter_total, estimate_max])
            work_max = max([work_total, work_max])
        estimate_max = max([estimate_max, 1])
        work_max = max([work_max, 1])
        total_max = max([estimate_max, work_max])

        chart = Chart(type = LINE,
                      data = [estimate_data, work_data],
                      size = (max([40*len(iterations), 250]), 250))
        chart.setDataColors(['8cacbb', '008000'])
        chart.setLegend(['estimated', 'worked'])
        iter_num = '|'.join([str(i) for i in range(len(iterations))])
        day_num = '|'.join([str(i) for i in range(0, int(total_max+2), 2)])
        xtra = '&chxt=x,y,x,y&chxl='
        xtra += '0:|%s|' % iter_num
        xtra += '1:|%s|' % day_num
        xtra += '2:||iteration||3:||days|'
        chart.setCustom(xtra)
        return chart.getUrl()