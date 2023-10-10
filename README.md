# Kannada-Handwriting-Calculator

A calculator that uses handwritten digits and operators to calculate the result, using contour detection and CNN model prediction.</br>
***Tensorflow (Keras)*** is used to create, train and load the neural network model used for predictions.</br>
***CustomTKinter*** is used to provide the GUI.</br>
***OpenCV*** and ***Pillow (PIL)*** are used to read input from the GUI canvas and to obtain contours for individual digits/operators.</br>
The individual digits/operators are detected and predicted. The predictions are combined into a string and evaluated to get the result.



## Requirements -
```bash
pip install -r requirements.txt
```
* Tensorflow (Keras)
* OpenCV
* Pillow (PIL)
* Pandas
* Numpy
* CustomTkinter

## Instructions -
* Clone the repo and run the Jupyter notebook, **MAIN.ipynb** or run **MAIN.py**
* You can use Kannada digits `೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯`, operators `+ - × /`, decimal point `.` and parentheses `()`
* You can also use `××` for exponentiation and `//` for floor division

### Data
* [Kannada MNIST dataset](https://www.kaggle.com/competitions/Kannada-MNIST/data)
* [Symbol dateset by Irfan Chahyadi ](https://github.com/irfanchahyadi/Handwriting-Calculator/blob/master/src/dataset/data.pickle)
