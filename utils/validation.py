

class Validation(object):
    @classmethod
    def check_identical_value(cls, title, current_value, expected_value, cast = None, verbose = True):
        '''
        Generic function to check that two values are identical.
        @param title: String to include in the success \ failed messages
        @param current_value: First value to compare
        @param expected_value: Second value to compare
        @param verbose(bool): decide whether a message will be written to the log or not 
        @raise ValueError: In case value is empty or not equal
        '''
        cls._validate_received_value(current_value)
        current_value, expected_value = FormatUtils.cast_values([current_value, expected_value], cast)

        if not cls.is_identical_value(title, current_value, expected_value, verbose = verbose):
            raise ValueError("{} expected value = {}, current value = {}".format(title.title(), expected_value, current_value))
    
    @classmethod
    def _validate_received_value(cls, current_value):
        if (current_value is None) or (current_value == ""):
            raise ValueError("Recieved value is Empty\\None!".format(current_value))
    
    @classmethod
    def validate_elements_in_list(cls, title, elements_list, supported_list, cast = None, exception = Exception):
        '''
        validate each element in a list of elements are inside a supported list
        @param title: String to include in the success \ failed messages
        @param supported_list: list of allowable values
        @param elements_list: list of elements, for each elements checks if inside supported_list
        @raise exception: if any an element of elements_list is not in supported_list, raise exception(info)
        @note: a single value can be inserted as elements_list or supported_list
        '''
        elements_list = FormatUtils.cast_values(FormatUtils.format_value_to_list(elements_list), cast)
        supported_list = FormatUtils.format_value_to_list(supported_list)
        for element in elements_list:
            if element not in supported_list:
                raise exception("{} - {} not in {}".format(title, element, supported_list))
    
    @classmethod
    def validate_identical_lists_length(cls, lists_to_validate, exception = Exception):
        '''
        validate each list in lists to validate has the same length
        '''
        Validation.validate_list_length_greater_than(1, lists_to_validate)
        required_length = len(lists_to_validate[0])
        for single_list in lists_to_validate[1:]:
            Validation.validate_list_length(required_length, single_list, exception)
            
    @classmethod
    def validate_list_length(cls, required_length, list_to_validate, exception = Exception):
        '''
        @validate list has the required length
        '''
        list_length = len(FormatUtils.format_value_to_list(list_to_validate))
        if list_length != required_length:
            raise exception("list length must be = {}, list length recieved = {}".format(required_length, list_length))
    
    @classmethod
    def validate_list_length_greater_than(cls, min_required_length, list_to_validate, exception = Exception):
        '''
        validate lists length is greater than required length
        '''
        list_to_validate = FormatUtils.format_value_to_list(list_to_validate)
        list_length = len(list_to_validate)
        if list_length <= min_required_length:
            raise exception("list length must be greater than = {}, list length recieved = {}".format(min_required_length, list_length))
    
    @classmethod
    def validate_list_length_smaller_than(cls, max_required_length, list_to_validate, exception = Exception):
        '''
        validate lists length is smaller than required length
        '''
        list_length = len(list_to_validate) 
        if list_length >= max_required_length:
            raise exception("list length must be smaller than = {}, list length recieved = {}".format(max_required_length, list_length))
    
    @classmethod
    def is_identical_value(cls, title, current_val, expected_val, cast = None, verbose = True):
        '''
        check if two values are equal
        @param title:  
        @param current_val,expected_val(same type): current_val == expected_val
        @param cast(cast type): cast both values to this type, can be None incase no cast needed
        @return(bool): returns the result  
        '''
        expected_val, current_val = FormatUtils.cast_values([current_val, expected_val], cast)
        result = (current_val == expected_val)
        if verbose:
            cls._log_manager.log_info_msg('{} - {} == {} :: result = {}'.format(title, current_val, expected_val, result))
        else:
            cls._log_manager.log_debug_msg('{} - {} == {} :: result = {}'.format(title, current_val, expected_val, result))
        return result
    
    @classmethod
    def validate_limits_min_max(cls, current_val, min_limit, max_limit, cast = None, info = "value is out-of-limits", exception = Exception):
        '''
        validate value is between limits
        @param current_val,min_limit,max_limit(int\float): min_limit <= current_val <= max_limit
        @param cast(cast type): cast both values to this type, can be None incase no cast needed
        @raises info(str),exception(Exception): raises exception(info)
        '''
        if not Validation.is_limits_min_max(current_val, min_limit, max_limit, cast, False):
            raise exception(info)
    
    @classmethod
    def is_limits_min_max(cls, current_val, min_limit, max_limit, cast = None, verbose = True):
        '''
        check if value is between limits
        @param current_val,min_limit,max_limit(int\float): min_limit <= current_val <= max_limit
        @param cast(cast type): cast both values to this type, can be None incase no cast needed
        @return(bool): returns the result  
        '''
        current_val, min_limit, max_limit = FormatUtils.cast_values([current_val, min_limit, max_limit], cast)
        result = (min_limit <= current_val <= max_limit)
        if verbose:
            cls._log_manager.log_info_msg('{} <= {} <= {} :: result = {}'.format(min_limit, current_val, max_limit, result))
        return result
    
    @classmethod
    def validate_limits_abs_tolerance(cls, current_val, expected_val, tolerance, cast = None, info = "value is out-of-limits", exception = Exception):
        '''
        validate value is around value with specified tolerance
        @param current_val,expected_val,tolerance(int\float): abs(current_val - expected_val) <= tolerane
        @param cast(cast type): cast both values to this type, can be None incase no cast needed
        @raises info(str),exception(Exception): raises exception(info)
        '''
        if not Validation.is_limits_abs_tolerance(current_val, expected_val, tolerance, cast, False):
            raise exception(info)
    
    @classmethod
    def is_limits_abs_tolerance(cls, current_val, expected_val, tolerance, cast = None, verbose = True):
        '''
        check if value is around value with specified tolerance
        @param current_val,expected_val,tolerance(int\float): abs(current_val - expected_val) <= tolerane
        @param cast(cast type): cast both values to this type, can be None incase no cast needed
        @return(bool): returns the result  
        '''
        current_val, expected_val, tolerance = FormatUtils.cast_values([current_val, expected_val, tolerance], cast)
        result = (abs(current_val - expected_val) <= tolerance)
        if verbose:
            cls._log_manager.log_info_msg('|{}-{}| <= {} :: result = {}'.format(current_val, expected_val, tolerance, result))
        return result

    @classmethod
    def validate_type(cls, value, expected_type, exception = TypeError):
        '''
        validate only python standard types -str, int, float, list, tuple, dict, bool, bytes, bytearray, memoryview
        @param value: parameter value
        @param expected_type: expected parameter value
        @param exception: if type is not python standard types or expected type is not eq. to current type.
        '''
        try:
            cls.validate_elements_in_list('supported types', [expected_type], [str, int, float, list, tuple, dict, bool, bytes, bytearray, memoryview], exception = exception)
            current_type = type(value)
            if not current_type == expected_type:
                raise exception("current type is {}, expected type is {}".format(current_type, expected_type))
        except Exception:
            raise

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

    def _check_identical_value(self, title, current_value, expected_value, cast = float, additional_data = None, value_to_str_func = None):
        '''
        Generic function to check that two values are identical.
        @param title: String to include in the success \ failed messages
        @param current_value: First value to compare
        @param expected_value: Second value to compare
        @param cast: the casting needed for the above values
        @param additional_data: additional info for the log message. Can be the units / small "dictionary" / any additional string.
        @raise ConfigException: In case value is empty or not equal
        '''
        if (current_value == None) or (current_value == ""):
            raise ConfigException("Failed to the set %s to %s, current value is empty" % (title.lower(), expected_value))
        else:
            if cast == str:
                current_value = str(current_value).replace("\"", "").replace("\r", "").replace("\n", "").strip()
            if cast(current_value) == cast(expected_value):
                if value_to_str_func is None:
                    msg = "%s set to %s" % (title.title(), str(cast(current_value)))
                else:
                    msg = "%s set to %s" % (title.title(), value_to_str_func(cast(current_value)))
                if additional_data != None:
                    msg = "%s %s" % (msg, additional_data)
            else:
                raise ConfigException(self._format_msg("Failed to set %s to %s, current value = %s" % (title.lower(), cast(expected_value), cast(current_value))))


class ConfigException(Exception):
    pass

if __name__ == "__main__":
    print(Validation.is_identical_value(None, True, cast = bool))
