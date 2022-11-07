Extraction and fine-tuning walls detection part from https://github.com/rbg-research/Floor-Plan-Detection

### Installation
```
pip install -r requirements.txt
```
### Usage example
```
python detect_walls.py example.png --kernel 3 --opening_iter 2 --dilate_iter 2 --approx_accuracy 0.1
```
### Possible improvements
ToDo:
Filter annotations, dimensions in the schemes and to replace doors and windows by implementing ML object detection methods.

Add a module wich implements this logic: 
https://docs.google.com/document/d/1BkJ9XAs2WIIHKXQlAzy7HI8aUoi05192h45TjiueSQs/edit?usp=sharing
