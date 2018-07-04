import cplex, string, random, shutil

CPLEX_INFINITY = cplex.infinity

def random_string_generator(N):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def copy_cplex_model(model):
	from os import mkdir, path
	folder = "tmp_"+random_string_generator(12)
	m_name, p_name = path.join(folder,random_string_generator(9)+".lp"), path.join(folder,random_string_generator(9)+".lp")
	mkdir(folder)

	model.write(m_name)
	model.parameters.write_file(p_name)

	new_model = cplex.Cplex()
	new_model.parameters.read_file(p_name)
	new_model.read(m_name)

	shutil.rmtree(folder)
	return new_model


class Solution(object):
	def __init__(self, value_map, status, **kwargs):
		self.__value_map = value_map
		self.__status = status
		self.__attribute_dict = kwargs

	def __getitem__(self, item):
		if hasattr(item, '__iter__') and not isinstance(item, str):
			return {k: self.__value_map[k] for k in item}
		elif isinstance(item, str):
			return self.__value_map[item]
		else:
			raise TypeError('\'item\' is not a sequence or string.')

	def set_attribute(self, key, value):
		self.__attribute_dict[key] = value

	def var_values(self):
		return self.__value_map

	def status(self):
		return self.__status

	def attribute_value(self, attribute_name):
		return self.__attribute_dict[attribute_name]

	def attribute_names(self):
		return self.__attribute_dict.keys()
