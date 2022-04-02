class Rune:
    def __init__(self, element, power):
        self.element = element
        self.power = power

    def __repr__(self):
        return "<Rune |Element:%s |Power:%s >" % (self.element, self.power)
    def __str__(self):
        return "%s%s" % (self.element, self.power)
    def __eq__(self, other):
        if isinstance(other, Rune):
            return self.element == other.element and self.power == other.power

    def get_element(self):
        return self.element

    def get_power(self):
        return self.power

