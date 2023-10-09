from setuptools import setup, find_packages

with open('README.md') as f:
    description = f.read()
setup(
    name="fxboard",
    version="0.1",
    description = "A streamlit dashboard which displays all the forex metric from your trading platforms",
    packages=['script'],
    url= "https://github.com/jaybfn/forex_dashboard",
    author = "Jayesh Arun Bafna",
    author_email = "jayesh.bfn@gmail.com",
    license= "MIT",
    install_requires=[
        "streamlit",
        "MetaTrader5",
        "pandas",
        "plotly",
        "plotly-express",
        "loguru"
        # Add other dependencies here
    ],
    extras_require = {"dev":["pytest","twine"],},
    python_requires=">=3.11"
)
