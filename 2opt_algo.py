from math import hypot
from timeit import default_timer
import googlemaps

class Node:
	"""
	represents a node in a TSP tour
	"""
	def __init__(self, coords):
		self.num = coords[0] # start position in a route's order
		self.x = coords[1]   # x coordinate/Lat
		self.y = coords[2]   # y coordinate/Lng
		self.key = 'AIzaSyCUglL7I7KhZY_7Ei2jJiGTA-10uqrJ-RE'
		self.client = googlemaps.Client(self.key)

	def __str__(self):
		"""
		returns the string representation of a Node
		"""
		return str(self.num)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def euclidean_dist(self, other):
		dx = self.x - other.x
		dy = self.y - other.y
		return hypot(dx, dy)

	def google_dist(self, other):
		origins = [{'lat': other.x, 'lng': other.y}]
		destinations = [{'lat': self.x, 'lng': self.y}]
		matrix = self.client.distance_matrix(origins, destinations)
		element = matrix['rows'][0]['elements'][0]
		return float(element['distance']['text'][:len(element['distance']['text']) - 3])

def get_coords(line):
	"""
	returns the line data as numerals, None if line contains more than
		3 items or non-numerics in the line
	line - string containing the data
	"""
	data = line.split()
	if len(data) == 3:
		try:
			coords = (int(data[0]), float(data[1]), float(data[2]))
			return coords
		except ValueError:
			pass
	return None

def route_distance(route):
	"""
	returns the distance traveled for a given tour
	route - sequence of nodes traveled, does not include
	        start node at the end of the route
	"""
	dist = 0
	prev = route[-1]
	# print(route)
	for node in route:
		# print(node)
		dist += node.google_dist(prev)
		prev = node
	return dist

def print_results(route, filename, parsing_time, opt_time):
	"""
	prints the nodes in the final route and route information
	route - route to print
	filename - name of the original input filename
	time - time to run 2opt
	startnode - start node of original tour if randomized
	"""
	for node in route:
		print(node)
	print(-1)
	print("Original input file : " + filename)
	print("Dimension : " + str(len(route)))
	print("Total Distance : " + str(route_distance(route)))
	print("Time to parse data : %.2f seconds" % parsing_time)
	print("Time to run 2opt : %.2f seconds" % opt_time)

def swap_2opt(route, i, k):
	"""
	swaps the endpoints of two edges by reversing a section of nodes,
		ideally to eliminate crossovers
	returns the new route created with a the 2-opt swap
	route - route to apply 2-opt
	i - start index of the portion of the route to be reversed
	k - index of last node in portion of route to be reversed
	pre: 0 <= i < (len(route) - 1) and i < k < len(route)
	post: length of the new route must match length of the given route
	"""
	assert i >= 0 and i < (len(route) - 1)
	assert k > i and k < len(route)
	new_route = route[0:i]
	new_route.extend(reversed(route[i:k + 1]))
	new_route.extend(route[k+1:])
	assert len(new_route) == len(route)
	return new_route

def run_2opt(route):
	"""
	improves an existing route using the 2-opt swap until no improved route is found
	best path found will differ depending of the start node of the list of nodes
		representing the input tour
	returns the best path found
	route - route to improve
	"""
	improvement = True
	best_route = route
	best_distance = route_distance(route)
	while improvement:
		improvement = False
		for i in range(len(best_route) - 1):
			for k in range(i+1, len(best_route)):
				new_route = swap_2opt(best_route, i, k)
				new_distance = route_distance(new_route)
				if new_distance < best_distance:
					best_distance = new_distance
					best_route = new_route
					improvement = True
					break #improvement found, return to the top of the while loop
			if improvement:
				break
	assert len(best_route) == len(route)
	print (best_route)
	return best_route

def parse_input_route(filename):
	"""
	returns initial route as read from input file, None if parsing errors occur
	filename - name of the input file with '.tsp' extension
	"""
	f = open(filename, 'r')
	route = []

	# Parse nodes
	for line in f:
		if "EOF" in line:
			break
		coords = get_coords(line)
		if coords != None:
		    route.append(Node(coords))
		# print(coords)
	f.close()

	return route

# Parse input file
parse_start = default_timer()
filename = 'data/coords.txt'
route = parse_input_route(filename)
parse_end = default_timer()

# Run 2opt
start = default_timer()
route = run_2opt(route)
end = default_timer()
print_results(route, filename, (parse_end - parse_start), (end - start))