class Simulator:
    def __init__(self):
        self.variables = {}
        self.dependency = set()
    
    
    def _set_variable(self, var, prob):
        if '|' in var:
            v1, v2 = var.split('|')
            self.dependency.add((v1, v2))
        if type(prob) not in [int, float]:
            raise Exception('prob value should be number')
        self.variables[var] = prob
    
    
    def _get_value(self, var, force=True):
        if var in self.variables:
            return self.variables[var]
        complement_var = f'{var[:-1]}' if var[-1] == '!' else f'{var}!'
        if complement_var in self.variables:
            return 1 - self.variables[complement_var]
        if force==True:
            result = None
            for dep_var in self.dependency:
                if var in dep_var:
                    if not self._are_independent(dep_var[0], dep_var[1]):
                        if result is None:
                            result = 0
                        result += self._get_intersection_prob(dep_var[0], dep_var[1])
            return result    
    
    
    def _set_dependent(self, var1, var2):
        self.dependency.add((var1, var2))
    
    
    def _are_independent(self, var1, var2):
        return (var1, var2) not in self.dependency and (var2, var1) not in self.dependency
    
    
    def _get_intersection_prob(self, var1, var2, force=True):
        value = self._get_value(f'{var1}^{var2}', force=False)
        if value is not None:
            return value
        value = self._get_value(f'{var2}^{var1}', force=False)
        if value is not None:
            return value
        else:
            value_1 = self._get_value(var1, force=False)
            value_2 = self._get_value(var2, force=False)
            if value_1 is not None and value_2 is not None:
                if self._are_independent(var1, var2):
                    return value_1 * value_2
                value_union = self._get_union_prob(var1, var2, force=False)
                if value_union is not None:
                    return value_1 + value_2 - value_union
            else:
                if force==True:
                    value_condition_1 = self._get_condition_prob(var1, var2, force=False)
                    if value_condition_1 is not None and value_2 is not None:
                        return value_condition_1 * value_2
                    else:
                        value_condition_2 = self._get_condition_prob(var2, var1, force=False)
                        if value_condition_2 is not None and value_1 is not None:
                            return value_condition_2 * value_1
            return None
    
    def _get_union_prob(self, var1, var2, force=True):
        value = self._get_value(f'{var1}+{var2}')
        if value is not None:
            return value
        else:
            value_1 = self._get_value(var1)
            value_2 = self._get_value(var2)
            if value_1 is not None and value_2 is not None:
                if force==True:
                    if self._are_independent(var1, var2):
                        value_intersection = self._get_intersection_prob(var1, var2, force=False)
                        if value_intersection is not None:
                            return value_1 + value_2 - value_intersection
                        else:
                            return value_1 + value_2
                    else:
                        value_intersection = self._get_intersection_prob(var1, var2, force=False)
                        if value_intersection is not None:
                            return value_1 + value_2 - value_intersection
            return None
        
        
    def _get_condition_prob(self, var1, var2, force=True):
        value = self._get_value(f'{var1}|{var2}')
        if value is not None:
            return value
        elif force==True:
            value_intersection = self._get_intersection_prob(var1, var2)
            value_var2 = self._get_value(var2)
            if value_intersection is not None and value_var2 is not None:
                return value_intersection / value_var2
            else:
                value_condition_reverse = self._get_condition_prob(var2, var1)
                value_var1 = self._get_value(var1)
                value_var2 = self._get_value(var2)
                if value_condition_reverse is not None and value_var1 is not None and value_var2 is not None:
                    return value_condition_reverse * value_var1 / value_var2
        return None
    
    def get_prob(self, var):
        if '^' in var:
            v1, v2 = var.split('^')
            return self._get_intersection_prob(v1, v2)
        elif '+' in var:
            v1, v2 = var.split('+')
            return self._get_union_prob(v1, v2)
        elif '|' in var:
            v1, v2 = var.split('|')
            return self._get_condition_prob(v1, v2)
        else:
            return self._get_value(var)
    
    def add_event(self, var, value):
        self._set_variable(var, value)
        return self