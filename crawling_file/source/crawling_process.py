import os
import sys
import logging
import subprocess
import schedule


def sub_process_list_start(command_list):
    process_list = []
    for command in command_list:
        process = subprocess.Popen(command)
        process_list.append(process)

    return process_list


def crawling_process(keyword='사과', total_page='1'):
    print(f'### CURRENT DIR {os.getcwd()}')
    print(f'### KEYWORD : {keyword}, SEARCH_PAGE : {total_page}')
    crawling_command1 = ['python', 'coupangCrawling.py', keyword, total_page]
    crawling_command2 = ['python', 'emartCrawling.py', keyword, total_page]
    crawling_command3 = ['python', 'gmarketCrawling.py', keyword, total_page]
    crawling_command4 = ['python', 'naverCrawling.py', keyword, total_page]
    # crawling_command4 = ['python', 'naverCrawling.py', keyword, '10']
    command_list = [crawling_command1, crawling_command2,
                    crawling_command3, crawling_command4]

    process_list = sub_process_list_start(command_list=command_list)

    command = input()
    if command == 'exit':
        for process in process_list:
            process.kill()


if __name__ == '__main__':
    argc = len(sys.argv)
    keyword = total_page = ''

    if argc == 1:
        crawling_process()
    elif argc == 2:
        keyword = sys.argv[1]
        crawling_process(keyword=keyword)
    elif argc == 3:
        keyword = sys.argv[1]
        total_page = sys.argv[2]
        crawling_process(keyword=keyword, total_page=total_page)

    #################### 스케줄러 코드 #######################
    # schedule_list = []
    # schedule_list.append(schedule.every().day.at(
    #     '11:00').do(crawling_process, keyword, total_page))
    # schedule_list.append(schedule.every().day.at(
    #     '19:00').do(crawling_process, keyword, total_page))
    # for job in schedule_list:
    #     schedule.cancel_job(job)
    #################### 스케줄러 코드 #######################
