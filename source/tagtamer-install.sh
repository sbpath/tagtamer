#!/bin/bash

# Install rpms
yum update -y
yum install -y python3 python3-pip dos2unix yum-utils
amazon-linux-extras install nginx1 -y

# Install Python modules
mkdir -p /home/ec2-user/tag-tamer/prod
chown -R ec2-user:ec2-user /home/ec2-user/tag-tamer
#pip3 install boto3 botocore flask flask-WTF gunicorn Flask_jwt_Extended flask_login
#pip3 install /var/tmp/tagtamer/source/Flask-AWSCognito
su - ec2-user -c "python3 -m venv /home/ec2-user/tag-tamer/prod;source /home/ec2-user/tag-tamer/prod/bin/activate; pip3 install boto3 botocore flask flask-WTF gunicorn Flask_jwt_Extended flask_login /var/tmp/tagtamer/source/Flask-AWSCognito; deactivate"

# Copy code and config
cd /var/tmp/tagtamer/source
cp config/tag-tamer.conf /etc/nginx/conf.d
cp config/proxy_params /etc/nginx
cp config/ssl-redirect.conf  /etc/nginx/default.d/
cp config/tagtamer.service /etc/systemd/system
cp -pr code/* to /home/ec2-user/tag-tamer/

mkdir -p /home/ec2-user/tag-tamer/log
mkdir -p /var/log/tag-tamer
touch /var/log/tag-tamer/tag-tamer.err.log
touch /var/log/tag-tamer/tag-tamer.out.log

# Permissions
chown root:root /etc/nginx/conf.d/tag-tamer.conf /etc/nginx/proxy_params /etc/nginx/default.d/ssl-redirect.conf /etc/systemd/system/tagtamer.service
chown -R ec2-user:ec2-user /home/ec2-user/tag-tamer /var/log/tag-tamer

dos2unix /home/ec2-user/tag-tamer/*.py
dos2unix /home/ec2-user/tag-tamer/templates/*.html


# SSL certificate creation - START
# Fix IP in config
sed -i  "s/10.0.5.59/`hostname -i`/g" /etc/nginx/conf.d/tag-tamer.conf 

# Get Public or Private Hostnames/IPs to configure in certificate
FQDN1=`curl http://169.254.169.254/latest/meta-data/public-hostname` 
FQDN2=`curl http://169.254.169.254/latest/meta-data/local-hostname` 
IP1=`curl http://169.254.169.254/latest/meta-data/public-ipv4`
IP2=`curl http://169.254.169.254/latest/meta-data/local-ipv4`

# Create root CA 
mkdir -p /etc/pki/nginx/
cd /etc/pki/nginx/
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 365 -out rootCA.crt -subj "/C=US/ST=NC/L=Raleigh/O=AWS/OU=AWS Support/CN=amazonaws.com"

# Create intermediate certificate - Alt DNS name input file
echo "subjectAltName = @alt_names

[alt_names]
DNS.1 = $FQDN1
DNS.2 = $FQDN2
IP.1 = $IP1
IP.2 = $IP2" > v3.ext

# Create intermediate certificate
openssl genrsa -out tagtamer.key 2048
openssl req -new -sha256 -key tagtamer.key -subj "/C=US/ST=NC/L=Raleigh/O=AWS/OU=AWS Support/CN=$FQDN1" -out tagtamer.csr
openssl x509 -req -in tagtamer.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out tagtamer.crt -days 365 -sha256 -extfile  v3.ext  

# Create file for import into browser, this can be shared to import into trust store of client from where application being accessed.
# ca-bundle file below.
cat tagtamer.crt rootCA.crt > cert_to_import.crt

# Example: Import to Mac OS trust store
# Ask application Administrator to import  /etc/pki/nginx/cert_to_import.crt to browser where required
# sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain cert_to_import.crt

# Verify command - openssl x509 -text -noout -in tagtamer.crt 

# SSL certificate creation - START

# Enable and start services
systemctl enable tagtamer.service; systemctl  start tagtamer.service
systemctl enable nginx; systemctl start nginx
