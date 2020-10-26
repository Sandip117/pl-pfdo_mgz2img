#!/usr/bin/env python                                            
#
# pfdo_mgz2img ds ChRIS plugin app
#
# (c) 2016-2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import importlib.metadata
import pudb

# Turn off all logging for modules in this libary.
import logging
logging.disable(logging.CRITICAL)

from chrisapp.base import ChrisApp
from pfdo_mgz2image import pfdo_mgz2image

Gstr_title = """

        __    _                             _____ _                 
       / _|  | |                           / __  (_)                
 _ __ | |_ __| | ___   _ __ ___   __ _ ____`' / /'_ _ __ ___   __ _ 
| '_ \|  _/ _` |/ _ \ | '_ ` _ \ / _` |_  /  / / | | '_ ` _ \ / _` |
| |_) | || (_| | (_) || | | | | | (_| |/ / ./ /__| | | | | | | (_| |
| .__/|_| \__,_|\___/ |_| |_| |_|\__, /___|\_____/_|_| |_| |_|\__, |
| |               ______          __/ |                        __/ |
|_|              |______|        |___/                        |___/ 

"""

Gstr_synopsis = """

    NAME

       pfdo_mgz2img.py 

    SYNOPSIS

        python pfdo_mgz2img.py                                         \\
            -I|--inputDir <inputDir>                                   \\
            -O|--outputDir <outputDir>                                 \\
            [-i|--inputFile <inputFile>]                                \\
            [--filterExpression <someFilter>]                           \\
            [--outputLeafDir <outputLeafDirFormat>]                     \\
            [-o|--outputFileStem]<outputFileStem>]                      \\
            [-t|--outputFileType <outputFileType>]                      \\
            [--saveImages]                                              \\
            [--label <prefixForLabelDirectories>]                       \\
            [-n|--normalize]                                            \\
            [-l|--lookupTable <LUTfile>]                                \\
            [-s|--skipLabelValueList <ListOfVoxelValuesToSkip>]         \\
            [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]    \\
            [-w|--wholeVolume <wholeVolDirName>]                        \\
            [--threads <numThreads>]                                    \\
            [--test]                                                    \\
            [-x|--man]                                                  \\
            [-y|--synopsis]                                             \\
            [--followLinks]                                             \\
            [--json]                                                    \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python pfdo_mgz2img.py   \\
                                in    out

    EXAMPLE

        Perform a `pfdo_mgz2image` down some input directory:

        pfdo_mgz2image                                      \\
            -I /var/www/html/data --filter nii              \\
            -O /var/www/html/jpg                            \\
            -t jpg                                          \\
            --threads 0 --printElapsedTime

        The above will find all files in the tree structure rooted at
        /var/www/html/data that also contain the string "nii" anywhere
        in the filename. For each file found, a `mgz2image` conversion
        will be called in the output directory, in the same tree location as
        the original input.

        Finally the elapsed time and a JSON output are printed.



    DESCRIPTION

        `pfdo_mgz2img.py` runs ``mgz2image`` at each path/file location in an
        input tree. The CLI space is the union of ``pfdo`` and ``mgz2image``.

    ARGS

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

        [-f|--filterExpression <someFilter>]
        An optional string to filter the files of interest from the
        <inputDir> tree.

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

        -v|--verbosity <level>
        Set the app verbosity level.

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write


"""

class Pfdo_mgz2img(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'FNNDSC <dev@babyMRI.org>'
    SELFPATH                = '/usr/local/bin'
    SELFEXEC                = 'pfdo_mgz2img'
    EXECSHELL               = 'python'
    TITLE                   = 'A ChRIS plugin app to run the Python utility: pfdo_mgz2image'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to run the Python utility: pfdo_mgz2image'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = importlib.metadata.version(__package__)
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument("-i", "--inputFile",
                            help    = "input file",
                            dest    = 'inputFile',
                            type    = str,
                            optional= True,
                            default = '')
        self.add_argument("--filterExpression",
                            help    = "string file filter",
                            dest    = 'filter',
                            type    = str,
                            optional= True,
                            default = '')
        # self.add_argument("-O", "--outputDir",
        #                     help    = "output image directory",
        #                     dest    = 'outputDir',
        #                     type    = str,
        #                     optional= False,
        #                     default = '')
        self.add_argument("--printElapsedTime",
                            help    = "print program run time",
                            dest    = 'printElapsedTime',
                            action  = 'store_true',
                            type    = bool,  
                            optional= True,   
                            default = False)
        self.add_argument("--threads",
                            help    = "number of threads for innermost loop processing",
                            dest    = 'threads',
                            type    = str,
                            optional= True,
                            default = "0")
        self.add_argument("--outputLeafDir",
                            help    = "formatting spec for output leaf directory",
                            dest    = 'outputLeafDir',
                            type    = str,
                            optional= True,
                            default = "")
        self.add_argument("--test",
                            help    = "test",
                            dest    = 'test',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument("-y", "--synopsis",
                            help    = "short synopsis",
                            dest    = 'synopsis',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument("--overwrite",
                            help    = "overwrite files if already existing",
                            dest    = 'overwrite',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument("--followLinks",
                            help    = "follow symbolic links",
                            dest    = 'followLinks',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
                            
        # mgz2image additional CLI flags

        self.add_argument("-o", "--outputFileStem",
                            help    = "output file",
                            default = "output.jpg",
                            type    = str,
                            optional= True,
                            dest    = 'outputFileStem')
        self.add_argument("-t", "--outputFileType",
                            help    = "output image type",
                            dest    = 'outputFileType',
                            type    = str,
                            optional= True,
                            default = '')
        self.add_argument('--saveImages',
                            help='store png images for each slice of mgz file',
                            dest='saveImages',
                            action= 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)                    
        self.add_argument('--label',
                            help='prefix a label to all the label directories',
                            dest='label',
                            type    = str,
                            optional= True,
                            default = 'label')
        self.add_argument('-n', '--normalize',
                            help='normalize the pixels of output image files',
                            dest='normalize',
                            type    = bool,
                            optional= True,
                            action= 'store_true',
                            default = False)
        self.add_argument('-l', '--lookupTable',
                            help='file contain text string lookups for voxel values',
                            dest='lookupTable',
                            type    = str,
                            optional= True,
                            default = '__val__')
        self.add_argument('-s', '--skipLabelValueList',
                            help='Comma separated list of voxel values to skip',
                            dest='skipLabelValueList',
                            type    = str,
                            optional= True,
                            default = '')
        self.add_argument('-f', '--filterLabelValueList',
                            help='Comma separated list of voxel values to include',
                            dest='filterLabelValueList',
                            type    = str,
                            optional= True,
                            default = "-1")
        self.add_argument('-w', '--wholeVolume',
                            help='Converts entire mgz volume to png/jpg instead of individually masked labels',
                            dest='wholeVolume',
                            type    = str,
                            optional= True,
                            default = 'wholeVolume')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        # pudb.set_trace()
        if options.man or options.synopsis:
            self.show_man_page()

        options.inputDir = options.inputdir
        options.outputDir = options.outputdir

        pfdo_shell = pfdo_mgz2image(vars(options))

        d_pfdo_shell = pfdo_shell.run(timerStart = True)
        # print(pfdo_shell)

        if options.printElapsedTime:
            pfdo_shell.dp.qprint(
                    "Elapsed time = %f seconds" %
                    d_pfdo_shell['runTime']
            )

        sys.exit(0)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)

# ENTRYPOINT
if __name__ == "__main__":
    app = Pfdo_mgz2img()
    app.launch()