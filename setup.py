from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(  
  name = 'MashUp-Bisman-102017051',
  packages = ['mashup'],
  version = '1.0.0',
  license='MIT',
  description = 'MashUp of Youtube Songs of your Favourite Streamer',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Bisman Kaur',
  author_email = 'k.bisman16@gmail.com',
  url = 'https://github.com/BKaur20/MashUp_Python_App.git',
  download_url = 'https://github.com/BKaur20/MashUp_Python_App/archive/refs/heads/main.zip',
  keywords = ['python', 'pypi', 'csv', 'xlsx', 'xls', 'cli'],
  install_requires=[
          'numpy',
          'pandas',
      ],
  entry_points={
    'console_scripts': [
      'mashup = mashup.mashup:main'
      ]
  },
)
