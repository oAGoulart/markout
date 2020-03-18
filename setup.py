from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='markout_html',
  version='0.1.4',
  description='A tool to extract HTML contents',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/oAGoulart/markout',
  author='Augusto Goulart',
  author_email='josegoulart.aluno@unipampa.edu.br',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Text Processing :: Markup :: HTML',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
  keywords='html conversion markup',
  package_dir={'': 'src'},
  packages=find_packages(where='src'),
  python_requires='>=3.5',
  install_requires=['pyquery>=1.3'],
  entry_points={
    'console_scripts': [
      'markout_html=markout_html:main',
    ],
  },
  project_urls={
    'Bug Reports': 'https://github.com/oAGoulart/markout/issues',
    'Source': 'https://github.com/oAGoulart/markout',
  },
)
