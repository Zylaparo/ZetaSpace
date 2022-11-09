#imports all necessary modules
import requests, pathlib, time, csv, math

#setting up the basics for getting response objects
API_KEY='g0Cn4gDEUSSvzepqd85uEzzZcGMVfgtG'
base_url='https://api.nytimes.com/svc/search/v2/articlesearch.json'

#using the params parameter from the requests.get() method to pass in the API key and query
parameters={'q':'Johnny Depp Amber Heard trial','api-key':API_KEY}

#returns up to 10 results per page 
parameters['page']=0
#date ranges of the articles returned
parameters['begin_date']='20220412'
parameters['end_date']='20220510'
#defines the filter queries for the articles returned
my_filters='document_type:("article")'
#adds the filter queries key value pair to the parameters dictionary
parameters['fq']=my_filters

#defines the field limiting parameter and adds the fl key value pair to the parameter dictionary
fl_tuple=('headline','pub_date','section_name')
parameters['fl']=fl_tuple

#calls the api
response=requests.get(base_url,params=parameters)
#obtains the data
content=response.json() 

#Outputs the total number of results
results = content['response']['meta']['hits']
print(f"Number of results:  {results}.")
print("\n")

#Defines a function that will return the number of pages based on the number of hits returned
def page_calculator(r):
    total_pages = math.ceil(r/10)
    return total_pages
#Calls the page_calculator function
pages=page_calculator(results)
print(f"Total # of pages: {pages}")

parameters['page']=0

article_data=[]
#Transforms the Data
for t in range(pages):
    parameters['page']=t
    response=requests.get(base_url,params=parameters)
    content=response.json() 
    time.sleep(10)
    for i in content['response']['docs']:
        headline=i['headline']
        pub_date=i['pub_date']
        section_name=i['section_name']
        article_data.append({'headline':headline, 'pub_date':pub_date, 'section_name':section_name})
       
#Process of creating a path to the csv file
cwd=pathlib.Path.cwd()

article_dir=cwd/"article_data"

article_dir.mkdir(exist_ok=True)

article_file=article_dir/"NYTimes_article.csv"

article_file.touch()

#Writes the data into the csv file
with article_file.open(mode='a', encoding='utf-8', newline='') as article_csv:
    writer=csv.DictWriter(article_csv,fieldnames=["headline","pub_date", "section_name"])
    writer.writeheader()
    writer.writerows(article_data)
