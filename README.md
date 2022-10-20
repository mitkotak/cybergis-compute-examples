# CyberGIS-Compute Examples

This guide walks through how to create a CyberGIS-Compute model for:

1. A Jupyter notebook
2. A Python script
3. A bash script

We also walk through examples of how to retrieve data from CyberGIS-Compute, pass parameters, and upload data.

<hr id="toc" />

# Table of Contents

* [Getting Started](#get-started)
* [Example 1 - Jupyter Notebook](#ex1)
* [Example 2 - Python Script](#ex2)
* [Example 3 - Bash script](#ex3)
* [Create a Manifest](#manifest)
* [Run the Model!](#run)
* [See Also](#see-also)

<hr id="get-started" />

# Getting Started

First, we need to create an account on a JupyterHub with access to CyberGIS-Compute (i.e. [CyberGISX](https://cybergisxhub.cigi.illinois.edu/)). 

Once you have an account and can use the JupyterHub, you are going to want to clone this repository onto the JupyterHub. On CyberGISX the steps would be:

1. Go to a "Launcher" (to open one, click the blue plus mark in the top-left on JupyterLab).
2. Under "Other" click "Terminal".
3. Change directories to your work folder (`cd work`)
4. Clone this repository (`git clone git@github.com:alexandermichels/cybergis-compute-examples.git`)
5. Switch to the `start` branch which give you the necessary files for this tutorial.

Keep this terminal open as we will use it throughout the guide!

<hr id="ex1" />

# Example 1 - Jupyter Notebook

This part walks you through converting a simple Jupyter notebook to a Python script that we can run through CyberGIS-Compute.

1. In the file browser, navigate to the folder of this Github repository on the JupyterHub and then go into the "example1" folder.
2. Open [example1/example1.ipynb](example1/example1.ipynb) and run the notebook.
3. Convert the notebook to a script with the following steps:
    1. In the terminal, navigate to the "example1" directory with the notebook (`cd example1`).
    2. Run the command `jupyter nbconvert example1.ipynb --to script` to convert the notebook to a script.
4. Test that the script runs by running it with `python example1.py`

Awesome, we have converted a simple Jupyter notebook to a Python script. We will go through two other examples and then add all three examples to a single CyberGIS-Compute model.

<hr id="ex2" />

# Example 2 - Python Script

In this example, we will learn how to deal with input and output data! Our example will allow users to upload geojson files and create simple maps of them.

1. In the file browser, navigate to the "example2" folder. 
2. Open the file "make_maps.py" to see what it does.
3. In the terminal, navigate back to the root directory of this repo (`cd ../`).
4. Just to make sure we can run the script here, run the command `pip install geopandas` to install the Python geopandas package.
5. Now, run the example 2 script with `python3 example2/make_maps.py`
6. In the file browser, go back to the root directory of this repo and you should find a "mymaps" folder with two maps in there.
7. In CyberGIS-Compute, if you want to retrieve data back from the HPC the data must go into a folder specified by the environmental variable `result_folder`. Let's change the script to use this folder.
    1. Open "make_maps.py" again.
    2. Change the line `output_path = "mymaps/"` to `output_path = os.getenv('result_folder')`.
8. We also want users to be able to upload the geojson files. In CyberGIS-Compute, uploaded data goes into a folder specified by the environment variable `data_folder`. Let's change to script to use this folder.
    1. Open "make_maps.py".
    2. Change the line `geojson_dir = "data/"` to `geojson_dir = os.getenv('data_folder')`.
9. Let's test this new configuration quickly! Try running the script with the environmental variables specified:

```
export data_folder="data" && export result_folder="mymaps" && python3 example2/make_maps.py
```

<hr id="ex3" />

# Example 3 - Bash Script

For this example, we will create a bash script that can say your name! This will utilize CyberGIS-Compute's ability of end-users to pass parameters into an existing model.

1. In the file browser, navigate to the "example3" folder. 
2. Open the file "say_my_name.sh" to see what it does.
3. In the terminal, let's run the script with `bash example3/say_my_name.sh`. You should see it print out "Your name is Alex"
4. Well your name probably isn't "Alex", so let's change it to use a parameter. In CyberGIS-Compute parameters are made available to the running job as environmental variables with the prefix "param_". So a parameter "name" would be the environmental variable "param_name". 
5. Let's change the script to use the "param_name" environmental variable. In "say_my_name.sh":
    1. Delete the first line (`NAME="Alex"`).
    2. Change the line `echo "Your name is ${NAME}"` to `echo "Your name is ${param_name}"`.
6. Let's test the new script by running in the terminal:

```
export param_name="Anand" && bash example3/say_my_name.sh
```

In the command above, replace the name (Anand) with whatever your name is.

Now that we have all three examples CyberGIS-Compute ready, let's make a manifest so that we can run it!



<hr id="manifest" />

# Create a Manifest

A manifest provides information on how the model can be run with CyberGIS-Compute. Let's create one to run our model.


1. In the file browser, navigate to the root directory of this repo, create a text file there, and rename it "manifest.json". 
2. Copy/paste the following in the file:

```
{
    "name": "three-examples",
    "description": "Runs three simple examples",
    "estimated_runtime": "5 minutes",
    "container": "cybergisx-0.4",
    "pre_processing_stage": "python example1/example1.py",
    "execution_stage": "python example2/make_maps.py",
    "post_processing_stage": "bash example3/say_my_name.sh",
    "slurm_input_rules": {
           "time": {
                "max": 10,
                "min": 5,
                "default_value": 10,
                "step": 1,
                "unit": "Minutes"   
            },
            "memory": {
                "max": 4,
                "min": 2,
                "default_value": 4,
                "step": 1,
                "unit": "GB"
            }
    },
    "require_upload_data": true,
    "param_rules": {
        "name": {
            "type": "string_input",
            "require": true,
            "default_value": "Your Name Here"
        }
    }
}
```

Let's break this file down:
* The first few lines provide metadata information to the end-user of the model:
```
    "name": "three-examples",
    "description": "Runs three simple examples",
    "estimated_runtime": "5 minutes",
```
* The next line specifies the container that should be used. This is our default geospatial python container. `"container": "cybergisx-0.4",`
* The following lines specify the steps of our model, running our examples (from the root of the repo) in order:
```
    "pre_processing_stage": "python example1/example1.py",
    "execution_stage": "python example2/make_maps.py",
    "post_processing_stage": "bash example3/say_my_name.sh",
```
* Next, we provide information to the SLURM job scheduler about the maximum amount of time and memory our model requires. We see both low so we don't take up too many resources, although it's possible that a user could upload many large GeoJSONs:
```
    "slurm_input_rules": {
           "time": {
                "max": 10,
                "min": 5,
                "default_value": 10,
                "step": 1,
                "unit": "Minutes"   
            },
            "memory": {
                "max": 4,
                "min": 2,
                "default_value": 4,
                "step": 1,
                "unit": "GB"
            }
    },
```
* To ensure that our user uploads some data, we use the line `"require_upload_data": true,`.
* Lastly, we define a parameter "name" and tell the GUI that it should be a required string input with a default value of "Your Name Here":
```
    "param_rules": {
        "name": {
            "type": "string_input",
            "require": true,
            "default_value": "Your Name Here"
        }
    }
```



<hr id="run" />

# Run the Model!

To run the model, you can use the notebook in the main branch called "RunExamples.ipynb"



<hr id="see-also">

# See Also

### Guides and Helpful Materials

* [Developing a Model with CyberGIS-Compute](https://cybergis.github.io/cybergis-compute-python-sdk/model_contribution/)