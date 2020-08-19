# How use

Go through the entire directory and clear JSON data from files/images.
The `files` and `upload` keys that will be removed from JSON DATA:
```
    python3 main.py PATH_TO_SLACK_EXPORT_FOLDER/
```

You can see the whole folder tree. This mode doesn't make it to fix files. It only shows tree's directories and files:
```
    python3 main.py PATH_TO_SLACK_EXPORT_FOLDER/ --tree
```


Example use:
```
python main.py ../channels/demo_sjon2 --tree  
python main.py ../channels/demo_sjon2 
```
