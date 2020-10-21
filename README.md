This simple script use pg_dump to make archive and then sent this archive to ftp server. <br/>

How to run the script: <br/>
Before to run the script on the machine you need to have installed postgres-client <br/>
 - sudo apt-get install postgresql-client <br/>

Then run the script with python and correct values for all parameters <br/>
 - python3.6 sql_to_ftp.py --ps_host "<host ip>" --ps_user "<user>" --database "<some db>" --ps_password "<mega secret password>" --ftp_host "<host ip>" --ftp_user "<user>" --ftp_password "<super secret password>" <br/>
 <br/>
If the script will be running on the same machine where is database server --ps_host might be localhost. <br/>
NB: the quotes are mandatory for all arguments values ! <br/>
