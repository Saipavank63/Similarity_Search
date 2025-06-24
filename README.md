# similarity-search-application

# Step 1: Data Cleaning

The dataset for this project initially contained several columns that were not required to calculate similarity between products. The features that I needed to used to calculate similarity were (brand, sales_price, weight, rating). Initially, there were 2890, 8143 and 23746 null values in the sales_price, brand and weight columns respectively. Since one of the assumptions was that a given unique_id would exist in the dataset, I couldn't just drop the nul values from the dataset. I did a couple of different things in order to handle the null values and populate the dataset in the best possible manner from what I was given. First, for the brand column I populated the null values by using the product_name and product_url columns in order to find brands names for each null value. I did this by recognizing a pattern between both the columns where the first couple of words in the product_name and product_url columns were always the brand name. I was able to get the brand name from this pattern by first creating a dictionary where the key was the first word common between product_name and product_url and the value for each key was a list of all the product names for that specific key since some brands have multiple items. After doing that I then ran a longest common substring algorithm between every item of the list for each specific key where the first word in the lcs has to be equal to the key value. That way I was able to get all the brand names than had multiple words in their name and I stored this in another dictionary where the key was the key from the previous dictionary and the value was the lcs. Once I was able to extract the brand names correctly I updated the null values in the rand column with the subsequent right value by comparing the unique_id.

Next, I had to find a way to handle null values in sales_price and the weight column. I could not just fill in the null values with the mean or median of the column since that would compromise the integrity of my dataset and the corresponding similarity score that would be created would be completely wrong. So in order to handle null values in these columns better I went with the approach of KMeans clustering where I created clusters based on the rating and product_name column since both the columns were completely populated and both the columns are reasonable parameters to use for clustering. To create the clustering using the product_name column I had to first convert the words in each of the rows into vectors using TfidfVectorizer. After doing that I created clusters using k = 5 as my parameter. I got this value of k by plotting an elbow plot for value of k VS WCSS where 5 was my elbow point. After creating the clusters I filled in the null values in the sales_price and weight column by taking the mean of whichever cluster the null values fell in and assigning the respective null values accordingly.

After doing this my dataset was now completely cleaned up for all the features I was going to use to calculate the similarity score on and now all I had to do was save this cleaned dataset into another csv file.

# Step 2: Model Building

Now, for the actual model building part it was fairly straightforward. All I had to do before feeding in the values into the cosine similarity function to calculate the score was scale the data using Standard Scaler and one hot encode all the unique values in the brand column. After that I got the similarity score I stored all the scores for each of the products compared to the given unique_id in a new similarity_score data frame which contained 'unique_id', 'similarity_score' and 'rating' as its columns. Next, to get only get num_similar number of items from the top of the data frame was also fairld straightforward and I stored all these unique_ids in my output list which would in turn be returned. In case of a tie between similarity scores, I used rating as my tie-breaker metric which is why I stroed rating as well in my similarity_score data frame.

# Step 3: APIs

After cleaning my dataset and making my model I now needed to create an API that would make a GET request to my model and get the list of similar product ids. I used FAST API for that as per the requirements and I also implemented error handling for various different HTTP error codes that the application could potentially run into.

# Step 4: Creating UI with streamlit

After making my model and the GET request API, I created a simple UI using streamlit in order to be able to test the application in a more user friendly manner.

# Step 5: Dockerization

After completeing all the requirements of the project so far the next step was to create a docker image that can be deployable on kubernetes. The process for this consisted of creating the Docker file with the right specifications, creating a requirements.txt file of the libraries used in the application and finally using the Docker client to create an image of the application. After creating the docker image I tested it by running the image locally on my device and it worked as intended.

# Step 6: Deploying using K8s

The next step was deployment using minikube to my local K8 cluster. This required creating a deployment.yaml and service.yaml files that were required for the pod in order to access and deploy the docker image correctly. I was able to successfully deploy my docker image to my local pod on my local minikube cluster with the pod running normally.

# Step 6: Optimisation and what can be improved

In the optimisation section of the assignment I explored a couple of different avenues including using a vector search algorithm as well as just reducing the dimensionality of my current dataset by using something other than one hot encoding. In relation to using a different vector search algorithm that would work better with much larger datasets, I have narrowed down my selection to FAISS and I will outline my approach to implementing FAISS as well. First, I added product_name to my Final_cleaned_data dataset, since I believe it is a good feature to find similarity between products and the brief product description that it contains on every product is also useful while differentiating products. To implement the algorithm I had to do a couple of different things in order to be able to find similar products. I first had to use NLTK for cleaning up the product_name column and also remove whitespaces and hyperlinks. Next, I needed to convert the product_name column into embeddings, which would then be stored in a vector database, pinecone in this instance. I used the steps in the hugging face course for this(linked below). The query for a find_similar_products would then go into this vector database, using the pinecone API, in order to find num_similar number of similar products. This way, once we create a vector database initially, we avoid doing the same computation over and over again for different queries, which would, in turn, reduce the processing time for a query significantly. After creating the vector database of embeddings of the product_name column, everytime we need to find similiar products to a given unique_id, the FAISS algorithm would then compare the embedding of that unique_id with the embeddings of the other unique_ids to find the most similar products.
Alternatively, I also explored the possibility of using Target Encoding for my 'brand' column which seemed like it would solve the dimensionality curse but once implemented it did not seem to have the same accuracy as the initial model with one hot encoding. For my research on FAISS and word embeddings I mainly used google and hugging face and I will link them to this readme file as well. I will upload my jupyter notebook file in which I implemented the FAISS algorithm as well.

Resource 1: https://manangarg.medium.com/implementing-faiss-vector-similarity-search-for-recommendations-faa5149f55de
Resource 2: https://huggingface.co/learn/nlp-course/chapter5/6?fw=tf

# Steps to run the Docker image from docker hub on your local laptop correctly

Once I pushed my docker image to docker hub I tried pulling the image and running it on a separate device and I ran into a couple of errors which is why I am writing this section on how to correctly pull the image and run the right commands in order for it to work successfully on your local device.

First, pull the image from the docker hub url provided with the following command:
'''docker pull arvindveerelli/similarity-search-application-ui
'''
Next, once you have the docker image on you device run this command in order to run both the starlit and FastAPI application on the right ports:
'''docker run -p 8000:8000 -p 8501:8501 arvindveerelli/similarity-search-application-ui:latest
'''
Running this command seems to solve the issue where docker randomly assigns the wrong port to the application which internally are expecting to be ran on different ports.

# Steps to run the application locally

I will put the terminal commands that are required to run the entire application on the right ports in order to prevent any errors that might arise. First run this command in the terminal to start the uvicorn application on the right port:
'''uvicorn app:app --reload --host 127.0.0.1 --port 8000
'''
Next, run this command to run the streamlit application on the right port:
'''streamlit run streamlit_app.py --server.port 8501 --server.address 127.0.0.1
'''
