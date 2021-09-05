#!/usr/bin/env python
# coding: utf-8

# # Social Network Analysis on BTS Fandom in Python

# In[1]:


import tweepy
import json
import pandas as pd
from pandas.io.json import json_normalize
import time
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from ipynb.fs.full.Credentials import *


# ## Data Collection

# In[2]:


consumer_key = Twitter_API_KEY 
consumer_secret = Twitter_API_SECRET 
access_token = Twitter_ACCESS_TOKEN 
access_token_secret = Twitter_ACCESS_SECRET 
  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 

api = tweepy.API(auth, wait_on_rate_limit = True) 


# In[3]:


def jsonify_tweepy(tweepy_object):
    json_str = json.dumps(tweepy_object._json)
    return json.loads(json_str)


# In[4]:


def getFollowers_toDF (followers, item_no_t2):

    followers_all = []
    
    for follower in followers:
    
        try:
            users = api.get_user(screen_name = follower)
            follower_ID = users.id_str
            print("The ID of the user " + follower + " is : " + follower_ID)

            followers_obj = tweepy.Cursor(api.followers, screen_name = follower, count = 200).items(item_no_t2)

            time.sleep(60)

            #Call the function and unload each _json into follower_list
            followers_list = [jsonify_tweepy(follower_obj) for follower_obj in followers_obj]

            #Convert followers_list to a pandas dataframe
            followers_df = json_normalize(followers_list)

            if len(followers_df) > 0:

                followers_df_filtered = followers_df[['screen_name']][followers_df['id_str'].notnull() & 
                                                                      (followers_df['friends_count'] <= 50) & 
                                                                      (1 <= followers_df['friends_count']) & 
                                                                      (followers_df['followers_count'] >= 100)]
                followers_df_filtered['Users'] = follower
                followers_df_filtered.rename(columns={'screen_name':'Followers'}, inplace=True)        

                followers_all.append(followers_df_filtered)
        
        except tweepy.error.TweepError:
            continue

    followers_all = pd.concat(followers_all, axis = 0, ignore_index = True, sort = False)

    return followers_all


# In[11]:


def getFriends_toDF (followers, item_no_t2):

    friends_all = []
    
    for follower in followers:
    
        try:
            user = api.get_user(screen_name = follower)
            user_ID = user.id_str
            print("The ID of the user " + follower + " is : " + user_ID)

            friends_obj = tweepy.Cursor(api.friends, screen_name = follower, count = 200).items(item_no_t2)

            time.sleep(60)

            #Call the function and unload each _json into follower_list
            friends_list = [jsonify_tweepy(friend_obj) for friend_obj in friends_obj]

            #Convert followers_list to a pandas dataframe
            friends_df = json_normalize(friends_list)

            if len(friends_df) > 0:

                friends_df_filtered = friends_df[['screen_name']][friends_df['id_str'].notnull() & 
                                                                  (friends_df['friends_count'] >= 1) &
                                                                  (friends_df['friends_count'] <= 150) &
                                                                  (friends_df['followers_count'] >= 100)]
                friends_df_filtered['Followers'] = follower
                friends_df_filtered.rename(columns={'screen_name':'Users'}, inplace=True)        

                friends_all.append(friends_df_filtered)
        
        except tweepy.error.TweepError:
            continue

    friends_all = pd.concat(friends_all, axis = 0, ignore_index = True, sort = False)
    friends_all = friends_all[['Followers', 'Users']]

    return friends_all


# In[6]:


def getFriends_T0_toDF (followers):

    friends_all = []
    
    for follower in followers:
    
        try:
            user = api.get_user(screen_name = follower)
            user_ID = user.id_str
            print("The ID of the user " + follower + " is : " + user_ID)

            friends_obj = tweepy.Cursor(api.friends, screen_name = follower, count = 200).items()

            time.sleep(60)

            #Call the function and unload each _json into follower_list
            friends_list = [jsonify_tweepy(friend_obj) for friend_obj in friends_obj]

            #Convert followers_list to a pandas dataframe
            friends_df = json_normalize(friends_list)

            if len(friends_df) > 0:

                friends_df_filtered = friends_df[['screen_name']][friends_df['id_str'].notnull() & 
                                                                  (friends_df['friends_count'] >= 1)]
                friends_df_filtered['Followers'] = follower
                friends_df_filtered.rename(columns={'screen_name':'Users'}, inplace=True)        

                friends_all.append(friends_df_filtered)
        
        except tweepy.error.TweepError:
            continue

    friends_all = pd.concat(friends_all, axis = 0, ignore_index = True, sort = False)
    friends_all = friends_all[['Followers', 'Users']]

    return friends_all


# In[7]:


screen_name = 'BTS_twt'


# In[16]:


T0_Fr1 = getFriends_T0_toDF([screen_name])


# In[17]:


T0_Fr1


# In[8]:


T1 = getFollowers_toDF([screen_name], 10000)


# In[9]:


T1


# In[12]:


T1_Fr1 = getFriends_toDF(list(T1['Followers']), 50)


# In[13]:


T1_Fr1


# In[14]:


len(list(T1_Fr1['Users'].unique()))


# In[ ]:


T1_Fr2 = getFriends_toDF(list(T1_Fr1['Users'].unique()), 50)


# In[ ]:


T1_Fr2


# In[ ]:


list(T1_Fr1['Users'].unique())


# In[18]:


T2 = getFollowers_toDF(list(T1['Followers']), 1000)


# In[19]:


T2


# In[20]:


T2_Fr1 = getFriends_toDF(list(T2['Followers'].unique()), 50)


# In[21]:


T2_Fr1


# In[ ]:


T2_Fr2 = getFriends_toDF(list(T2_Fr1['Users'].unique()), 50)


# In[ ]:


T2_Fr2


# In[22]:


DF = pd.concat([T0_Fr1, T1, T1_Fr1, T2, T2_Fr1]).drop_duplicates().reset_index(drop=True)


# In[23]:


DF


# ## Exploratory Data Analysis

# In[24]:


print(DF['Followers'].value_counts())


# In[ ]:


print(dict(DF['Followers'].value_counts()))


# In[25]:


print(DF['Users'].value_counts())


# In[ ]:


print(dict(DF['Users'].value_counts()))


# ## Data Visualization

# In[46]:


graph = nx.from_pandas_edgelist(DF, 'Followers', 'Users', 
                            edge_attr = None, create_using = nx.DiGraph())


# In[47]:


print(nx.info(graph))


# In[48]:


'{:.15f}'.format(nx.average_clustering(graph))


# In[149]:


dict(sorted(nx.in_degree_centrality(graph).items(), key=lambda item: item[1], reverse=True))


# In[59]:


dict(sorted(nx.eigenvector_centrality(graph).items(), key=lambda item: item[1], reverse=True))


# In[56]:


dict(filter(lambda value: value[1] > 0, dict(sorted(nx.betweenness_centrality(graph, 
                                                                     normalized = True, 
                                                                     endpoints = True).items(), key=lambda item: item[1], 
                                                    reverse=True)).items()))


# In[147]:


plt.figure(figsize =(20, 20))

layout = nx.spring_layout(graph,
                          k = 0.7)
nx.draw_networkx_edges(graph, 
                       layout, 
                       edge_color = '#AAAAAA')

uni_dots = [node for node in graph.nodes() 
            if node in np.unique(DF[['Users', 'Followers']].values)]
nx.draw_networkx_nodes(graph, 
                       layout, 
                       nodelist = uni_dots, 
                       node_size = 30, 
                       node_color = '#AAAAAA')

eig_dict = dict(filter(lambda value: value[1] > 0.03, 
                           dict(sorted(nx.eigenvector_centrality(graph).items(), 
                                       key=lambda item: item[1], 
                                       reverse=True)).items()))

inde_dict = dict(filter(lambda value: value[1] > 0.005, 
                           dict(sorted(nx.in_degree_centrality(graph).items(), 
                                       key=lambda item: item[1], 
                                       reverse=True)).items()))

btn_dict = dict(filter(lambda value: value[1] > 0.0005, 
                               dict(sorted(nx.betweenness_centrality(graph, 
                                                                     normalized = True, 
                                                                     endpoints = True).items(), 
                                           key=lambda item: item[1], 
                                           reverse=True)).items()))

intersection =  [node for node in graph.nodes() 
                 if node in eig_dict.keys()
                 if node in inde_dict.keys() 
                 if node in btn_dict.keys()]

size_intersection = [value * 1000000 for (node, value) in nx.in_degree_centrality(graph).items() 
                     if node in intersection]
nx.draw_networkx_nodes(graph, 
                       layout, 
                       nodelist = intersection, 
                       node_size = size_intersection, 
                       node_color = 'purple', 
                       alpha = 0.3)
nx.draw_networkx_labels(graph, 
                        layout, 
                        labels = dict(zip(list(intersection), list(intersection))),
                        font_size = 16)

inde_btn = [node for node in graph.nodes()
           if node not in eig_dict.keys()
           if node in inde_dict.keys()
           if node in btn_dict.keys()]
size_inde_btn = [value * 1000000 for (node, value) in nx.in_degree_centrality(graph).items() 
               if node in inde_btn]
nx.draw_networkx_nodes(graph, 
                       layout, 
                       nodelist = inde_btn, 
                       node_size = size_inde_btn, 
                       node_color = 'aqua', 
                       alpha = 0.3)
nx.draw_networkx_labels(graph, 
                        layout, 
                        labels = dict(zip(list(inde_btn), list(inde_btn))),
                        font_size = 16)

eig_inde = [node for node in graph.nodes()
           if node in eig_dict.keys()
           if node in inde_dict.keys()
           if node not in btn_dict.keys()]
size_eig_inde = [value * 1000000 for (node, value) in nx.in_degree_centrality(graph).items() 
               if node in eig_inde]
nx.draw_networkx_nodes(graph, 
                       layout, 
                       nodelist = eig_inde, 
                       node_size = size_eig_inde, 
                       node_color = 'yellow', 
                       alpha = 0.3)
nx.draw_networkx_labels(graph, 
                        layout, 
                        labels = dict(zip(list(eig_inde), list(eig_inde))),
                        font_size = 16)

eig_btn = [node for node in graph.nodes()
           if node in eig_dict.keys()
           if node not in inde_dict.keys()
           if node in btn_dict.keys()]
size_eig_btn = [value * 1000000 for (node, value) in nx.in_degree_centrality(graph).items() 
               if node in eig_btn]
nx.draw_networkx_nodes(graph, 
                       layout, 
                       nodelist = eig_btn, 
                       node_size = size_eig_btn, 
                       node_color = 'orange', 
                       alpha = 0.4)
nx.draw_networkx_labels(graph, 
                        layout, 
                        labels = dict(zip(list(eig_btn), list(eig_btn))),
                        font_size = 16)

plt.axis('off')
plt.title("The Popular Accounts in BTS Fandom")
#based on eigenvector_centrality, in-degree centrality & betweenness centrality
plt.show()

