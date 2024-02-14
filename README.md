# Requirements
* A [Mailgun](http://www.mailgun.com/) account, for sending out XSS payload fire emails.
* A domain name, preferably something short to keep payload sizes down. Here is a good website for finding two letter domain names: [https://catechgory.com/](https://catechgory.com/). My domain is [xss.ht](xss.ht) for example.
* A wildcard SSL certificate, [here's a cheap one](https://www.namecheap.com/security/ssl-certificates/wildcard.aspx). This is required because XSS Hunter identifies users based off of their sub-domains and they all need to be SSL-enabled. We can't use Let's Encrypt because [they don't support wildcard certificates](https://community.letsencrypt.org/t/frequently-asked-questions-faq/26). I'm going to hold off on insulting the CA business model, but rest assured it's very silly and costs them very little to mint you a wildcard certificate so go with the cheapest provider you can find (as long as it's supported in all browsers).
    
# Setup
* Modify the generate_config.py file
* run this cmd
* """
* sudo docker build -t xsshunter .
* sudo docker run -it -p 80:80 -p 5000:5000 xsshunter
* """
