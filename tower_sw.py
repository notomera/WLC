from netmiko import ConnectHandler
from helper import connection_data, parsed_yaml


def device_connection(new_base_data, new_commands):
    device_ssh_data = ''
    device_ssh = ConnectHandler(**new_base_data)

    device_ssh.enable()
    device_name = device_ssh.find_prompt().split('#')[0]
    device_ssh.send_command('terminal length 0')

    for command in new_commands:
        device_ssh_data += device_ssh.send_command(command)

    return device_name, device_ssh_data


def main():
    inventory = 'inventory_sw.yml'
    data = parsed_yaml(inventory)
    base_data = data['base']
    devices = data['devices']

    all_data = connection_data(base_data, devices)

    for data_ in all_data:
        device_name, device_ssh_data = device_connection(*data_)
        sw_data = device_ssh_data.split('\n')[1:]

        ap_name_port = {}
        for row in sw_data:
            row_col = row.split(' ')
            ap_name_port.update({f'{row_col[0]}': f'{row_col[10] + row_col[11]}'})

        with open('ap_name_port.txt', 'a+') as file:
            for k in ap_name_port:
                file.write(f'{k} ---> {ap_name_port[k]}\n')

        for k in ap_name_port:
            config_commands = [
                               f'default int {ap_name_port[k]}',
                               f'int {ap_name_port[k]}',
                               f'description To-{k}',
                               f'switchport mode trunk',
                               f'switchport trunk native vlan 107'
                               ]

            base_data, commands = data_
            config_object = ConnectHandler(**base_data)
            output = config_object.send_config_set(config_commands)
            print(output)


if __name__ == '__main__':
    main()
