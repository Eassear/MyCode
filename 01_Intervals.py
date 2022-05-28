class SimpleInterval(object):
    def __init__(self, start, end):
        if start > end:
            raise ValueError ("Start must be grater than End")
        else:
            self.start = start
            self.end = end
        self.freq = 1
        
    def __str__(self):
        return "I("+ str(self.start) +", "+str(self.end) + ")"

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        else:
            return False
        
    def __lt__(self, other):
        if self.start < other.start:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.end > other.end:
            return True
        else:
            return False

    def upper(self, increment = 1):
        self.start += increment

    def lower(self, decrease = 1):
        self.end -= increment
    
    def length (self):
        return abs(self.end - self.start)

    def minimum(self):
        return self.start

    def maximum(self):
        return self.end

    def has_number(self, number):
        if number > self.start and number < self.end:
            return True
        else:
            return False

    def isInside(self, other):
        if self.start < self.other and self.end > other.end:
            return True
        else:
            return False
        
    def isContainedBy(self, other):
        if self.start > self.other and self.end < other.end:
            return True
        else:
            return False

    def cut_point(self, point):
        if point > self.start and point < self.end:
            return (SimpleInterval(self.start, point), SimpleInterval(point, self.end))
        

    def isCompetable(self, other):
        if self.start > other.end or self.end < other.start:
            return True
        else:
            return False

    def cut_interval(self, other):
        cuts = []
        if self == other:
            return [self, self, True]
        
        elif self.isCompetable(other) or self.end == other.start or other.end == self.start:
            return [self, other, True]

        elif self.start == other.start:
            if self.has_number(other.end):
                Interval1, Interval2 = self.cut_point(other.end)
                return [Interval1, Interval1, Interval2, True]
            else:
                Interval1, Interval2 = other.cut_point(self.end)
            return [Interval1, Interval1, Interval2, False]
        
        elif self.end == other.end:
            if self.has_number(other.start):
                Interval1, Interval2 = self.cut_point(other.start)
            else:
                Interval1, Interval2 = other.cut_point(self.start)
            return [Interval1, Interval2, Interval2, True]
        
        elif self.has_number(other.start):
            Interval1, Interval2 = self.cut_point(other.start)
            if Interval2.has_number(other.end):
                Interval3, Interval4 = Interval2.cut_point(other.end)
                return [Interval1, Interval3, Interval3, Interval4, True]
            else:
                Interval3, Interval4 = other.cut_point(Interval2.end)
            return [Interval1, Interval3, Interval3, Interval4, False]

        elif other.has_number(self.start):
            Interval1, Interval2 = other.cut_point(self.start)
            if Interval2.has_number(self.end):
                Interval3, Interval4 = Interval2.cut_point(self.end)
                return [Interval1, Interval3 ,Interval3, Interval4, False]
            else:
                Interval3, Interval4 = other.cut_point(Interval2.end)
            return [Interval1, Interval3 ,Interval3, Interval4, True]


class SimpleSchedule(object):
    def __init__ (self):
        self.num_freq = {}
        self.intervals = []
        self.sorted_list = []
        self.cut_list = []
        self.intervals_freq = {}

    def __str__(self):
        s = "( "
        for interval in self.intervals:
            s += str(interval) + ", "
        return s +")"

    def first(self):
        return min(self.intervals)

    def last(self):
        return max(self.intervals)

    def competables(self, selected_interval):
        competables_list= list(filter(lambda x: selected_interval.isCompetable(x), self.intervals ))
        return competables_list

    def update_num_freq(self, p1, p2):
        Dictionary = self.num_freq
        Sorted_Intervals = self.sorted_list
        if len(Sorted_Intervals) == 0:
            Dictionary[p1] = 1
            Dictionary[p2] = 1
        else:    
            goOn = True
            for key in Sorted_Intervals:
                if p1 <= key and goOn:
                    Dictionary[p1] = Dictionary[key]+1
                    goOn = False
                if p2 > key and not goOn and key > p1:
                    Dictionary[key] += 1
                if p2 <= key and not goOn:
                    Dictionary[p2] = Dictionary[key] +1
                    return Dictionary
            if goOn:
                Dictionary[p1] = 1
            Dictionary[p2] = 1
        return Dictionary

    def add_cuts(self, other):
        cuts = []
        i = 0
        start = True
        goOn = True
        if self.cut_list == []:
            self.cut_list.append(other)
        while i < len(self.cut_list) and goOn:
            if start:
                result = self.cut_list[i].cut_interval(other)
                start= False
            else:
                result =  self.cut_list[i].cut_interval(result[-2])
                    
            if  result[-1] == True:
                cuts.append(result[:-1])
                goOn = False
            else:
                cuts.append(result[:-2])
                i += 1
                
        if i == len(self.cut_list) and result[-1] == False:
            cuts.append([result[-2]])
            
        self.cut_list = flatten(cuts)                
        self.cut_list.sort(key=lambda x: x.end)
        
    
    def add_interval(self, start, end):
        self.intervals.append(SimpleInterval(start, end))
        self.dict_freq = self.update_num_freq(start, end)
        self.sorted_list = list(self.dict_freq.keys())
        self.sorted_list.sort()
        self.add_cuts(SimpleInterval(start, end))
        self.intervals_freq = countmap(self.cut_list)



def countmap(items):
    counts = dict()
    for i in items:
        counts[str(i)] = counts.get(str(i), 0) + 1
    return counts

def show(List):
    return list(map(lambda x : str(x), List))

def flatten(t):
    return [item for sublist in t for item in sublist]
