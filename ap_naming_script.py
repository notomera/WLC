
with open('ap_mac_name.txt') as file:
    data = file.read()

ap_data = data.split('\n')
print(ap_data)

for i in ap_data:
    try:
        ap_name_mac = i.split('>')
        print(ap_name_mac[0], ap_name_mac[1])
        with open('ap_naming_script.txt', 'a+') as file:
            file.write(f'config ap name {ap_name_mac[0]} {ap_name_mac[1]}\n')
    except IndexError:
        pass