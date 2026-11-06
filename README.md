This repository contains incomplete code intended for creating simplified GUI for the ADALM1000, intended for introductory student use. This was intended to be more feature complete than [Pixelpulse2](https://github.com/analogdevicesinc/Pixelpulse2) and less intimidating than [Alice](https://github.com/analogdevicesinc/alice).

# Install

Ensure that python3, pip, and venv are installed. (venv not required if installing packages globally)

Create a virtual environment within this directory:

```
python -m venv env
source /env/bin/activate
```

Install python requirements

```
pip install -r requirements.txt
```

Install `libsmu` and `pysmu`. See here: [libsmu](https://github.com/rpi-mercerxlab/libsmu)

To install the `pysmu` package within the virtual environment, find the `pysmu-*.whl` file and install it with:

```
pip install pysmu-*.whl
```

# Run Basic Demo

Ensure the virtual environment is activated:

```
source /env/bin/activate
```

Run Oscilloscope Demo

```
python adalm1000_osc.py
```
