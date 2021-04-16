import os
import sys
import traceback

import uuid
import logging
import datetime
import argparse
import configparser

from json_tricks import dumps as json_dump
import matplotlib.pyplot as plt

class io_manager(object):
    def __init__(self, session_id=None, output="logs", config_file_path="config.ini", do_init=True):
        if(do_init):
            self.session_id = session_id if session_id is not None else io_manager.generate_session_id()
            self.output = self.prepare_output_folder(output, session_id)
            self.load_config(config_file_path)

    def prepare_output_folder(self, parent_folder, inc_session_id):
        if(not os.path.isdir(parent_folder)):
            os.mkdir(parent_folder)

        out_dir = "/".join([parent_folder, self.session_id])
        if(not os.path.isdir(out_dir)):
            os.mkdir(out_dir)

        if(inc_session_id is not None):
            out_dir = "/".join([out_dir, datetime.datetime.utcnow().strftime(format='%c').replace(':', '-').replace(' ', '-')])
            os.mkdir(out_dir)

        return out_dir

    def generate_session_id():
        return str(uuid.uuid1()).replace('-', '')

    def load_config(self, config_file_path):
        self.configuration = configparser.ConfigParser()
        self.configuration.read(config_file_path)
        return self.configuration

    def load_console_config(self):
        if 'CONSOLE' in self.configuration:
            description = self.configuration['CONSOLE']['description']
            name = self.configuration['CONSOLE']['name']
            return name, description
        else:
            raise Exception('Missing CONSOLE section from config file')

    def load_celery_config(self):
        if 'CELERY' in self.configuration:
            training_worker_queue = self.configuration['CELERY']['training_queue']
            inference_worker_queue = self.configuration['CELERY']['inference_queue']
            broker = self.configuration['CELERY']['broker']
            backend = self.configuration['CELERY']['backend']
            return training_worker_queue, inference_worker_queue, broker, backend
        else:
            raise Exception('Missing CELERY section from config file')

    def load_celery_worker_config(self):
        if 'CELERY_WORKER' in self.configuration:
            concurrency = self.configuration['CELERY_WORKER']['concurrency']
            logging = self.configuration['CELERY_WORKER']['logging']
            return concurrency, logging
        else:
            raise Exception('Missing CELERY_WORKER section from config file')

    def load_db_config(self):
        if 'MONGODB' in self.configuration:
            host = self.configuration['MONGODB']['host']
            port = self.configuration['MONGODB']['port']
            auth_source = self.configuration['MONGODB']['auth_source']
            user = self.configuration['MONGODB']['user']
            password = self.configuration['MONGODB']['password']
            dbname = self.configuration['MONGODB']['dbname']
            return host, port, auth_source, user, password, dbname
        else:
            raise Exception('Missing MONGODB section from config file')

    def load_zmq_config(self):
        if 'ZMQ' in self.configuration:
            protocol = self.configuration['ZMQ']['protocol']
            host = self.configuration['ZMQ']['host']
            port = self.configuration['ZMQ']['port']
            name = self.configuration['ZMQ']['name']
            return protocol, host, port, name
        else:
            raise Exception('Missing ZMQ section from config file')

    def load_logging(self):
        if 'LOGGING' in self.configuration:
            log_file = self.configuration['LOGGING']['filename']
            logging.basicConfig(
                level = logging._nameToLevel[self.configuration['LOGGING']['level'].upper()],
                filename = '/'.join([self.output, log_file]),
                filemode = 'w',
                format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            raise Exception('Missing LOGGING section from config file')

    def load_network_definition(self):
        if 'NETWORK_DEFINITION' in self.configuration:
            optimizer = self.configuration['NETWORK_DEFINITION']['optimizer']
            loss = self.configuration['NETWORK_DEFINITION']['loss']
        else:
            raise Exception('Missing NETWORK_DEFINITION section from config file')
        return optimizer, loss

    def load_data_scaling_type(self):
        if 'DATA_SCALING' in self.configuration:
            scaling = self.configuration['DATA_SCALING']['scaling']
        else:
            raise Exception('Missing DATA_SCALING section from config file')
        return scaling

    def load_plot_definition(self):
        config = self.configuration
        if 'PLOT_STYLE' in config:
            plot_style = config['PLOT_STYLE']['plot_style']
            plot_title = config['PLOT_STYLE']['plot_title']
            plot_fig_size = (int(config['PLOT_STYLE']['plot_fig_size_x']), int(config['PLOT_STYLE']['plot_fig_size_y']))
            plot_x_label = config['PLOT_STYLE']['plot_x_label']
            plot_y_label = config['PLOT_STYLE']['plot_y_label']
            output_file_name = config['PLOT_STYLE']['output_file_name']
            output_dpi = int(config['PLOT_STYLE']['output_dpi'])
            figformat = config['PLOT_STYLE']['figformat']
            show_plot = int(config['PLOT_STYLE']["show_plot"])
        else:
            raise Exception('Missing PLOT_STYLE section from config file')
        return plot_style, plot_title, plot_fig_size, plot_x_label, plot_y_label, output_file_name, output_dpi, figformat, show_plot

    def parse_args(prog_name, command_desc, args_def):
        parser = argparse.ArgumentParser(prog=prog_name, description=command_desc)
        for adef in args_def:
            parser.add_argument(adef[0], adef[1], help=adef[2], type=adef[3])
        return parser.parse_args()

    def plot_datasets(self, style, title, datasets, figsize, xlabel, ylabel, figfname, dpi, figformat, legend, show=False):
        plt.style.use(style)
        plt.figure(figsize=figsize)
        plt.title(title)
        for i in range(len(datasets)):
            plt.plot(datasets[i], marker='d', linewidth=1)
        plt.xticks(datasets[0].index[0::1])
        plt.xlabel(xlabel, fontsize=18)
        plt.ylabel(ylabel, fontsize=18)
        plt.legend(legend, loc='lower right')
        plt.savefig(fname=".".join(["/".join([self.output, figfname]), figformat]), dpi=dpi, format=figformat)
        if show:
            plt.show()
            
    def out(content, is_exception=False, exception_info="", logger=logging.info):    
        try:
            transport = sys.stdout
            if(is_exception):
                exception_type = "N/A" if exception_info == "" else exception_info[0].__name__
                exception_atfile = "N/A" if exception_info == "" else exception_info[2].tb_frame.f_code.co_filename
                exception_atline = "N/A" if exception_info == "" else exception_info[2].tb_lineno
                transport = sys.stderr
                logger = logging.error if logger is not None else None
                exception_heading = exception_type.join(["\n<ERROR>", "</ERROR>\n"])
                content = "\n".join([(content if isinstance(content, str) else " ".join(content.args)), io_manager.format_exception()])
                io_manager.print(exception_heading, transport, logger)
                io_manager.print(":".join([exception_atfile, str(exception_atline)]).join(["@", "\n"]), transport, logger)
            io_manager.print(content, transport, logger)
        except Exception as ex:
            exception_type = sys.exc_info()[0].__name__
            exception_atfile = sys.exc_info()[2].tb_frame.f_code.co_filename
            exception_atline = sys.exc_info()[2].tb_lineno
            sys.stderr.write("".join([exception_type.join(["\n<ERROR>", " (@output)</ERROR>\n@"]), "\n".join([":".join([exception_atfile, str(exception_atline)]), io_manager.format_exception()])]))
            sys.exit(1)

    def format_exception():
        exception_list = traceback.format_stack()
        exception_list = exception_list[:-2]
        exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
        exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        return "\n".join(exception_list)

    def print(content, transport, logger):
        transport.write(content)
        if logger is not None:
            logger(content.strip('\n'))

    def throw_if_except(*args):
        for a in args:
            if type(a) == Exception:
                raise a
