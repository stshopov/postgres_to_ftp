from ftplib import FTP
import subprocess
import os
import tarfile
import argparse
import datetime
import os.path

date_now = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
backup_dir = "/tmp/"


def backup_db(database_name, host, user, password):
    sql_file = "{}{}.sql".format(backup_dir, database_name)
    archive_name = "{}.{}.tar.gz".format(sql_file, date_now)
    command = "PGPASSWORD='{}' pg_dump -h {} -U {} -d {} -c -f {} " \
              "--no-privileges --if-exists --lock-wait-timeout=30000"\
        .format(password, host, user, database_name, sql_file)
    subprocess.call(command, shell=True)
    archive = tarfile.open(archive_name, "w:gz")
    archive.add(sql_file)
    archive.close()
    os.remove(sql_file)
    return archive_name


def get_directories(server):
    lines = []
    directories = []
    server.dir(lines.append)
    for line in lines:
        if line[0] == 'd':
            directories.append(line.split(' ')[-1])

    return directories


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ps_host', type=str, help='Postgres host IP')
    parser.add_argument('--ps_user', type=str, help='Postgres user name')
    parser.add_argument('--ps_password', type=str, help='postgres user password')
    parser.add_argument('--database', type=str, help='Name of the database')
    parser.add_argument('--ftp_host', type=str, help='FTP host IP')
    parser.add_argument('--ftp_user', type=str, help='FTP user name')
    parser.add_argument('--ftp_password', type=str, help='FTP user password')
    args = parser.parse_args()
    archive = backup_db(args.database, args.ps_host, args.ps_user, args.ps_password)
    ftp_server = FTP(host=args.ftp_host, user=args.ftp_user, passwd=args.ftp_password)
    directories = get_directories(ftp_server)

    if args.database in directories:
        ftp_server.cwd(args.database)
    elif args.database not in directories:
        ftp_server.mkd(args.database)
        ftp_server.cwd(args.database)

    ftp_server.storbinary('STOR {}'.format(archive.split('/')[2]),
                          open(archive, 'rb'))
    ftp_server.quit()

    if os.path.exists(archive):
        os.remove(archive)


if __name__ == '__main__':
    main()
