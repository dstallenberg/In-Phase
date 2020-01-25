from setuptools import setup

def get_long_description():
    """ Extract the long description from the README file """

    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

    return long_description

setup(
    name='quantum_phase_estimation',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    version='1.0',
    packages=['quantum_phase_estimation', 'qasm_topology_mapper', 'qasm_to_projectq', 'qasm_optimizer', 'qasm_error_introducer', 'connecting'],
    url='',
    license='Apache 2.0',
    author='Group7',
    author_email='',
    description='Quantum phase estimation',
    python_requires='>=3.6',
    install_requires=['pytest>=3.3.1', 'matplotlib>=2.1', 'numpy', 'quantuminspire'],
    package_dir={'': 'src'},
    extras_require={'projectq': ["projectq>=0.4"]}
)