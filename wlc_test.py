

with open('sw_data.txt', 'r') as file:
    data = file.read()

# ap_data = data.split('\n')[1:]
# ap_mac_name = {}
# for row in ap_data:
#     row_col = row.split(' ')   # [34:62:88:e2:46:20, 58:f3:9c:bd:bf:8b, AP1F-05, 10.230.15.145, Joined]
#     ap_mac_name.update({f'{row_col[8]}': f'{row_col[4]}'})
#
# with open('ap_mac_name.txt', 'w') as file:
#     for k in ap_mac_name:
#         file.write(f'{k} ---> {ap_mac_name[k]}\n')


sw_data = data.split('\n')[1:]
ap_name_port = {}
for row in sw_data:
    row_col = row.split(' ')
    ap_name_port.update({f'{row_col[0]}': f'{row_col[10]+row_col[11]}'})

with open('ap_name_port.txt', 'w') as file:
    for k in ap_name_port:
        file.write(f'{k} ---> {ap_name_port[k]}\n')

config_commands = []
for k in ap_name_port:
    config_commands.append(f'default int {ap_name_port[k]}\n '
                            f'int {ap_name_port[k]} \n '
                            f'description To-{k} \n '
                            f'switchport trunk encap dot \n '
                            f'switchport mode trunk \n '
                            f'switchport trunk allowed vlan 106, 107, 500')


configured_data = device_connection(data_[0], config_commands)
print(ap_name_port)