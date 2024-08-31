class Simulator:
    def __init__(self):
        self.variables = {}  # Stores variable probabilities
        self.dependencies = set()  # Stores dependent variable pairs

    def _set_variable(self, var, prob):
        """
        Sets the probability for a variable. Handles conditional probability.
        """
        if '|' in var:
            # Add dependency for conditional probabilities (A|B)
            v1, v2 = var.split('|')
            self.dependencies.add((v1, v2))

        if not isinstance(prob, (int, float)):
            raise ValueError('Probability value should be a number')
        
        self.variables[var] = prob

    def _get_value(self, var, force=True):
        """
        Retrieves the probability of a variable or its complement.
        """
        # Return the variable's probability if already known
        if var in self.variables:
            return self.variables[var]

        # Handle complement (e.g., A -> A!, A! -> A)
        complement_var = f'{var[:-1]}' if var[-1] == '!' else f'{var}!'
        if complement_var in self.variables:
            return 1 - self.variables[complement_var]

        # Force calculation by checking dependencies
        if force:
            result = None
            for dep_var in self.dependencies:
                if var in dep_var:
                    if not self._are_independent(dep_var[0], dep_var[1]):
                        if result is None:
                            result = 0
                        result += self._get_intersection_prob(dep_var[0], dep_var[1])
            return result

        return None

    def _set_dependent(self, var1, var2):
        """
        Adds a dependency between two variables.
        """
        self.dependencies.add((var1, var2))

    def _are_independent(self, var1, var2):
        """
        Checks if two variables are independent.
        """
        return (var1, var2) not in self.dependencies and (var2, var1) not in self.dependencies

    def _get_intersection_prob(self, var1, var2, force=True):
        """
        Calculates the intersection probability P(A ∩ B).
        """
        # Check for existing values for intersection (var1^var2 or var2^var1)
        value = self._get_value(f'{var1}^{var2}', force=False)
        if value is not None:
            return value

        value = self._get_value(f'{var2}^{var1}', force=False)
        if value is not None:
            return value

        # Calculate intersection based on independence or conditional probabilities
        value_1 = self._get_value(var1, force=False)
        value_2 = self._get_value(var2, force=False)
        if value_1 is not None and value_2 is not None:
            if self._are_independent(var1, var2):
                return value_1 * value_2
            
            value_union = self._get_union_prob(var1, var2, force=False)
            if value_union is not None:
                return value_1 + value_2 - value_union

        if force:
            value_condition_1 = self._get_condition_prob(var1, var2, force=False)
            if value_condition_1 is not None and value_2 is not None:
                return value_condition_1 * value_2

            value_condition_2 = self._get_condition_prob(var2, var1, force=False)
            if value_condition_2 is not None and value_1 is not None:
                return value_condition_2 * value_1

        return None

    def _get_union_prob(self, var1, var2, force=True):
        """
        Calculates the union probability P(A ∪ B).
        """
        value = self._get_value(f'{var1}+{var2}')
        if value is not None:
            return value

        value_1 = self._get_value(var1)
        value_2 = self._get_value(var2)
        if value_1 is not None and value_2 is not None:
            if force:
                value_intersection = self._get_intersection_prob(var1, var2, force=False)
                if value_intersection is not None:
                    return value_1 + value_2 - value_intersection
                else:
                    return value_1 + value_2

        return None

    def _get_condition_prob(self, var1, var2, force=True):
        """
        Calculates the conditional probability P(A|B).
        """
        value = self._get_value(f'{var1}|{var2}')
        if value is not None:
            return value

        if force:
            value_intersection = self._get_intersection_prob(var1, var2)
            value_var2 = self._get_value(var2)
            if value_intersection is not None and value_var2 is not None:
                return value_intersection / value_var2

            # Handle reverse condition (P(B|A))
            value_condition_reverse = self._get_condition_prob(var2, var1)
            value_var1 = self._get_value(var1)
            value_var2 = self._get_value(var2)
            if value_condition_reverse is not None and value_var1 is not None and value_var2 is not None:
                return value_condition_reverse * value_var1 / value_var2

        return None

    def get_prob(self, var):
        """
        Gets the probability for a given variable, handling intersections, unions, and conditional probabilities.
        """
        if '^' in var:  # Intersection
            v1, v2 = var.split('^')
            return self._get_intersection_prob(v1, v2)

        if '+' in var:  # Union
            v1, v2 = var.split('+')
            return self._get_union_prob(v1, v2)

        if '|' in var:  # Conditional
            v1, v2 = var.split('|')
            return self._get_condition_prob(v1, v2)

        # Default: direct value
        return self._get_value(var)

    def add_event(self, var, value):
        """
        Adds an event with its probability.
        """
        self._set_variable(var, value)
        return self
