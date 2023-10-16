from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(
    name="fx_analytics",
    version="1.5.6",
    packages=['fx_analytics'],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url= "https://github.com/jaybfn/fx_analytics",
    author = "Jayesh Arun Bafna",
    author_email = "jayesh.bfn@gmail.com",
    license= "MIT",
    extras_require = {"dev":["pytest","twine"],},
    install_requires=['pandas>=2.1.0',
                        'streamlit>=1.26.0',
                        'plotly>=5.16.1',
                        'plotly-express>=0.4.1',
                        'loguru>=0.7.2',
                        'wheel',
                        'pytest'
                        ],
    python_requires=">=3.11"
)
