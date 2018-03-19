from setuptools import setup, find_packages

setup(name='requestify',
      version='1.0.0',
      description='convert curl to python requests code',
      author='Yue Minatsuki',
      author_email='yue.official.jp@gmail.com',

      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3.6',
      ],
      url='https://www.python.org/sigs/distutils-sig/',
      license="MIT Licence",
      packages=find_packages(),
      scripts=["main.py","generate.py"],
      install_requires = ["requests"]
     )