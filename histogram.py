from code.classes import stations, connection, trajectory, network
import seaborn as sn
import matplotlib.pyplot as plt

scores = []
counts = []
count = 0

for i in range(1000):
  count += 1
  counts.append(count)

  # Create network from our data
  test_network = network.Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')

  test_network.load_stations()
  test_network.load_connections()

  test_network.create_network()
  scores.append(test_network.quality_network)

plt.bar(counts, scores)
plt.show()
