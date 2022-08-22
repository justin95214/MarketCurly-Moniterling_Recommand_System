import os
import subprocess


def server_start(command_list):
    process_list = []
    for command in command_list:
        process = subprocess.Popen(command)
        process_list.append(process)

    return process_list


if __name__ == '__main__':
    print(f'### current dir {os.getcwd()}')
    keyword = input('크롤링할 키워드 입력 : ')
    total_page = '5'
    crawling_command1 = ['python', 'coupangCrawling.py', keyword, total_page]
    # crawling_command2 = ['python', 'emartCrawling.py', keyword]
    crawling_command3 = ['python', 'gmarketCrawling.py', keyword, total_page]
    #crawling_command4 = ['python', 'naverCrawling.py', keyword, total_page]
    crawling_command4 = ['python', 'naverCrawling.py', keyword, '10']
    command_list = [crawling_command1,
                    crawling_command3, crawling_command4]

    process_list = server_start(command_list=command_list)

    command = input()
    if command == 'exit':
        for process in process_list:
            process.kill()
