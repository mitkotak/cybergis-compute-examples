#!/usr/bin/env python
# coding: utf-8

# In[1]:


print(f"Hello from example 1!")


# In[2]:


def fibonacci(n):
    """Prints the first n elements of the fibonacci sequence"""
    a, b = 0, 1
    for i in range(n):
        print(a)
        c = a + b
        a = b
        b = c


# In[3]:


fibonacci(30)


# In[ ]:




