Instructions to run the code



## INSTALLATION

1. Download the project ZIP file and extract it to your local machine.
2. Open a terminal or command prompt and navigate to the project directory.
3. Create a virtual environment (optional but recommended)
4. Open the virtual environment
5. Install dependencies using "requirements.txt"



## HOW TO RUN THE PROGRAM

To run the program, place the files "actual{number}.json" and "standard{number}.json"
in the directory "data". Use this format, including a number, or the program
may not run correctly. Examples of valid names for the standard and actual routes
json files are "actual34.json", "standard34.json".

Once the files are in the "data" directory, go to the "main" file and enter only
the actual routes file name as input to the main function at the bottom of the file.
For example, if you want to use the files "actual3.json" and "standard3.json", write

if __name__ == "__main__":
    main(input_filename='actual3.json')

Run the "main" file (it may take some time (5 to 10 minutes) to finish).

The three files

1. recStandard3.json
2. driver3.json
3. perfectRoute3.json

will be written in the directory "results", using the default settings for the parameters.




## CREATING YOUR OWN DATASET

To generate your own dataset, you can use the file "DatasetGeneration" in the
directory "Datasets_Generation", following the steps:

1. Create a configuration file similar to "config_dataset_1.py".
   (For a detailed description of the meaning of the parameters, see the documentation
   of the function "generate_routes" in the file "generate_random_routes.py").
   The variable "dataset_number" in the configuration files corresponds to the number
   appearing in the files standard.json and actual.json that will be generated.
   For example, if you want to create the files actual6.json and standard6.json,
   set dataset_number = 6.

2. Open the file "DatasetGeneration" and modify the command
   "from config_dataset_4 import(...)"
   replacing config_dataset_4 with the correct configuration file name.

3. Run the DatasetGeneration file.