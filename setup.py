from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pprobs',
  version='0.0.1',
  description='a library for probability computation',
  long_description=open('README.txt').read(),
  url='',  
  author='Mohamadreza Kariminejad',
  author_email='mokar2001@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['scipy', 'numpy', 'pandas'] 
)