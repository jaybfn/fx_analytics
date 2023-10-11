from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()
setup(
    name="fx_analytics",
    version="1.3.2",
    description = "A streamlit dashboard which displays all the forex metric from your trading platforms",
    packages=['fx_analytics'],
    long_description = long_description,
    long_description_content_type = "text/markdown",
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
