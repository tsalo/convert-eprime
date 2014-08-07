Convert_eprime
==============

Python code meant to convert eprime files to csvs for analysis. In progress.

index_eprime_files.py: Basically looks through a folder and finds pairs of edat/txt files (successful runs) and all other combinations of files. It notes these other files as requiring individual attention. Eventually it will call convert_epr_txt_to_red_csv so that you can automatically convert the text files in pairs.

pickle_files.py: Writes out pickle file with a number of dictionaries used by convert_epr_txt_to_red_csv.py. All of your task-specific information goes here.

convert_epr_txt_to_red_csv.py: Does the conversion. Buggy, and currently a script, but I’m working on it. 


Current procedure for eprime conversion scripts.
1. Using whatever scripts you use to create your vectors, identify necessary columns in the edat file.
2. Add your task to headers (with your edat headers), merge_cols (empty list), merge_col_names (empty list), null_cols (any column), and replace_dict (copy from another task) in pickle_files.
3. Run convert_epr_txt_to_red_csv. It will fail, but will output WHOLE_TEXT_FILE first. I will probably end up splitting this portion of the code into its own function, so that you can do this without the script failing.
4. Look through WHOLE_TEXT_FILE and compare with edat.
a. There will be some columns with different names that contain the same information (replace_dict).
i. You might also come across a column in the text file that has the same name as an important column in the edat, but with different information. You can rename that column to something else using replace_dict, so that you’re essentially switching out a bad header with a good one (assuming you’ve found the differently-named but corresponding text file header for that edat header).
b. There will also be some columns that have NULLs right where you need them (on the rows you want to remove), so use one of those for null_cols. You can use more than one if no one of them covers everything.
c. There may also be columns in the edat that correspond to multiple columns in WHOLE_TEXT_FILE. For example, one column in the text file might correspond to block 1, with another corresponding to block 2, while in the edat they’re just one column. You can add those columns as lists to merge_cols, with the name of the edat column in the corresponding position in merge_col_names. 
5. Test it out. Yes, I know this procedure is tedious, but now it should work with your task. 

