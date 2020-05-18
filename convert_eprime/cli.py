import argparse

from .convert import text_to_csv, text_to_rcsv, etext_to_rcsv


def _is_valid_file(parser, arg):
    """
    Check if argument is existing file.
    """
    if not op.isfile(arg) and arg is not None:
        parser.error('The file {0} does not exist!'.format(arg))

    return arg


def _get_parser():
    """Set up argument parser for functions."""
    parser = argparse.ArgumentParser(description='Conversion of E-Prime files.')
    subparsers = parser.add_subparsers(help='convert_eprime functions')

    # text_to_csv
    text_to_csv_parser = subparsers.add_parser(
        'text2csv',
        help=('Convert text file produced by successful completion of E-Prime '
              'experiment to csv.'),
    )
    text_to_csv_parser.set_defaults(func=text_to_csv)
    text_to_csv_parser.add_argument(
        'text_file',
        type=lambda x: _is_valid_file(parser, x),
        help=('Raw E-Prime text file to convert')
    )
    text_to_csv_parser.add_argument(
        'out_file',
        type=str,
        help=('Output csv file')
    )

    # text_to_rcsv
    text_to_rcsv_parser = subparsers.add_parser(
        'text2rcsv',
        help=('Convert text file produced by successful completion of E-Prime '
              'experiment to reduced csv.'),
    )
    text_to_rcsv_parser.set_defaults(func=text_to_rcsv)
    text_to_rcsv_parser.add_argument(
        'text_file',
        type=lambda x: _is_valid_file(parser, x),
        help=('Raw E-Prime text file to convert')
    )
    text_to_rcsv_parser.add_argument(
        'out_file',
        type=str,
        help=('Output csv file')
    )
    text_to_rcsv_parser.add_argument(
        '--edat',
        dest='edat_file',
        type=lambda x: _is_valid_file(parser, x),
        help=('Raw E-Prime edat file paired with text_file. '
              'Only used for its file type, because sometimes files will '
              'differ between version of E-Prime (edat vs. edat2 suffix).')
    )
    text_to_rcsv_parser.add_argument(
        '--params',
        dest='param_file',
        type=lambda x: _is_valid_file(parser, x),
        help=('A json file with relevant task-specific parameters')
    )

    # etext_to_rcsv
    # in_file, param_file, out_file=None
    etext_to_rcsv_parser = subparsers.add_parser(
        'etext2rcsv',
        help=('Read exported "E-Prime text" file, reduce columns based on '
              'task-specific list of headers, and write out reduced csv.'),
    )
    etext_to_rcsv_parser.set_defaults(func=etext_to_rcsv)
    etext_to_rcsv_parser.add_argument(
        'in_file',
        type=lambda x: _is_valid_file(parser, x),
        help=('Exported E-Prime text file to convert and reduce')
    )
    etext_to_rcsv_parser.add_argument(
        'out_file',
        type=str,
        help=('Output csv file')
    )
    etext_to_rcsv_parser.add_argument(
        '--params',
        dest='param_file',
        type=lambda x: _is_valid_file(parser, x),
        help=('A json file with relevant task-specific parameters')
    )
    return parser


def _main(argv=None):
    """convert_eprime CLI entrypoint"""
    parser = _get_parser()
    options = parser.parse_args(argv)
    args = vars(options).copy()
    try:
        args.pop('func')
    except KeyError:
        parser.print_help()
        return
    options.func(**args)


if __name__ == '__main__':
    _main()
