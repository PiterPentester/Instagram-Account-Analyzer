from selenium import webdriver
import sys
import datetime
import time



#time.sleep() functions are used to give loading time to the driver

WAIT_TIME = 2 #How much time a page gets to load before it starts searching for elements, depends on speed of intrnet


class IgAccountAnalyzer:
    def __init__(self,accountName):
        self.accountName = accountName
        self.driver = webdriver.Firefox()
        self.picCount = 0
        self.followerCount="" #String since the number of followers on instagram is not always a number


    #Goes to the profile of the given profile name and gets the number of followers and posts
    def post_and_follower_numbers(self):
        accountName = self.accountName
        driver = self.driver
        driver.get("https://www.instagram.com/"+accountName+"/")
        time.sleep(WAIT_TIME)
        pictureCount = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[1]/a/span").text  #Number of posts
        followerCount = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").text #Number of followers
        pictureCount = pictureCount.replace(',','') #if the number has a seperating comma
        self.picCount = int(pictureCount)
        self.followerCount = followerCount


    #Checks if an account is private
    def check_if_private(self):
        try:
            webdriver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div/div/h2")
            return False
        except:
            return True


    #Extracts all the links for each picture per given profile
    def get_links(self):
        numOfPics = self.picCount
        driver = self.driver
        listOfPics = []
        #Keeps scrolling until the number of links to pictures is the same as the number of "posts" on profile.
        #This step is necessary since we do not know how many scrolls is needed to get all the pictures in view
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(WAIT_TIME)
            anchorTags = driver.find_elements_by_tag_name('a')  #Gets a list of every anchor tag element on the webpage.
            for tag in anchorTags:
                #Only get the anchor tags elements with href values that contain "com/p" since it is a picture
                if ('com/p/' in tag.get_attribute('href')):
                    if(tag.get_attribute('href') not in listOfPics):
                        listOfPics.append(tag.get_attribute('href'))
            if(len(listOfPics) == numOfPics):
                break
        return listOfPics #List of post links


    #Gets the number of likes per post
    def get_likes_and_followers(self,listOfPics):
        driver = self.driver
        likeNumbers = {}
        if (self.picCount>0):
            for pic in listOfPics:
                driver.get(pic)
                time.sleep(WAIT_TIME)
                likes = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[2]/section[2]/div/div/a/span")
                likeNumbers[pic] = int(likes.text)
        return likeNumbers


    #Nicely prints out the results in a CSV file
    def documentResults(self,listOfPics,likeNumbers):
        fileName = str(self.accountName) + " IG Data"+".tsv"
        with open(fileName,'w') as file:
            file.write(datetime.datetime.today().strftime('%Y-%m-%d')+"\n")
            file.write("Profile:"+"\t"+self.accountName+"\n")
            file.write("Follower Count:"+"\t"+self.followerCount+"\n")
            file.write("Picture Count:" +"\t"+str(self.picCount)+"\n")
            file.write("\n \nThe program lists the pictures from most to least recent uploads \n \n")
            if(self.picCount > 0):
                tmp = 1
                for pic in listOfPics:
                    file.write(str(tmp)+": "+"\t"+ str(likeNumbers[pic])+"\n")
                    tmp+=1
            else:
                file.write("No pictures")

    def document_results(self):
        fileName = str(self.accountName) + " IG Data"+".tsv"
        with open(fileName,'w') as file:
            file.write(datetime.datetime.today().strftime('%Y-%m-%d')+"\n")
            file.write("Profile:"+"\t"+self.accountName+"\n")
            file.write("Follower Count:"+"\t"+self.followerCount+"\n")
            file.write("Picture Count:" +"\t"+str(self.picCount)+"\n")
            file.write("\n \nThe account is private, posts cannot be seen")


    #Function that implements the entire funcionality of the class
    def get_data(self):
        self.post_and_follower_numbers()
        accountIsPrivate = self.check_if_private()
        if(accountIsPrivate == True):
            links = self.get_links()
            likesNdFollowers = self.get_likes_and_followers(links)
            self.document_results(links,likesNdFollowers)
        else:
            self.document_results()

        print("File has been written")






def main(argv):
    accountNames=""
    print("Input Instagram account name:")
    analyzer = IgAccountAnalyzer(input())
    analyzer.get_data()



if __name__ == "__main__":
    main(sys.argv)
