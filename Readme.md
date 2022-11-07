Extraction and fine-tuning walls detection part from https://github.com/rbg-research/Floor-Plan-Detection

### Installation
```
pip install -r requirements.txt
```
### Usage example
```
python detect_walls.py example.png --kernel 3 --opening_iter 2 --dilate_iter 2 --approx_accuracy 0.1
```
