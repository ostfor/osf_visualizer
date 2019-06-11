from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='osf_visualizer',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      install_requires=required,
      description='Open visualization tools for training process',
      url='http://github.com/ostfor/open_mlstat',
      author='Denis Brailovsky',
      author_email='denis.brailovsky@gmail.com',
      license='MIT',
      data_files=[('', ['LICENSE', 'CHANGELOG.md'])],
      packages=["osf_visualizer.{}".format(pkg) for pkg in find_packages("osf_visualizer")] + ["osf_visualizer"],
      zip_safe=False)
