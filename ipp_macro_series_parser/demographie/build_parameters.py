#! /usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import logging
import os
import sys
import population
import ipp_macro_series_parser.scripts.demographic_projections_downloader as dpd
from ipp_macro_series_parser.config import Config

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def run_all(pop_input_dir = None, til_input_dir = None, uniform_weight = None, parameters_dir = None, til = False):
    if parameters_dir is None:
        parameters_dir = os.getcwd()
    
    if til_input_dir is not None:
        import dependance
        assert uniform_weight is not None
        dependance_output_dir = os.path.join(
            parameters_dir,
            "dependance"
            )
        dependance.build_prevalence_2010(
            input_dir = til_input_dir,
            output_dir = dependance_output_dir,
            uniform_weight = uniform_weight
            )
        dependance.build_prevalence_all_years(
            input_dir = til_input_dir,
            output_dir = dependance_output_dir,
            to_csv = True
            )

    population_output_dir = os.path.join(parameters_dir, "population")
    population.build_mortality_rates(
        input_dir = pop_input_dir,
        output_dir = population_output_dir,
        to_csv = True,
        uniform_weight = uniform_weight
        )

    population.build_deaths(
        input_dir = pop_input_dir,
        output_dir = population_output_dir,
        to_csv = True,
        uniform_weight = uniform_weight
        )

    population.build_fertility_rates(
        input_dir = pop_input_dir,
        output_dir = population_output_dir,
        to_csv = True,
        uniform_weight = uniform_weight
        )

    population.build_migration(
        input_dir = pop_input_dir,
        output_dir = population_output_dir,
        to_csv = True,
        uniform_weight = uniform_weight
        )

    population.rescale_migration(
        input_dir = pop_input_dir,
        output_dir = population_output_dir,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--download', action = 'store_true',
        help = "download all input files from their web sources")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    parser.add_argument('-o', '--output', type = str, default = None, help = "output directory")
    parser.add_argument('-p', '--pop_input', type = str, default = None, help = "input directory for population files")
    parser.add_argument('-w', '--weight', default = 200, help = "weight used for TIL-France")
    # TODO remove weight from here
    parser.add_argument('-t', '--til_input', default = None,
        help = "input directory for til-specific files (dependance)")
    args = parser.parse_args()

    logging.basicConfig(
        level = logging.DEBUG if args.verbose else logging.WARNING,
        stream = sys.stdout)

    if not os.path.isabs(args.output):
        output_dir = os.path.abspath(args.output)
    else:
        output_dir = args.output

    if not os.path.exists(output_dir):
        log.info('Creating directory {}'.format(output_dir))
        os.makedirs(output_dir)

    if args.download and (args.til_input or args.pop_input):
        parser.error("-d cannot be used with -p nor -t")
        sys.exit(-1)

    if args.til_input and not args.weight:
        print("--weight 200 used by default")

    if args.download:
        dpd.main()
        files = ['insee_projections', 'drees_dependance']
        output_dirs_by_file = {file: Config().get('data', file) for file in files}
        pop_input = output_dirs_by_file['insee_projections']
        til_input = output_dirs_by_file['drees_dependance']

    else:
        pop_input = os.path.abspath(args.pop_input)
        assert os.path.exists(pop_input)

        til_input = args.til_input

        if til_input is not None:
            til_input = os.path.abspath(args.til_input)
            assert os.path.exists(til_input)
        else:
            til_input = None

    run_all(
        pop_input_dir = pop_input,
        til_input_dir = til_input,
        parameters_dir = output_dir,
        uniform_weight = int(args.weight),
        )


if __name__ == "__main__":
    sys.exit(main())
