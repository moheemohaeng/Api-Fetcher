import schedule
import time


def main_run():

    # for subreddit_name in SUB_REDDIT_LIST:
    #     print("================================= SUBREDDIT : ", subreddit_name, '=================================')
    #     try:
    #         submission_in_subreddit(subreddit_name)
    #     except:
    #         print('!!!!!!!!!!!!!!!!!!!!!!!!!fail read subreddit : ', subreddit_name, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    # # if os.path.exists('C:/Users/user/Desktop/reddit test/meta') :
    #     #     shutil.rmtree('C:/Users/user/Desktop/reddit test/meta')
    # # if os.path.exists('C:/Users/user/Desktop/reddit test/data') :    
    #     #     shutil.rmtree('C:/Users/user/Desktop/reddit test/data')
    print("ddddddddddddddd")
    time.sleep(5)

if __name__ =='__main__':
    # os.mkdir('C:/Users/user/Desktop/reddit test/meta')
    # os.mkdir('C:/Users/user/Desktop/reddit test/data')
    main_run()
    schedule.every(5).seconds.do(main_run)
    while True:
        schedule.run_pending()
        time.sleep(1)
