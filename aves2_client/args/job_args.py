import argparse
import aves2_client.commands.job as job_cmd
import aves2_client.commands.example as example_cmd


aves2_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Command line for AVES2',
    epilog=''
)

subparsers = aves2_parser.add_subparsers(title='Available commands')

# Command: aves2 create
create_job_parser = subparsers.add_parser('create', help='Create aves2 job')
create_job_parser.add_argument('-f', '--file', dest='job_conf', required=True, help='job config file')
create_job_parser.set_defaults(func=job_cmd.create_job)


# Command: aves2 rerun
rerun_job_parser = subparsers.add_parser('rerun', help='Rerun aves2 job')
rerun_job_parser.add_argument('--jobid', dest='job_id', required=True, help='job id')
rerun_job_parser.set_defaults(func=job_cmd.rerun_job)


# Command: aves2 list
list_job_parser = subparsers.add_parser('list', help='List aves2 jobs')
list_job_parser.set_defaults(func=job_cmd.list_jobs)


# Command: aves2 show
show_job_parser = subparsers.add_parser('show', help='Show aves2 job info')
show_job_parser.add_argument('--jobid', dest='job_id', required=True, help='job id')
show_job_parser.set_defaults(func=job_cmd.show_job)


# Command: aves2 delete
delete_job_parser = subparsers.add_parser('delete', help='delete aves2 job')
delete_job_parser.add_argument('--jobid', dest='job_id', required=True, help='job id')
delete_job_parser.set_defaults(func=job_cmd.delete_job)


# Command: aves2 cancel
cancel_job_parser = subparsers.add_parser('cancel', help='cancel aves2 job')
cancel_job_parser.add_argument('--jobid', dest='job_id', required=True, help='job id')
cancel_job_parser.set_defaults(func=job_cmd.cancel_job)


# Command: aves2 log
log_job_parser = subparsers.add_parser('log', help='log aves2 job')
log_job_parser.add_argument('--jobid', dest='job_id', required=True, help='job id')
log_job_parser.set_defaults(func=job_cmd.log_job)


# Command: aves2 example
example_parser = subparsers.add_parser('example', help='show aves2 job example')
example_subparser = example_parser.add_subparsers()

hostpath_example_parser = example_subparser.add_parser('hostpath', help='submit job based on local data')
hostpath_example_parser.set_defaults(func=example_cmd.show_hostpath_template)

ossfile_example_parser = example_subparser.add_parser('ossfile', help='submit job based on oss data')
ossfile_example_parser.set_defaults(func=example_cmd.show_ossfile_template)

pvc_example_parser = example_subparser.add_parser('pvc', help='submit job based on pvc')
pvc_example_parser.set_defaults(func=example_cmd.show_pvc_template)
