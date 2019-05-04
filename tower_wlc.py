from netmiko import ConnectHandler
from helper import connection_data, parsed_yaml


def device_connection(new_base_data, new_commands):
    device_ssh_data = ''
    device_ssh = ConnectHandler(**new_base_data)

    device_name = device_ssh.find_prompt().split('>')[0]

    for command in new_commands:
        device_ssh_data += device_ssh.send_command(command)

    return device_name, device_ssh_data


def main():
    inventory = 'inventory_wlc.yml'
    data = parsed_yaml(inventory)
    base_data = data['base']
    devices = data['devices']

    all_data = connection_data(base_data, devices)

    for data_ in all_data:
        device_name, device_ssh_data = device_connection(*data_)
        with open(f'{device_name}_data.txt', 'w') as captured_data:
            captured_data.write(device_ssh_data)

        ap_data = device_ssh_data.split('\n')[1:]

        ap_mac_name = {}
        for row in ap_data:
            row_col = row.split(' ')  # [34:62:88:e2:46:20, 58:f3:9c:bd:bf:8b, AP1F-05, 10.230.15.145, Joined]
            ap_mac_name.update({f'{row_col[8]}': f'{row_col[4]}'})

        with open('ap_mac_name.txt', 'a+') as file:
            for k in ap_mac_name:
                file.write(f'{k} > {ap_mac_name[k]}\n')

        clear_commands = []
        for k in ap_mac_name:
            clear_commands.append(f'clear ap config {k}')

        cleared_data = device_connection(data_[0], clear_commands)
        print(cleared_data)


if __name__ == '__main__':
    main()
