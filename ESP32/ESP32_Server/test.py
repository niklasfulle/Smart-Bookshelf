import sys

sys.path.append("../")
from utils.send_data import build_data_to_send_bytearray_arr

data = "testdpoawhjdpawohdapdihlawkdicaüpjfeüfosjeofpsefjofjsepofespofpsofposehfposhefpsnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsntestdpoawhjdpawohdapdihlawkdicaüpjfeüfosjeofpsefjpofjsepofespofpsofposehfposhefpsnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsnfspeoifbensifpiseapwdhapwi"

result = build_data_to_send_bytearray_arr(data)

print(result[0])
print(result[1])
print(result[2])
print(result[3])
print(result[4])
