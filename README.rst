pl-pfdo_mgz2img
================================

.. image:: https://badge.fury.io/py/pfdo_mgz2img.svg
    :target: https://badge.fury.io/py/pfdo_mgz2img

.. image:: https://travis-ci.org/FNNDSC/pfdo_mgz2img.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdo_mgz2img

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-pfdo_mgz2img

.. contents:: Table of Contents


Abstract
--------

`pl-pfdo_mgz2img` is a ChRIS plugin that can recursively 
walk down a directory tree and perform a 'mgz2imgslices'
on files in each directory. (optionally filtered by some simple
expression). Results of each operation are saved in output tree
that  preserves the input directory structure.


Synopsis
--------

.. code::

    python pfdo_mgz2img.py                  \
            [-i|--inputFile <inputFile>]                                \
            [--filterExpression <someFilter>]                           \
            [--analyzeFileIndex <someIndex>]                            \
            [--outputLeafDir <outputLeafDirFormat>]                     \
            [-o|--outputFileStem]<outputFileStem>]                      \
            [-t|--outputFileType <outputFileType>]                      \
            [--saveImages]                                              \
            [--label <prefixForLabelDirectories>]                       \
            [-n|--normalize]                                            \
            [-l|--lookupTable <LUTfile>]                                \
            [--skipAllLabels]                                           \
            [-s|--skipLabelValueList <ListOfVoxelValuesToSkip>]         \
            [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]    \
            [-w|--wholeVolume <wholeVolDirName>]                        \
            [--threads <numThreads>]                                    \
            [--test]                                                    \
            [-x|--man]                                                  \
            [-y|--synopsis]                                             \
            [--followLinks]                                             \
            [--json]                                                    \
            <inputDir>                                                  \   
            <outputDir> 


Arguments
---------

.. code::

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

        [-f|--filterExpression <someFilter>]
        An optional string to filter the files of interest from the
        <inputDir> tree.

        [--analyzeFileIndex <someIndex>]
        An optional string to control which file(s) in a specific directory
        to which the analysis is applied. The default is "-1" which implies
        *ALL* files in a given directory. Other valid <someIndex> are:
            'm':   only the "middle" file in the returned file list
            "f":   only the first file in the returned file list
            "l":   only the last file in the returned file list
            "<N>": the file at index N in the file list. If this index
                   is out of bounds, no analysis is performed.
            "-1" means all files.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as
        'anon' or 'preview'.

        This is a formatting spec, so

            --outputLeafDir 'preview-%%s'

        where %%s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store image conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

        [--saveImages]
        If specified as True(boolean), will save the slices of the mgz file as 
        ".png" image files along with the numpy files.

        [--label <prefixForLabelDirectories>]
        Prefixes the string <prefixForLabelDirectories> to each filtered
        directory name. This is mostly for possible downstream processing,
        allowing a subsequent operation to easily determine which of the output
        directories correspond to labels.

        [-n|--normalize]
        If specified as True(boolean), will normalize the output image pixel values to
        0 and 1, otherwise pixel image values will retain the value in
        the original input volume.

        [-l|--lookupTable <LUTfile>]
        Need to pass a <LUTfile> (eg. FreeSurferColorLUT.txt)
        to perform a looktup on the filtered voxel label values
        according to the contents of the <LUTfile>. This <LUTfile> should
        conform to the FreeSurfer lookup table format (documented elsewhere).

        Note that the special <LUTfile> string ``__val__`` can be passed only when 
        running the docker image (fnndsc/pl-mgz2imageslices) of this utility which
        effectively means "no <LUTfile>". In this case, the numerical voxel
        values are used for output directory names. This special string is
        really only useful for scripted cases of running this application when
        modifying the CLI is more complex than simply setting the <LUTfile> to
        ``__val__``.

        While running the docker image, you can also pass ``__fs__`` which will use
        the FreeSurferColorLUT.txt from within the docker container to perform a 
        looktup on the filtered voxel label values according to the contents of 
        the FreeSurferColorLUT.txt

        [--skipAllLabels]
        Skips all labels and converts only the whole mgz volume to png/jpg images.

        [-s|--skipLabelValueList <ListOfLabelNumbersToSkip>]
        If specified as a comma separated string of label numbers,
        will not create directories of those label numbers.

        [-f|--filterLabelValues <ListOfVoxelValuesToInclude>]
        The logical inverse of the [skipLabelValueList] flag. If specified,
        only filter the comma separated list of passed voxel values from the
        input volume.

        The detault value of "-1" implies all voxel values should be filtered.

        [-w|--wholeVolume <wholeVolDirName>]
        If specified, creates a diretory called <wholeVolDirName> (within the
        outputdir) containing PNG/JPG images files of the entire input.

        This effectively really creates a PNG/JPG conversion of the input
        mgz file.

        Values in the image files will be the same as the original voxel
        values in the ``mgz``, unless the [--normalize] flag is specified
        in which case this creates a single-value mask of the input image.

        [--threads <numThreads>]
        If specified, break the innermost analysis loop into <numThreads>
        threads.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--json]
        If specified, output a JSON dump of final return.

        [--followLinks]
        If specified, follow symbolic links.

        --verbose <level>
        Set the app verbosity level.

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write


Run
===

While ``pl-pfdo_mgz2img`` is meant to be run as a containerized docker image, typically within ChRIS, it is quite possible to run the dockerized plugin directly from the command line as well. The following instructions are meant to be a psuedo- ``jupyter-notebook`` inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now we need to fetch MGZ files.

Pull MGZ data
~~~~~~~~~~~~~

- We provide a sample directory of a few ``.mgz`` volumes here. (https://github.com/FNNDSC/mgz_converter_dataset.git)

- Clone this repository (``mgz_converter_dataset``) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/mgz_converter_dataset.git

Make sure the ``mgz_converter_dataset`` directory is placed in the devel directory.

Run using ``docker run``
^^^^^^^^^^^^^^^^^^^^^^^^^^

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

- Make sure your current working directory is ``devel``. At this juncture it should contain ``mgz_converter_dataset``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

- Pull the ``fnndsc/pl-pfdo_mgz2img`` image using the following command.

.. code:: bash

    docker pull fnndsc/pl-pfdo_mgz2img


Examples
--------

Copy and modify the different commands below as needed:

.. code:: bash

    docker run --rm             \
        -v ${DEVEL}/:/incoming                          \
        -v ${DEVEL}/results/:/outgoing                  \
        fnndsc/pl-pfdo_med2img pfdo_med2img.py          \
        --filterExpression aparc.a2009s+aseg.mgz        \                          \
        --analyzeFileIndex -1                           \
        --saveImages                                    \
        --filterLabelValueList 10,15                    \
        --lookupTable __val__                           \ 
        --threads 0                                     \
        --printElapsedTime                              \
        --verbose 5                                     \
        /incoming /outgoing

The above command uses the argument ``--filterExpression`` to filter the ``.mgz`` files from the ${DEVEL} directory.
It replicates the structure of the ``inputdir`` into the ``outputdir`` (in this case: ``results`` directory) then converts all those MGZ files to png files within  
the outputdir.

The following is an example that converts all the raw mgz files (in this case ``brain.mgz``) files to png/jpg images in the desired outputdir.
These raw mgz files do not require the "FreeSurferColorLUT.txt" to convert to images. Therefore we pass __none__ to the --lookupTable argument.

**NOTE:** Make sure you clear the ``results`` directory before running the following command.

.. code:: bash

    docker run --rm             \
        -v ${DEVEL}/mgz_converter_dataset/:/incoming    \
        -v ${DEVEL}/results/:/outgoing                  \
        fnndsc/pl-pfdo_mgz2img pfdo_mgz2img.py          \
        --filterExpression brain.mgz                    \
        --analyzeFileIndex -1                           \ 
        --saveImages                                    \
        --skipAllLabels                                 \
        --lookupTable __none__                          \
        --threads 0                                     \
        --printElapsedTime                              \
        --verbose 5                                     \
        /incoming /outgoing
