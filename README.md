# Web-scraping-projects

Stack overflow scraping using various Python frameworks such as Beautiful Soup, Selenium, Scrapy 

## Definition :- Scrapping information from stack overflow

**Site** :- https://stackoverflow.com/questions/tagged/python (ex : python tag)

- There are 1,92,53,044 questions are available in stack overflow
- I have to scrap first 1000 pages for any given tags. containing 50 questions each.  so total 50,000 question's info to scrap
- In this task i have to scrap these things from each question
  - Question
  - Answer if it's available
    - comment of answer if it's available
  - Up votes
  - Down votes
  - Views
  - Question title
  - Description
  - Date
  - User

## Challenges : 

- scrap the data through pagination  [1000 different pages]
- dealing with the huge amount of data
- storing this huge amount data into the database
- only store a question which is not  available in the database
- question can have multiple answer, and answer can have multiple comments



## Steps to achieve : 

- i have to scrap the questions for any given tag. this URL used in SO for presenting all the question of that particular tag - "https://stackoverflow.com/questions/tagged/{tag}" [here tag is any selected tag]

  - so there are lots of various questions are available for one particular tag. so i have to go through all question with the pagination and the URL for that is : "https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page=1&pagesize=50" 

    i have to scrap first 50,000 question so the total page will be 1000 as page size is 50.

- stack overflow has unique id for each and every question. so after getting into the particular one question i will fetch the question id of that question and with the help of that question id i will scrap the whole information of the question. 

    URL : https://stackoverflow.com/questions/{que_id}" 

     [here que_id is unique integer for each question we get through scrapping the questions page]

- here i use web-crawling framework __scrapy__ to scrap the stack overflow data
