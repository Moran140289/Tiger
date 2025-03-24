

class Validation(object):
    @classmethod
    def check_identical_value(cls, title, current_value, expected_value):
        '''
        Generic function to check that two values are identical.
        @param current_value: First value to compare
        @param expected_value: Second value to compare
        @raise ValueError: In case value is empty or not equal
        '''

        if not cls.is_identical_value(current_value, expected_value):
            raise ValueError("{} expected value = {}, current value = {}".format(title.title(), expected_value, current_value))
    
    @classmethod
    def validate_elements_in_list(cls, title, elements_list, supported_list, exception = Exception):
        '''
        validate each element in a list of elements are inside a supported list
        @param title: String to include in the success \ failed messages
        @param supported_list: list of allowable values
        @param elements_list: list of elements, for each elements checks if inside supported_list
        @raise exception: if any an element of elements_list is not in supported_list, raise exception(info)
        @note: a single value can be inserted as elements_list or supported_list
        '''
        for element in elements_list:
            if element not in supported_list:
                raise exception("{} - {} not in {}".format(title, element, supported_list))
    
    @classmethod
    def is_identical_value(cls, current_val, expected_val):
        '''
        check if two values are equal
        @param current_val,expected_val(same type): current_val == expected_val
        @return(bool): returns the result  
        '''
        result = (current_val == expected_val)
        return result
    
    @classmethod
    def validate_limits_min_max(cls, current_val, min_limit, max_limit, info = "value is out-of-limits", exception = Exception):
        '''
        validate value is between limits
        @param current_val,min_limit,max_limit(int\float): min_limit <= current_val <= max_limit
        @param cast(cast type): cast both values to this type, can be None incase no cast needed
        @raises info(str),exception(Exception): raises exception(info)
        '''
        if not Validation.is_limits_min_max(current_val, min_limit, max_limit):
            raise exception(info)
    
    @classmethod
    def is_limits_min_max(cls, current_val, min_limit, max_limit):
        '''
        check if value is between limits
        @param current_val,min_limit,max_limit(int\float): min_limit <= current_val <= max_limit
        @return(bool): returns the result  
        '''
        result = (min_limit <= current_val <= max_limit)
        return result

    @classmethod
    def validate_input_parameter_in_range(self, name, value, from_val = None, to_val = None, exception = ValueError):
        '''
        Validate input parameter is in range: [from_val : to_val]
        Usage Example: self._validate_input_parameter("age", 20, 18, 22)
        @param name: name of the parameter - for logging
        @param value: current value
        @param from_val: start range of val. if None validate partial range value <= to_val
        @param to_val: end range of val. if None validate partial range from_val <= value
        @param exception: type of exception to raise
        @raise exception: in case input parameter is invalid OR can't cast value to relevant type OR in case (from_val == None and to_val == None)
        '''
        if value is None:
            raise exception("Invalid value for '%s' input parameter, must be between [%s - %s] and not None" % (
            name, from_val, to_val))

        if to_val is None:
            if from_val <= value:
                return
            else:
                raise exception("Invalid value for '%s' input parameter, must be %s >= %s" % (name, value, from_val))
        if from_val is None:
            if value <= to_val:
                return
            else:
                raise exception("Invalid value for '%s' input parameter, must be %s <= %s" % (name, value, to_val))
        if value < from_val or value > to_val:
            raise exception("Invalid value for '%s' input parameter, must be between [%s - %s] and not %s" % (
                name, from_val, to_val, value))


class ConfigException(Exception):
    pass

if __name__ == "__main__":
    print(Validation.is_identical_value(None, True))
